from __future__ import annotations

import pathlib
import typing as _t

import docutils.statemachine
import sphinx.addnodes
import sphinx.util.logging
import sphinx.util.parsing
import syntax_diagrams
from docutils.nodes import Node
from docutils.parsers.rst import directives

from sphinx_syntax.diagram import DiagramDirective
from sphinx_syntax.domain import GrammarDescription, RuleDescription
from sphinx_syntax.model import (
    HrefResolverData,
    LoadingOptions,
    Model,
    RuleBase,
    find_provider,
)
from sphinx_syntax.model_renderer import render, to_dash_case
from sphinx_syntax.reachable_finder import find_reachable_rules

_logger = sphinx.util.logging.getLogger("sphinx_syntax")


class AutoGrammarDescription(GrammarDescription):
    option_spec = {
        "root-rule": directives.unchanged,
        "only-reachable-from": directives.unchanged,
        "mark-root-rule": directives.flag,
        "no-mark-root-rule": directives.flag,
        "diagrams": directives.flag,
        "no-diagrams": directives.flag,
        "cc-to-dash": directives.flag,
        "no-cc-to-dash": directives.flag,
        "lexer-rules": directives.flag,
        "no-lexer-rules": directives.flag,
        "parser-rules": directives.flag,
        "no-parser-rules": directives.flag,
        "fragments": directives.flag,
        "no-fragments": directives.flag,
        "undocumented": directives.flag,
        "no-undocumented": directives.flag,
        "honor-sections": directives.flag,
        "no-honor-sections": directives.flag,
        "bison-c-char-literals": directives.flag,
        "no-bison-c-char-literals": directives.flag,
        "grouping": lambda x: directives.choice(
            x, ("mixed", "lexer-first", "parser-first")
        ),
        "ordering": lambda x: directives.choice(x, ("by-source", "by-name")),
        "literal-rendering": lambda x: directives.choice(
            x, ("name", "contents", "contents-unquoted")
        ),
        **GrammarDescription.option_spec,
    }

    def run(self) -> list[Node]:
        self.name = self.name.replace("auto", "")
        self.options = self.options.copy()

        if "only-reachable-from" in self.options:
            if "root-rule" in self.options:
                _logger.error(
                    "option :only-reachable-from: can't be given together with :root-rule:",
                    location=self.get_location(),
                    type="sphinx_syntax",
                )
            else:
                _logger.warning(
                    "option :only-reachable-from: was renamed to :root-rule:",
                    location=self.get_location(),
                    type="sphinx_syntax",
                    subtype="deprecation_warning",
                    once=True,
                )

                self.options["root"] = self.options["only-reachable-from"]

        for flag in [
            "mark-root-rule",
            "diagrams",
            "cc-to-dash",
            "lexer-rules",
            "parser-rules",
            "fragments",
            "undocumented",
            "honor-sections",
            "bison-c-char-literals",
        ]:
            if f"no-{flag}" in self.options:
                if flag in self.options:
                    _logger.error(
                        f":{flag}: can't be given together with :no-{flag}:",
                        location=self.get_location(),
                        type="sphinx_syntax",
                    )
                self.options[flag] = False
                del self.options[f"no-{flag}"]
            elif flag in self.options:
                self.options[flag] = True

        for option in [
            "mark-root-rule",
            "diagrams",
            "cc-to-dash",
            "lexer-rules",
            "parser-rules",
            "fragments",
            "undocumented",
            "grouping",
            "ordering",
            "literal-rendering",
            "honor-sections",
            "bison-c-char-literals",
        ]:
            if option not in self.options:
                self.options[option] = self.env.config[
                    f"syntax_{option.replace("-", "_")}"
                ]

        self.model = self.load_model()
        self.arguments = [self.model.get_name()]
        self.note_deps()

        if "imports" not in self.options:
            self.options["imports"] = [
                i.get_name() for i in self.model.get_imports() if i.get_name()
            ]

        return super().run()

    def load_model(self) -> Model:
        base_path = self.env.config["syntax_base_path"] or "."
        path = pathlib.Path(self.env.app.confdir, base_path, self.arguments[0])
        provider = find_provider(path)
        if provider is None:
            raise self.error(
                f"can't determine file format for {path}; "
                f"make sure that extension for this file type is loaded"
            )
        return provider.from_file(
            path,
            LoadingOptions(use_c_char_literals=self.options["bison-c-char-literals"]),
        )

    def transform_content(self, content_node: sphinx.addnodes.desc_content) -> None:
        content_node += self.render_docs(
            self.model.get_model_docs(), self.model.get_path()
        )

        last_section = None
        honor_sections = (
            self.options["honor-sections"] and self.options["ordering"] == "by-source"
        )
        all_rules, root_rule = self.make_order(self.model)
        for rule in all_rules:
            if honor_sections and rule.section is not last_section:
                last_section = rule.section
                if last_section:
                    content_node += self.render_docs(
                        last_section.docs, last_section.position.file
                    )

            content_node += AutoRuleDescription(
                name=f"{self.domain}:rule",
                arguments=[],
                options=self.options,
                content=docutils.statemachine.StringList(),
                lineno=self.lineno,
                content_offset=self.content_offset,
                block_text=self.block_text,
                state=self.state,
                state_machine=self.state_machine,
                rule=rule,
                is_root=root_rule is not None and rule is root_rule,
            ).run()

    def render_docs(
        self, docs: list[tuple[int, str]] | None, source: pathlib.Path | None
    ):
        if not docs:
            return []

        content = docutils.statemachine.StringList(
            initlist=[line[1] for line in docs],
            items=[(line[1], line[0]) for line in docs],
            source=str(source),
        )

        return sphinx.util.parsing.nested_parse_to_nodes(
            self.state,
            content,
        )

    def make_order(self, model: Model) -> tuple[_t.Iterable[RuleBase], RuleBase | None]:
        lexer_rules = []
        if self.options["lexer-rules"]:
            lexer_rules = model.get_terminals()
            if not self.options["fragments"]:
                lexer_rules = filter(lambda r: not r.is_fragment, lexer_rules)

        parser_rules = []
        if self.options["parser-rules"]:
            parser_rules = model.get_non_terminals()

        if self.options["ordering"] == "by-source":
            precedence = lambda rule: rule.position
        else:
            precedence = lambda rule: rule.name.lower()

        grouping = self.options["grouping"]
        if grouping == "mixed":
            all_rules = sorted(list(*lexer_rules, *parser_rules), key=precedence)
        elif grouping == "lexer-first":
            all_rules = sorted(lexer_rules, key=precedence) + sorted(
                parser_rules, key=precedence
            )
        elif grouping == "parser-first":
            all_rules = sorted(parser_rules, key=precedence) + sorted(
                lexer_rules, key=precedence
            )
        else:
            raise RuntimeError("invalid grouping parameter")

        seen: set[RuleBase] = set()
        unique_rules: list[RuleBase] = []
        for rule in all_rules:
            if rule.is_nodoc or rule.is_inline or rule in seen:
                continue
            seen.add(rule)
            unique_rules.append(rule)

        root_rule = None
        if rule_name := self.options.get("root-rule"):
            rule_model = model
            if " " in rule_name:
                model_path, rule_name = rule_name.rsplit(1)
                base_path = self.env.config["syntax_base_path"] or "."
                path = pathlib.Path(self.env.app.confdir, base_path, model_path)
                provider = find_provider(path)
                if not provider:
                    _logger.error(
                        f"can't determine file format for {path}; "
                        f"make sure that extension for this file type is loaded",
                        location=self.get_location(),
                        type="sphinx_syntax",
                    )
                    rule_model = None
                else:
                    rule_model = provider.from_file(
                        path,
                        LoadingOptions(
                            use_c_char_literals=self.options["bison-c-char-literals"]
                        ),
                    )
            elif "." in rule_name:
                model_name, rule_name = rule_name.rsplit(".", 1)
                base_path = pathlib.Path(rule_model.get_path()).parent
                rule_model = rule_model.get_provider().from_name(
                    base_path,
                    model_name,
                    LoadingOptions(
                        use_c_char_literals=self.options["bison-c-char-literals"]
                    ),
                )
            if rule_model:
                root_rule = rule_model.lookup(rule_name)
                if root_rule:
                    reachable = find_reachable_rules(root_rule)
                    unique_rules = [r for r in unique_rules if r in reachable]

        if not self.options["undocumented"]:
            unique_rules = [r for r in unique_rules if r.documentation]

        return unique_rules, root_rule

    def note_deps(self):
        for model in self.model.iter_import_tree():
            self.env.note_dependency(model.get_path())
            for rule in model.get_all_rules():
                self.env.note_dependency(rule.position.file)
                if rule.section:
                    self.env.note_dependency(rule.section.position.file)


