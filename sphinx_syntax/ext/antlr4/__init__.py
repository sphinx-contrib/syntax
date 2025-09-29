from __future__ import annotations

import pathlib

import sphinx.application
import sphinx.util.logging
import syntax_diagrams
from antlr4 import CommonTokenStream, InputStream

from sphinx_syntax import (
    EMPTY,
    WILDCARD,
    Alternative,
    CharSet,
    Doc,
    LexerRule,
    Literal,
    LoadingOptions,
    Model,
    ModelImpl,
    ModelProvider,
    Negation,
    OnePlus,
    ParserRule,
    Position,
    Range,
    Reference,
    RuleContent,
    Section,
    Sequence,
    ZeroPlus,
)
from sphinx_syntax.ext.syntax.gen.ANTLRv4Lexer import ANTLRv4Lexer as Lexer
from sphinx_syntax.ext.syntax.gen.ANTLRv4Parser import ANTLRv4Parser as Parser
from sphinx_syntax.ext.syntax.gen.ANTLRv4ParserVisitor import (
    ANTLRv4ParserVisitor as ParserVisitor,
)
from sphinx_syntax.ext.utils import LoggingErrorListener, load_docs

__all__ = [
    "Antlr4Provider",
    "PROVIDER",
]


_logger = sphinx.util.logging.getLogger(__name__)


class Antlr4Provider(ModelProvider):
    supported_extensions = {".g4"}

    def __init__(self):
        self._loaded: dict[pathlib.Path, Model] = {}

    def from_file(self, path: pathlib.Path, options: LoadingOptions) -> Model:
        path = path.expanduser().resolve()

        if path in self._loaded:
            return self._loaded[path]

        if not (path.exists() and path.is_file()):
            _logger.error(
                f"can't load grammar {path!r}: file not found",
                type="sphinx_syntax",
            )
            model = self._loaded[path] = Antlr4Model(self, path, 0, False)
            return model

        with open(path, "r", encoding="utf-8", errors="strict") as f:
            self._loaded[path] = self._do_load(f.read(), path, 0, False, [])

        return self._loaded[path]

    def from_text(
        self,
        text: str,
        path: pathlib.Path,
        offset: int = 0,
        imports: list["Model"] | None = None,
    ) -> "Model":
        return self._do_load(text, path, offset or 0, True, imports)

    def _do_load(
        self,
        text: str,
        path: pathlib.Path,
        offset: int,
        in_memory: bool,
        imports: list["Model"] | None,
    ) -> "Model":
        content = InputStream(text)

        lexer = Lexer(content)
        lexer.removeErrorListeners()
        lexer.addErrorListener(LoggingErrorListener(path, offset))

        tokens = CommonTokenStream(lexer)

        parser = Parser(tokens)
        parser.removeErrorListeners()
        parser.addErrorListener(LoggingErrorListener(path, offset))

        tree = parser.grammarSpec()

        if parser.getNumberOfSyntaxErrors():
            return Antlr4Model(self, path, offset, in_memory)

        model = Antlr4Model(self, path, offset, in_memory)

        for im in imports or []:
            model.add_import(im)

        MetaLoader(model, self).visit(tree)
        LexerRuleLoader(model).visit(tree)
        ParserRuleLoader(model).visit(tree)

        return model


class Antlr4Model(ModelImpl):
    def __init__(
        self, provider: ModelProvider, path: pathlib.Path, offset: int, in_memory: bool
    ):
        super().__init__(
            provider=provider,
            path=path,
            name="<unknown>",
            docs=None,
            imports=[],
            terminals=[],
            non_terminals=[],
        )

        self._in_memory = in_memory
        self._offset = offset

    def is_in_memory(self):
        return self._in_memory

    def get_offset(self) -> int:
        return self._offset

    def set_type(self, t: str | None):
        self._type = t

    def set_name(self, n: str):
        self._name = n

    def set_model_docs(self, docs: list[tuple[int, str]] | None):
        self._docs = docs

    def add_import(self, model: "Model"):
        self._imports.add(model)

    def set_lexer_rule(self, name: str, rule: LexerRule):
        self._terminals[name] = rule

    def set_parser_rule(self, name: str, rule: ParserRule):
        self._non_terminals[name] = rule


