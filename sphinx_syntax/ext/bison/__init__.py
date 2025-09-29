import pathlib
import re

import antlr4
import sphinx.application
import sphinx.util.logging
import syntax_diagrams
from antlr4 import CommonTokenStream, InputStream

from sphinx_syntax import (
    EMPTY,
    Alternative,
    Doc,
    LexerRule,
    Literal,
    LoadingOptions,
    Model,
    ModelImpl,
    ModelProvider,
    ParserRule,
    Position,
    Reference,
    RuleContent,
    Section,
    Sequence,
)
from sphinx_syntax.ext.syntax.gen.BisonLexer import BisonLexer as Lexer
from sphinx_syntax.ext.syntax.gen.BisonParser import BisonParser as Parser
from sphinx_syntax.ext.syntax.gen.BisonParserVisitor import (
    BisonParserVisitor as ParserVisitor,
)
from sphinx_syntax.ext.utils import LoggingErrorListener, load_docs

__all__ = [
    "BisonProvider",
    "PROVIDER",
]


_logger = sphinx.util.logging.getLogger(__name__)


class BisonProvider(ModelProvider):
    supported_extensions = {".y"}

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
            model = self._loaded[path] = BisonModel(self, path)
            return model

        with open(path, "r", encoding="utf-8", errors="strict") as f:
            self._loaded[path] = self._do_load(f.read(), path, [], options)

        return self._loaded[path]

    def _do_load(
        self,
        text: str,
        path: pathlib.Path,
        imports: list["Model"] | None,
        options: LoadingOptions,
    ) -> "Model":
        content = InputStream(text)

        lexer = Lexer(content)
        lexer.is_like_c = options.use_c_char_literals
        lexer.removeErrorListeners()
        lexer.addErrorListener(LoggingErrorListener(path, 0))

        tokens = CommonTokenStream(lexer)

        parser = Parser(tokens)
        parser.removeErrorListeners()
        parser.addErrorListener(LoggingErrorListener(path, 0))

        tree = parser.grammarSpec()

        if parser.getNumberOfSyntaxErrors():
            return BisonModel(self, path)

        model = BisonModel(self, path)

        for im in imports or []:
            model.add_import(im)

        MetaLoader(model, self).visit(tree)
        ParserRuleLoader(model).visit(tree)

        return model