class AutoRuleDescription(RuleDescription):
    def __init__(
        self,
        *args,
        rule: RuleBase,
        is_root: bool,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.rule = rule
        self.is_root = is_root

    def run(self) -> list[Node]:
        self.name = self.name.replace("auto", "")
        self.arguments = [self.rule.name]
        self.options = self.options.copy()
        if self.rule.display_name:
            self.options["name"] = self.rule.display_name
        elif self.options["cc-to-dash"]:
            self.options["name"] = to_dash_case(self.rule.name)
        self.options.pop("imports", None)
        if self.options["mark-root-rule"]:
            self.options["diagram-end-class"] = self.options["end-class"] = (
                syntax_diagrams.EndClass.COMPLEX
                if self.is_root
                else syntax_diagrams.EndClass.SIMPLE
            )

        return super().run()

    def transform_content(self, content_node: sphinx.addnodes.desc_content) -> None:
        if description := self.rule.documentation:
            content = docutils.statemachine.StringList(
                initlist=[line[1] for line in description],
                items=[(line[1], line[0]) for line in description],
                source=str(self.rule.position.file),
            )

            content_node += sphinx.util.parsing.nested_parse_to_nodes(
                self.state,
                content,
            )

        if (
            self.options["diagrams"]
            and not self.rule.is_no_diagram
            and self.rule.content
        ):
            diagram = render(
                self.rule,
                literal_rendering=self.options["literal-rendering"],
                cc_to_dash=self.options["cc-to-dash"],
            )

            content_node += AutoDiagramDirective(
                name=f"{self.domain}:diagram",
                arguments=[],
                options={
                    k: v
                    for k, v in self.options.items()
                    if k in AutoDiagramDirective.option_spec
                    and k not in AutoDiagramDirective.disabled_options
                },
                content=docutils.statemachine.StringList(),
                lineno=self.lineno,
                content_offset=self.content_offset,
                block_text=self.block_text,
                state=self.state,
                state_machine=self.state_machine,
                diagram=diagram,
            ).run()


class AutoDiagramDirective(DiagramDirective):
    def __init__(
        self,
        *args,
        diagram: syntax_diagrams.Element[HrefResolverData],
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.diagram = diagram

    def get_data(self) -> _t.Any:
        return self.diagram