class MetaLoader(ParserVisitor):
    def __init__(self, model: Antlr4Model, cache: Antlr4Provider):
        self._model = model
        self._cache = cache
        if self._model.is_in_memory():
            self._basedir = None
        else:
            self._basedir = pathlib.Path(self._model.get_path()).parent

    def add_import(self, name: str, position: Position):
        if self._model.is_in_memory():
            _logger.error(
                "imports are not allowed for in-memory grammars",
                location=str(position),
                type="sphinx_syntax",
            )
        else:
            assert self._basedir
            model = self._cache.from_file(
                self._basedir / (name + ".g4"), LoadingOptions()
            )
            self._model.add_import(model)

    def visitGrammarSpec(self, ctx):
        t = ctx.gtype.getText()
        if "lexer" in t:  # that's nasty =(
            t = "lexer"  # in fact, the whole file is nasty =(
        elif "parser" in t:
            t = "parser"
        else:
            t = None
        self._model.set_name(ctx.gname.getText())
        self._model.set_type(t)
        if ctx.docs:
            docs = load_docs(
                self._model, self._model.get_offset(), ctx.docs, allow_cmd=False
            )
            self._model.set_model_docs(docs.documentation)
        return super(MetaLoader, self).visitGrammarSpec(ctx)

    def visitParserRuleSpec(self, ctx: Parser.ParserRuleSpecContext):
        return None  # do not recurse into this

    def visitLexerRuleSpec(self, ctx: Parser.LexerRuleSpecContext):
        return None  # do not recurse into this

    def visitModeSpec(self, ctx: Parser.ModeSpecContext):
        return None  # do not recurse into this

    def visitOption(self, ctx: Parser.OptionContext):
        if ctx.name.getText() == "tokenVocab":
            self.add_import(
                ctx.value.getText(),
                Position(
                    self._model.get_path(), ctx.start.line + self._model.get_offset()
                ),
            )

    def visitDelegateGrammar(self, ctx: Parser.DelegateGrammarContext):
        self.add_import(
            ctx.value.getText(),
            Position(self._model.get_path(), ctx.start.line + self._model.get_offset()),
        )

    def visitTokenSpec(self, ctx: Parser.TokenSpecContext):
        section_lines: list[tuple[int, str]] = []

        for token in ctx.headers:
            text: str = token.text.lstrip("/").strip()
            line: int = token.line + self._model.get_offset()
            section_lines.append((line, text))

        if section_lines:
            section = Section(
                section_lines, Position(self._model.get_path(), section_lines[0][0])
            )
        else:
            section = None

        doc_info = load_docs(self._model, self._model.get_offset(), ctx.docs)

        rule = LexerRule(
            name=ctx.name.getText(),
            display_name=doc_info.name,
            model=self._model,
            position=Position(
                self._model.get_path(), ctx.start.line + self._model.get_offset()
            ),
            is_literal=isinstance(doc_info.content, Literal),
            is_fragment=False,
            content=doc_info.content,
            is_nodoc=doc_info.is_nodoc,
            is_inline=doc_info.is_inline,
            is_no_diagram=doc_info.is_no_diagram,
            keep_diagram_recursive=doc_info.keep_diagram_recursive,
            css_class=doc_info.css_class,
            importance=doc_info.importance,
            documentation=doc_info.documentation,
            section=section,
        )

        self._model.set_lexer_rule(rule.name, rule)


class RuleLoader(ParserVisitor):
    def __init__(self, model: Antlr4Model):
        self._model = model
        self._current_section: Section | None = None

    def wrap_suffix(self, element, suffix):
        if element == EMPTY:
            return element
        if suffix is None:
            return element
        suffix = suffix.getText()
        if suffix.startswith("?"):
            return Alternative((EMPTY, element))
        if suffix.startswith("+"):
            return OnePlus(child=element)
        if suffix.startswith("*"):
            return ZeroPlus(child=element)
        return element

    def make_alt_rule(self, content):
        return Alternative(children=tuple(self.visit(alt) for alt in content))

    def make_seq_rule(self, content):
        elements = []
        linebreaks = set()

        for element in [self.visit(element) for element in content]:
            if isinstance(element, Sequence):
                elements.extend(element.children)
            else:
                elements.append(element)
            linebreaks.add(len(elements) - 1)

        if len(elements) == 1:
            return elements[0]

        linebreaks = tuple(
            (
                syntax_diagrams.LineBreak.SOFT
                if i in linebreaks
                else syntax_diagrams.LineBreak.DEFAULT
            )
            for i in range(len(elements) - 1)
        )
        return Sequence(tuple(elements), linebreaks)

    def visitRuleSpec(self, ctx: Parser.RuleSpecContext):
        section_lines: list[tuple[int, str]] = []

        for token in ctx.headers:
            text: str = token.text.lstrip("/").strip()
            line: int = token.line + self._model.get_offset()
            section_lines.append((line, text))

        if section_lines:
            self._current_section = Section(
                section_lines, Position(self._model.get_path(), section_lines[0][0])
            )
        else:
            self._current_section = None
        super(RuleLoader, self).visitRuleSpec(ctx)


