from __future__ import annotations

import itertools
import pathlib
import sys
import threading
import typing as _t
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field, replace
from weakref import ReferenceType, WeakKeyDictionary, WeakValueDictionary, ref

import sphinx.util.logging
import syntax_diagrams

__all__ = [
    "HrefResolverData",
    "LoadingOptions",
    "ModelProvider",
    "Model",
    "ModelImpl",
    "Position",
    "Section",
    "RuleBase",
    "ParserRule",
    "LexerRule",
    "RuleContent",
    "Reference",
    "Doc",
    "Wildcard",
    "Negation",
    "ZeroPlus",
    "OnePlus",
    "Sequence",
    "Alternative",
    "Literal",
    "Range",
    "CharSet",
    "EMPTY",
    "WILDCARD",
    "RuleContentVisitor",
    "CachedRuleContentVisitor",
    "register_provider",
]

T = _t.TypeVar("T")

_logger = sphinx.util.logging.getLogger("sphinx_syntax")


@dataclass
class HrefResolverData:
    """
    Additional data attached to text nodes.

    See `syntax_diagrams.HrefResolver` for details.

    """

    text_is_weak: bool = True
    """
    Indicates that node's text is weak. If node's href resolves to a documentation
    entity which has

    """


@dataclass
class LoadingOptions:
    """
    Additional options for loading a grammar file.

    """

    use_c_char_literals: bool = True
    """
    Bison-specific setting that indicates whether the target language uses
    C-lite char literals or single quoted strings.

    This option affects parsing of inline code blocks within Bison file.

    """


class ModelProvider(metaclass=ABCMeta):
    """
    Base interface for extracting data from a grammar source files.

    """

    supported_extensions: set[str]
    """
    Set of file extensions that correspond to this provider's syntax,
    including leading periods.

    """

    def can_handle(self, path: pathlib.Path) -> bool:
        """
        Check whether this provider can parse the given diagram file.

        By default, checks file extension against `ModelProvider.supported_extensions`.

        """

        return path.suffix in self.supported_extensions

    @abstractmethod
    def from_file(self, path: pathlib.Path, options: LoadingOptions) -> Model:
        """
        Load model from file.

        If model wasn't found, or there were errors while loading
        the model, this method should print errors to a log and return an empty
        (or a partially loaded) model.

        """

    def from_name(
        self, base_path: pathlib.Path, name: str, options: LoadingOptions
    ) -> Model | None:
        """
        Load model by name.

        Used to load root rule if it's located in a separate grammar. For example,
        when documenting a lexer, but limiting lexemes to only those used in a parser.

        By default, just adds extensions from `~ModelProvider.supported_extensions`
        to ``name`` and loads the file if it exists.

        """

        for extension in self.supported_extensions:
            path = pathlib.Path(base_path, name + extension)
            if model := self.from_file(path, options):
                return model

        _logger.error(
            "can't find grammar %r: file not found\n  Tried files:\n    ",
            name,
            "\n    ".join(
                str(pathlib.Path(base_path, name + extension))
                for extension in sorted(self.supported_extensions)
            ),
            type="sphinx_syntax",
        )

        return None