class BisonModel(ModelImpl):
    def __init__(self, provider: ModelProvider, path: pathlib.Path):
        super().__init__(
            provider=provider,
            path=path,
            name=path.stem,
            docs=None,
            imports=[],
            terminals=[],
            non_terminals=[],
        )

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
    def __init__(self, model: BisonModel, cache: BisonProvider):
        self._model = model
        self._cache = cache
        self._emitted_model_docs = False
        self._docs: list[antlr4.Token] = []
        self._section_lines: list[tuple[int, str]] = []

    def visitGrammarSpec(self, ctx: Parser.GrammarSpecContext):
        super().visitGrammarSpec(ctx)
        if not self._emitted_model_docs:
            doc_info = load_docs(self._model, 0, self._docs, allow_cmd=False)
            self._model.set_model_docs(doc_info.documentation)
            self._emitted_model_docs = True

    def visitRules(self, ctx: Parser.RulesContext):
        return None  # do not recurse into this

    def visitPrequelConstructToken(self, ctx: Parser.PrequelConstructTokenContext):
        if (
            not self._emitted_model_docs
            and self._docs
            and self._docs[0].text.startswith("/**")
        ):
            doc_info = load_docs(self._model, 0, self._docs[:1], allow_cmd=False)
            self._model.set_model_docs(doc_info.documentation)
            self._emitted_model_docs = True
            self._docs.pop(0)

        if self._section_lines:
            section = Section(
                self._section_lines,
                Position(self._model.get_path(), self._section_lines[0][0]),
            )
            self._section_lines = []
        else:
            section = None

        doc_info = load_docs(self._model, 0, self._docs)
        self._docs = []

        tokens = ctx.tokens
        is_literal = False
        literal = ""

        if ctx.name.text == "%epp":
            # Grmtools extension
            if len(tokens) > 1 and doc_info.name is None:
                is_literal = True
                literal = tokens[1].text
            tokens = tokens[:1]
        elif ctx.name.text.startswith("//@"):
            if text := self._parse_token_name(ctx.name.text):
                tok = antlr4.Token()
                tok.line = ctx.start.line
                tok.text = text
                tokens = [tok]
            else:
                _logger.error(
                    f"failed to parse '%token' command",
                    type="sphinx_syntax",
                    location=str(Position(self._model.get_path(), ctx.start.line)),
                )
            pass

        for token in tokens:
            token_text: str = token.text
            content = None

            if self._model.lookup_local(token_text):
                continue

            if doc_info.content:
                content = doc_info.content
                if isinstance(content, Literal):
                    is_literal = True
                    literal = content.content
                else:
                    is_literal = False
                    literal = ""

            if (
                not content
                and not is_literal
                and len(token_text) >= 2
                and (
                    (token_text.startswith('"') and token_text.endswith('"'))
                    or (token_text.startswith("'") and token_text.endswith("'"))
                )
            ):
                is_literal = True
                literal = token_text
                content = Literal(literal)

            rule = LexerRule(
                name=token_text,
                display_name=doc_info.name,
                model=self._model,
                position=Position(self._model.get_path(), token.line),
                is_literal=is_literal,
                is_fragment=False,
                content=content,
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
            if is_literal:
                self._model.set_lexer_rule(literal, rule)

            doc_info.name = None
            doc_info.css_class = None
            doc_info.documentation = []
            doc_info.content = None
            is_literal = False
            literal = ""

    _TOKEN_COMMAND_RE = re.compile(r"^//@\s*%token\s*(?P<name>.*)$")

    def _parse_token_name(self, command: str) -> str | None:
        if match := self._TOKEN_COMMAND_RE.match(command):
            return match.group("name")
        else:
            return None

    def visitPrequelConstructDoc(self, ctx: Parser.PrequelConstructDocContext):
        self._docs.append(ctx.doc)

    def visitPrequelConstructHeader(self, ctx: Parser.PrequelConstructHeaderContext):
        text: str = ctx.header.text.lstrip("/").strip()
        line: int = ctx.header.line
        self._section_lines.append((line, text))


class ParserRuleLoader(ParserVisitor):
    def __init__(self, model: BisonModel):
        self._model = model

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

    def visitPrequelConstruct(self, ctx: Parser.PrequelConstructContext):
        return None

    def visitRuleSpec(self, ctx: Parser.RuleSpecContext):
        section_lines: list[tuple[int, str]] = []

        for token in ctx.headers:
            text: str = token.text.lstrip("/").strip()
            line: int = token.line
            section_lines.append((line, text))

        if section_lines:
            section = Section(
                section_lines, Position(self._model.get_path(), section_lines[0][0])
            )
        else:
            section = None

        content: RuleContent = self.visit(ctx.ruleBlock())
        doc_info = load_docs(self._model, 0, ctx.docs)
        position = Position(self._model.get_path(), ctx.start.line + 0)
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
            section=section,
        )

        self._model.set_parser_rule(rule.name, rule)

    def visitRuleAltList(self, ctx: Parser.RuleAltListContext):
        return self.make_alt_rule(ctx.alts)

    def visitAlternative(self, ctx: Parser.AlternativeContext):
        return self.make_seq_rule(ctx.elements)

    def visitSymbolId(self, ctx: Parser.SymbolIdContext):
        return Reference(self._model, ctx.name.text)

    def visitSymbolLiteral(self, ctx: Parser.SymbolLiteralContext):
        return Literal(ctx.content.text)

    def visitElementActionBlock(self, ctx: Parser.ElementActionBlockContext):
        return EMPTY

    def visitElementPredicateBlock(self, ctx: Parser.ElementPredicateBlockContext):
        return EMPTY

    def visitElementEmpty(self, ctx: Parser.ElementEmptyContext):
        return EMPTY

    def visitElementPrec(self, ctx: Parser.ElementPrecContext):
        return EMPTY

    def visitElementDPrec(self, ctx: Parser.ElementDPrecContext):
        return EMPTY

    def visitElementMerge(self, ctx: Parser.ElementMergeContext):
        return EMPTY

    def visitElementExpect(self, ctx: Parser.ElementExpectContext):
        return EMPTY

    def visitElementExpectRr(self, ctx: Parser.ElementExpectRrContext):
        return EMPTY

    def visitElementInlineDoc(self, ctx: Parser.ElementInlineDocContext):
        docs = load_docs(self._model, 0, [ctx.value], False).documentation
        return Doc(value="\n".join(d[1] for d in docs))


PROVIDER = BisonProvider()


def setup(app: sphinx.application.Sphinx):
    import sphinx_syntax

    sphinx_syntax.register_provider(PROVIDER)

    return {
        "version": sphinx_syntax.__version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