class LexerRuleLoader(RuleLoader):
    def visitParserRuleSpec(self, ctx: Parser.ParserRuleSpecContext):
        return None  # do not recurse into this

    def visitPrequelConstruct(self, ctx: Parser.PrequelConstructContext):
        return None  # do not recurse into this

    def visitLexerRuleSpec(self, ctx: Parser.LexerRuleSpecContext):
        content: RuleContent = self.visit(ctx.lexerRuleBlock())

        doc_info = load_docs(self._model, self._model.get_offset(), ctx.docs)

        if doc_info.content:
            content = doc_info.content
        if isinstance(content, Literal):
            is_literal = True
            literal = content.content
        else:
            is_literal = False
            literal = ""

        rule = LexerRule(
            name=ctx.name.text,
            display_name=doc_info.name,
            model=self._model,
            position=Position(
                self._model.get_path(), ctx.start.line + self._model.get_offset()
            ),
            content=content,
            is_nodoc=doc_info.is_nodoc,
            is_inline=doc_info.is_inline,
            is_no_diagram=doc_info.is_no_diagram,
            keep_diagram_recursive=doc_info.keep_diagram_recursive,
            css_class=doc_info.css_class,
            importance=doc_info.importance,
            documentation=doc_info.documentation,
            is_fragment=bool(ctx.frag),
            is_literal=is_literal,
            section=self._current_section,
        )

        self._model.set_lexer_rule(rule.name, rule)
        if is_literal:
            self._model.set_lexer_rule(literal, rule)

    def visitLexerAltList(self, ctx: Parser.LexerAltListContext):
        return self.make_alt_rule(ctx.alts)

    def visitLexerAlt(self, ctx: Parser.LexerAltContext):
        return self.visit(ctx.lexerElements())

    def visitLexerElements(self, ctx: Parser.LexerElementsContext):
        return self.make_seq_rule(ctx.elements)

    def visitLexerElementLabeled(self, ctx: Parser.LexerElementLabeledContext):
        return self.wrap_suffix(self.visit(ctx.value), ctx.suffix)

    def visitLexerElementAtom(self, ctx: Parser.LexerElementAtomContext):
        return self.wrap_suffix(self.visit(ctx.value), ctx.suffix)

    def visitLexerElementBlock(self, ctx: Parser.LexerElementBlockContext):
        return self.wrap_suffix(self.visit(ctx.value), ctx.suffix)

    def visitLexerElementAction(self, ctx: Parser.LexerElementActionContext):
        return EMPTY

    def visitLabeledLexerElement(self, ctx: Parser.LabeledLexerElementContext):
        return self.visit(ctx.lexerAtom() or ctx.lexerBlock())

    def visitLexerBlock(self, ctx: Parser.LexerBlockContext):
        return self.visit(ctx.lexerAltList())

    def visitCharacterRange(self, ctx: Parser.CharacterRangeContext):
        return Range(start=ctx.start.text, end=ctx.end.text)

    def visitTerminalRef(self, ctx: Parser.TerminalRefContext):
        return Reference(model=self._model, name=ctx.value.text)

    def visitTerminalLit(self, ctx: Parser.TerminalLitContext):
        content = ctx.value.text
        if content == "''":
            return EMPTY
        else:
            return Literal(content=ctx.value.text)

    def visitLexerAtomCharSet(self, ctx: Parser.LexerAtomCharSetContext):
        content = ctx.value.text
        if content == "[]":
            return EMPTY
        else:
            return CharSet(content=content)

    def visitLexerAtomWildcard(self, ctx: Parser.LexerAtomWildcardContext):
        return WILDCARD

    def visitLexerAtomDoc(self, ctx: Parser.LexerAtomDocContext):
        docs = load_docs(
            self._model, self._model.get_offset(), [ctx.value], False
        ).documentation
        return Doc(value="\n".join(d[1] for d in docs))

    def visitNotElement(self, ctx: Parser.NotElementContext):
        return Negation(child=self.visit(ctx.value))

    def visitNotBlock(self, ctx: Parser.NotBlockContext):
        return Negation(child=self.visit(ctx.value))

    def visitBlockSet(self, ctx: Parser.BlockSetContext):
        return self.make_alt_rule(ctx.elements)

    def visitSetElementRef(self, ctx: Parser.SetElementRefContext):
        return Reference(model=self._model, name=ctx.value.text)

    def visitSetElementLit(self, ctx: Parser.SetElementLitContext):
        content = ctx.value.text
        if content == "''":
            return EMPTY
        else:
            return Literal(content=ctx.value.text)

    def visitSetElementCharSet(self, ctx: Parser.SetElementCharSetContext):
        content = ctx.value.text
        if content == "[]":
            return EMPTY
        else:
            return CharSet(content=content)