class Model(metaclass=ABCMeta):
    """
    Represents a single parsed grammar.

    """

    @abstractmethod
    def get_provider(self) -> ModelProvider:
        """
        Return provider that loaded this model.

        """

    @abstractmethod
    def get_name(self) -> str:
        """
        Get grammar name.

        """

    @abstractmethod
    def get_path(self) -> pathlib.Path:
        """
        Get path for the file that this model was loaded from.

        """

    @abstractmethod
    def get_model_docs(self) -> list[tuple[int, str]] | None:
        """
        Get documentation that appears on top of the model.

        The returned list contains one item per documentation comment.

        The first element of this item is a line number at which the comment
        started, the second element is the comment itself.

        """

    @abstractmethod
    def lookup_local(self, name: str) -> RuleBase | None:
        """
        Lookup symbol with the given name.

        Imported models are not checked.

        """

    def lookup(self, name: str) -> RuleBase | None:
        """
        Lookup symbol with the given name.

        Check symbols in the model first, than check imported models.
        To lookup literal tokens, pass contents of the literal,
        e.g. ``model.lookup("'literal'")``.

        Return `None` if symbol cannot be found.

        If there are duplicate symbols, it is unspecified which one is returned.

        """

        for model in self.iter_import_tree():
            symbol = model.lookup_local(name)
            if symbol is not None:
                return symbol

        return None

    @abstractmethod
    def get_imports(self) -> _t.Iterable[Model]:
        """
        Get all imported models.

        No order of iteration is specified.

        Note: cyclic imports *are allowed* in the model.

        """

    def iter_import_tree(self) -> _t.Iterable[Model]:
        """
        Iterate over this model and all imported models.

        No order of iteration is specified.

        """

        models: set[Model] = set()
        visited: set[Model] = set()

        models.add(self)

        while models:
            model = models.pop()
            if model in visited:
                continue
            yield model
            models.update(model.get_imports())
            visited.add(model)

    @abstractmethod
    def get_terminals(self) -> _t.Iterable[LexerRule]:
        """
        Get all terminals (including fragments) declared in this model.

        Terminals declared in imported models are not included.

        No order of iteration is specified.

        """

    @abstractmethod
    def get_non_terminals(self) -> _t.Iterable[ParserRule]:
        """
        Get all non-terminals (parser rules) declared in this model.

        Non-terminals declared in imported models are not included.

        No order of iteration is specified.

        """

    def get_all_rules(self) -> _t.Iterable[RuleBase]:
        """
        Get all rules, both terminals and non-terminals.

        No order of iteration is specified.

        """

        yield from self.get_terminals()
        yield from self.get_non_terminals()


class ModelImpl(Model):
    """
    Default model implementation, simply stores model data.

    """

    def __init__(
        self,
        provider: ModelProvider,
        path: pathlib.Path,
        name: str,
        *,
        docs: list[tuple[int, str]] | None,
        imports: _t.Iterable[Model],
        terminals: _t.Iterable[LexerRule],
        non_terminals: _t.Iterable[ParserRule],
    ):
        self._provider: ModelProvider = provider
        self._path: pathlib.Path = path
        self._name: str = name
        self._docs: list[tuple[int, str]] | None = docs
        self._imports: set[Model] = set(imports)
        self._terminals: dict[str, LexerRule] = {t.name: t for t in terminals}
        self._non_terminals: dict[str, ParserRule] = {
            nt.name: nt for nt in non_terminals
        }

    @classmethod
    def empty(
        cls,
        provider: ModelProvider,
        path: pathlib.Path,
        name: str,
    ):
        return cls(
            provider,
            path,
            name,
            docs=None,
            imports=[],
            terminals=[],
            non_terminals=[],
        )

    def get_provider(self) -> ModelProvider:
        return self._provider

    def get_name(self) -> str:
        return self._name

    def get_path(self) -> pathlib.Path:
        return self._path

    def get_model_docs(self) -> list[tuple[int, str]] | None:
        return self._docs

    def lookup_local(self, name: str) -> RuleBase | None:
        if result := self._non_terminals.get(name):
            return result
        elif result := self._terminals.get(name):
            return result
        else:
            return None

    def get_imports(self) -> _t.Iterable[Model]:
        return self._imports

    def get_terminals(self) -> _t.Iterable[LexerRule]:
        return self._terminals.values()

    def get_non_terminals(self) -> _t.Iterable[ParserRule]:
        return self._non_terminals.values()


@dataclass(order=True, frozen=True, slots=True)
class Position:
    file: pathlib.Path
    """
    Absolute path to the file in which this rule is declared.

    """

    line: int
    """
    Line at which this rule is declared.

    """

    def as_tuple(self):
        return self.file, self.line

    def __repr__(self):
        return "Position({!r}, {!r})".format(self.file, self.line)

    def __str__(self):
        return "{}:{}".format(self.file, self.line)


@dataclass(eq=False, frozen=True, slots=True)
class Section:
    """
    Represents a single section header, i.e. a group of comments that start
    with a triple slash.

    """

    docs: list[tuple[int, str]]
    """
    List of documentation lines in the section description.

    """

    position: Position
    """
    A position at which this section is declared.

    """


@dataclass(eq=False, frozen=True, slots=True)
class RuleBase:
    """
    Base class for parser and lexer rules.

    Note that actual model implementations use `LexerRule` and `ParserRule`
    instead of this base.

    """

    name: str
    """
    Name of this rule.

    """

    display_name: str | None
    """
    Display name from ``doc:name`` command.

    """

    model: Model
    """
    Reference to the model in which this rule was declared.

    """

    position: Position
    """
    A position at which this rule is declared.

    """

    content: RuleContent | None
    """
    Body of the token or rule definition.

    May be omitted for implicitly declared tokens or tokens that were declared
    in the ``tokens`` section of a lexer.

    """

    is_nodoc: bool
    """
    Indicates that the ``doc:nodoc`` flag is set for this rule.

    If true, generators should not output any content for this rule.

    """

    is_no_diagram: bool
    """
    Indicates that the ``doc:no_diagram`` flag is set.

    If true, generators should not produce syntax diagram for this rule.

    """

    css_class: str | None
    """
    Custom css class set via the ``doc:css_class`` command.

    All diagram nodes referencing this rule will have this css class added to them.

    """

    is_inline: bool
    """
    Indicates that the ``doc:inline`` flag is set for this rule.

    If true, generators should not output any content for this rule.

    They should also inline diagram of this rule when rendering
    diagrams for any other rule that refers this rule.

    """

    keep_diagram_recursive: bool
    """
    Indicates that the ``doc:keep-diagram-recursive`` flag is set for this rule.

    If true, diagram renderer will not attempt converting recursive alternatives
    to cycles.

    """

    importance: int
    """
    Importance of the rule, determines its placing in auto-generated diagrams.

    """

    documentation: list[tuple[int, str]] | None
    """
    Documentation for this rule.

    """

    section: Section | None
    """
    Which section this rule belongs to?

    """

    def __str__(self):
        lines = [self.name]

        if self.content is None:
            lines.append("  <implicit>")
        else:
            if isinstance(self.content, Alternative):
                alts = self.content.children
            else:
                alts = (self.content,)

            for i, alt in enumerate(alts):
                if i == 0:
                    lines.append("  : " + str(alt))
                else:
                    lines.append("  | " + str(alt))

        lines.append("  ;")

        return "\n".join(lines)


@dataclass(eq=False, frozen=True, slots=True)
class LexerRule(RuleBase):
    content: RuleContent | None

    is_literal: bool
    """
    Indicates that this token is a literal token.

    Literal tokens are tokens with a single fixed-string literal element.

    """

    is_fragment: bool
    """
    Indicates that this rule is a fragment.

    """


@dataclass(eq=False, frozen=True, slots=True)
class ParserRule(RuleBase):
    content: RuleContent | None


R = _t.TypeVar("R", bound="RuleContent")


def _meta(**kwargs):
    """
    Decorator that sets meta for the given AST node.

    """

    def wrapper(cls: type[R]) -> type[R]:
        cls.__meta__ = replace(cls.__meta__, **kwargs)
        return cls

    return wrapper


_AST_INTERN: WeakValueDictionary[ReferenceType[RuleContent], RuleContent] = (
    WeakValueDictionary()
)