class ParserRuleLoader(RuleLoader):
    def visitParserRuleSpec(self, ctx: Parser.ParserRuleSpecContext):
        content: RuleContent = self.visit(ctx.ruleBlock())
        doc_info = load_docs(self._model, self._model.get_offset(), ctx.docs)
        position = Position(
            self._model.get_path(), ctx.start.line + self._model.get_offset()
        )
        if doc_info.content:
            _logger.error(
                f"'content' command can't appear before parser rules",
                type="sphinx_syntax",
                location=str(position),
            )
        rule = ParserRule(
            name=ctx.name.text,
            display_name=doc_info.name,
            model=self._model,
            position=position,
            content=content,
            is_nodoc=doc_info.is_nodoc,
            is_inline=doc_info.is_inline,
            is_no_diagram=doc_info.is_no_diagram,
            keep_diagram_recursive=doc_info.keep_diagram_recursive,
            css_class=doc_info.css_class,
            importance=doc_info.importance,
            documentation=doc_info.documentation,
            section=self._current_section,
        )

        self._model.set_parser_rule(rule.name, rule)

    def visitPrequelConstruct(self, ctx: Parser.PrequelConstructContext):
        return None  # do not recurse into this

    def visitLexerRuleSpec(self, ctx: Parser.LexerRuleSpecContext):
        return None  # do not recurse into this

    def visitModeSpec(self, ctx: Parser.ModeSpecContext):
        return None  # do not recurse into this

    def visitRuleAltList(self, ctx: Parser.RuleAltListContext):
        return self.make_alt_rule(ctx.alts)

    def visitAltList(self, ctx: Parser.AltListContext):
        return self.make_alt_rule(ctx.alts)

    def visitLabeledAlt(self, ctx: Parser.LabeledAltContext):
        return self.visit(ctx.alternative())

    def visitAlternative(self, ctx: Parser.AlternativeContext):
        return self.make_seq_rule(ctx.elements)

    def visitParserElementLabeled(self, ctx: Parser.ParserElementLabeledContext):
        return self.wrap_suffix(self.visit(ctx.value), ctx.suffix)

    def visitParserElementAtom(self, ctx: Parser.ParserElementAtomContext):
        return self.wrap_suffix(self.visit(ctx.value), ctx.suffix)

    def visitParserElementBlock(self, ctx: Parser.ParserElementBlockContext):
        return self.wrap_suffix(self.visit(ctx.value), ctx.suffix)

    def visitParserElementAction(self, ctx: Parser.ParserElementActionContext):
        return EMPTY

    def visitParserInlineDoc(self, ctx: Parser.ParserInlineDocContext):
        docs = load_docs(
            self._model, self._model.get_offset(), [ctx.value], False
        ).documentation
        return Doc(value="\n".join(d[1] for d in docs))

    def visitLabeledElement(self, ctx: Parser.LabeledElementContext):
        return self.visit(ctx.atom() or ctx.block())

    def visitBlock(self, ctx: Parser.BlockContext):
        return self.visit(ctx.altList())

    def visitAtomWildcard(self, ctx: Parser.AtomWildcardContext):
        return WILDCARD

    def visitTerminalRef(self, ctx: Parser.TerminalRefContext):
        return Reference(model=self._model, name=ctx.value.text)

    def visitTerminalLit(self, ctx: Parser.TerminalLitContext):
        return Reference(model=self._model, name=ctx.value.text)

    def visitRuleref(self, ctx: Parser.RulerefContext):
        return Reference(model=self._model, name=ctx.value.text)

    def visitNotElement(self, ctx: Parser.NotElementContext):
        return Negation(child=self.visit(ctx.value))

    def visitNotBlock(self, ctx: Parser.NotBlockContext):
        return Negation(child=self.visit(ctx.value))

    def visitBlockSet(self, ctx: Parser.BlockSetContext):
        return self.make_alt_rule(ctx.elements)

    def visitSetElementRef(self, ctx: Parser.SetElementRefContext):
        return Reference(model=self._model, name=ctx.value.text)

    def visitSetElementLit(self, ctx: Parser.SetElementLitContext):
        return Reference(model=self._model, name=ctx.value.text)

    def visitSetElementCharSet(self, ctx: Parser.SetElementCharSetContext):
        content = ctx.value.text
        if content == "[]":
            return EMPTY
        else:
            return CharSet(content=content)

    def visitCharacterRange(self, ctx: Parser.CharacterRangeContext):
        return Range(start=ctx.start.text, end=ctx.end.text)


PROVIDER = Antlr4Provider()


def setup(app: sphinx.application.Sphinx):
    import sphinx_syntax

    sphinx_syntax.register_provider(PROVIDER)

    return {
        "version": sphinx_syntax.__version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