def _intern(v: RuleContent) -> RuleContent:
    return _AST_INTERN.setdefault(ref(v), v)


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class RuleContent:
    """
    Base class for AST nodes that form lexer and parser rules.

    Note that all AST nodes are interned, and can be compared via ``is`` keyword
    instead of ``==``.

    """

    @dataclass(frozen=True, slots=True)
    class _Meta:
        precedence: int = 0
        visitor_relay: str = "visit_default"
        formatter: _t.Callable[..., str] = field(default=lambda x, _: repr(x))

    __meta__ = _Meta()

    def __str__(self):
        p = self.__meta__.precedence
        return self.__meta__.formatter(
            self, lambda x: f"{x}" if x.__meta__.precedence > p else f"({x})"
        )


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
@_meta(visitor_relay="visit_reference")
@_meta(precedence=4, formatter=lambda x, f: f"{x.name}")
class Reference(RuleContent):
    """
    Refers another parser or lexer rule.

    """

    model: Model = field(repr=False)
    """
    Reference to the model in which the rule is used.

    """

    name: str
    """
    Referenced rule name.

    """

    def __new__(cls, model: Model, name: str) -> RuleContent:
        self = object.__new__(cls)
        object.__setattr__(self, "model", model)
        object.__setattr__(self, "name", sys.intern(name))
        return _intern(self)

    def get_reference(self) -> RuleBase | None:
        """
        Lookup and return the actual rule class.

        Returns `None` if reference is invalid.

        """

        return self.model.lookup(self.name)


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
@_meta(visitor_relay="visit_doc")
@_meta(precedence=4, formatter=lambda x, f: f"/** {x.value} */")
class Doc(RuleContent):
    """
    Inline documentation.

    """

    value: str
    """
    Documentation content.

    """

    def __new__(cls, value: str) -> RuleContent:
        self = object.__new__(cls)
        object.__setattr__(self, "value", sys.intern(value))
        return _intern(self)


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
@_meta(visitor_relay="visit_wildcard")
@_meta(precedence=4, formatter=lambda x, f: f".")
class Wildcard(RuleContent):
    """
    Matches any token.

    """

    def __new__(cls):
        return WILDCARD


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
@_meta(visitor_relay="visit_negation")
@_meta(precedence=3, formatter=lambda x, f: f"~{f(x.child)}")
class Negation(RuleContent):
    """
    Matches anything but the child rules.

    """

    child: RuleContent
    """
    Rules that will be negated.

    """

    def __new__(cls, child: RuleContent) -> RuleContent:
        self = object.__new__(cls)
        object.__setattr__(self, "child", child)
        return _intern(self)


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
@_meta(visitor_relay="visit_zero_plus")
@_meta(precedence=3, formatter=lambda x, f: f"{f(x.child)}*")
class ZeroPlus(RuleContent):
    """
    Matches the child zero or more times.

    """

    child: RuleContent
    """
    Rule which will be parsed zero or more times.

    """

    def __new__(cls, child: RuleContent) -> RuleContent:
        if child is EMPTY:
            return child

        self = object.__new__(cls)
        object.__setattr__(self, "child", child)
        return _intern(self)


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
@_meta(visitor_relay="visit_one_plus")
@_meta(precedence=3, formatter=lambda x, f: f"{f(x.child)}+")
class OnePlus(RuleContent):
    """
    Matches the child one or more times.

    """

    child: RuleContent
    """
    Rule which will be parsed one or more times.

    """

    def __new__(cls, child: RuleContent) -> RuleContent:
        if child is EMPTY:
            return child

        self = object.__new__(cls)
        object.__setattr__(self, "child", child)
        return _intern(self)


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
@_meta(visitor_relay="visit_sequence")
@_meta(precedence=1, formatter=lambda x, f: " ".join(map(f, x.children)))
class Sequence(RuleContent):
    """
    Matches a sequence of elements.

    """

    children: tuple[RuleContent, ...]
    """
    Children rules that will be parsed in order.

    """

    linebreaks: tuple[syntax_diagrams.LineBreak, ...] = field(compare=False, repr=False)
    """
    Describes where it is preferable to wrap sequence.

    """

    def __new__(
        cls,
        children: tuple[RuleContent, ...],
        linebreaks: tuple[syntax_diagrams.LineBreak, ...] | None = None,
    ) -> RuleContent:
        if not children:
            return EMPTY
        elif len(children) == 1:
            return children[0]

        assert (
            linebreaks is None or not children or len(linebreaks) + 1 == len(children)
        )

        self = object.__new__(cls)

        if linebreaks is None:
            linebreaks = tuple(
                [syntax_diagrams.LineBreak.DEFAULT] * (len(children) - 1)
            )

        _children = []
        _linebreaks = []

        for item, linebreak in itertools.zip_longest(children, linebreaks):
            if item is EMPTY:
                continue
            if isinstance(item, Sequence):
                _children.extend(item.children)
                _linebreaks.extend(item.linebreaks)
            else:
                _children.append(item)
            if linebreak is not None:
                _linebreaks.append(linebreak)

            children = tuple(_children)
            linebreaks = tuple(_linebreaks)

        object.__setattr__(self, "children", children)
        object.__setattr__(self, "linebreaks", linebreaks)

        return _intern(self)


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
@_meta(visitor_relay="visit_alternative")
@_meta(precedence=0, formatter=lambda x, f: " | ".join(map(f, x.children)))
class Alternative(RuleContent):
    """
    Matches either of children.

    """

    children: tuple[RuleContent, ...]
    """
    Children rules.

    """

    def __new__(
        cls,
        children: tuple[RuleContent, ...],
    ) -> RuleContent:
        if len(children) == 0:
            return EMPTY
        elif len(children) == 1:
            return children[0]

        _children: list[RuleContent] = []
        for item in children:
            if isinstance(item, Alternative):
                _children.extend(item.children)
            else:
                _children.append(item)

        self = object.__new__(cls)

        object.__setattr__(self, "children", tuple(_children))

        return _intern(self)


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
@_meta(visitor_relay="visit_literal")
@_meta(precedence=4, formatter=lambda x, f: f"{x.content}")
class Literal(RuleContent):
    """
    A sequence of symbols (e.g. ``'kwd'``).

    """

    content: str
    """
    Formatted content of the literal, with special symbols escaped.

    """

    def __new__(cls, content: str) -> RuleContent:
        self = object.__new__(cls)
        object.__setattr__(self, "content", sys.intern(content))
        return _intern(self)


@dataclass(frozen=True, slots=True, weakref_slot=True)
@_meta(visitor_relay="visit_range")
@_meta(precedence=4, formatter=lambda x, f: f"{x.start}..{x.end}")
class Range(RuleContent):
    """
    A range of symbols (e.g. ``a..b``).

    """

    start: str
    """
    Range first symbol.

    """

    end: str
    """
    Range last symbol.

    """

    def __new__(cls, start: str, end: str) -> RuleContent:
        self = object.__new__(cls)
        object.__setattr__(self, "start", sys.intern(start))
        object.__setattr__(self, "end", sys.intern(end))
        return _intern(self)


@dataclass(frozen=True, slots=True, weakref_slot=True)
@_meta(visitor_relay="visit_charset")
@_meta(precedence=4, formatter=lambda x, f: f"{x.content}")
class CharSet(RuleContent):
    """
    A character set (e.g. ``[a-zA-Z]``).

    """

    content: str
    """
    Character set description, square brackets included.

    """

    def __new__(cls, content: str) -> RuleContent:
        self = object.__new__(cls)
        object.__setattr__(self, "content", sys.intern(content))
        return _intern(self)


WILDCARD = object.__new__(Wildcard)
"""
Wildcard node.

"""

EMPTY = object.__new__(Sequence)
"""
Empty sequence.

"""

object.__setattr__(EMPTY, "children", ())
object.__setattr__(EMPTY, "linebreaks", ())


class RuleContentVisitor(_t.Generic[T]):
    """
    Generic visitor for rule contents.

    """

    def visit(self, r: RuleContent) -> T:
        return getattr(self, r.__meta__.visitor_relay, self.visit_default)(r)

    def visit_default(self, r: RuleContent) -> T:
        raise RuntimeError(f"no visitor for {r.__class__.__name__!r}")

    def visit_literal(self, r: Literal) -> T:
        return self.visit_default(r)

    def visit_range(self, r: Range) -> T:
        return self.visit_default(r)

    def visit_charset(self, r: CharSet) -> T:
        return self.visit_default(r)

    def visit_reference(self, r: Reference) -> T:
        return self.visit_default(r)

    def visit_doc(self, r: Doc) -> T:
        return self.visit_default(r)

    def visit_wildcard(self, r: Wildcard) -> T:
        return self.visit_default(r)

    def visit_negation(self, r: Negation) -> T:
        return self.visit_default(r)

    def visit_zero_plus(self, r: ZeroPlus) -> T:
        return self.visit_default(r)

    def visit_one_plus(self, r: OnePlus) -> T:
        return self.visit_default(r)

    def visit_sequence(self, r: Sequence) -> T:
        return self.visit_default(r)

    def visit_alternative(self, r: Alternative) -> T:
        return self.visit_default(r)


class CachedRuleContentVisitor(RuleContentVisitor[T]):
    def __init__(self):
        self._cache: WeakKeyDictionary[RuleContent, T] = WeakKeyDictionary()

    def visit(self, r: RuleContent) -> T:
        if r not in self._cache:
            self._cache[r] = super().visit(r)
        return self._cache[r]


_KNOWN_PROVIDERS: list[ModelProvider] = []
_KNOWN_PROVIDERS_LOCK = threading.Lock()


def register_provider(provider: ModelProvider):
    """
    Register new model provider.

    Extensions should call this function during their setup.

    """

    with _KNOWN_PROVIDERS_LOCK:
        _KNOWN_PROVIDERS.append(provider)


def find_provider(path: pathlib.Path) -> ModelProvider | None:
    """
    Find a provider for the given file path.

    """

    with _KNOWN_PROVIDERS_LOCK:
        for provider in _KNOWN_PROVIDERS:
            if provider.can_handle(path):
                return provider

    return None
