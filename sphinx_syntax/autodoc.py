from __future__ import annotations

import pathlib
import typing as _t

import docutils.nodes
import docutils.statemachine
import sphinx.addnodes
import sphinx.directives
import sphinx.util.logging
import sphinx.util.parsing
import syntax_diagrams
from docutils.parsers.rst import directives

from sphinx_syntax.diagram import DiagramDirective
from sphinx_syntax.domain import (
    GrammarDescription,
    RuleDescription,
    SyntaxObjectDescription,
)
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


class AutoObjectMixin(SyntaxObjectDescription):
    def load_model(self, name: str) -> Model:
        base_path = self.env.config["syntax_base_path"] or "."
        path = pathlib.Path(self.env.app.confdir, base_path, name)
        # We need to add dependency on this path even if file doesn't exist.
        # This way, Sphinx will pick it up when this file appears.
        self.env.note_dependency(path)
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


class AutoGrammarDescription(AutoObjectMixin, GrammarDescription):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    option_spec = {
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
        "grouping": lambda x: directives.choice(
            x, ("mixed", "lexer-first", "parser-first")
        ),
        "ordering": lambda x: directives.choice(x, ("by-source", "by-name")),
        **GrammarDescription.option_spec,
    }

    def run(self) -> list[docutils.nodes.Node]:
        self.name = self.name.replace("auto", "")

        self.process_flags()
        # self.options.update(self.get_autodoc_options())

        # Load options from config.
        for option in [
            "lexer-rules",
            "parser-rules",
            "fragments",
            "undocumented",
            "honor-sections",
            "grouping",
            "ordering",
        ]:
            if option not in self.options:
                self.options[option] = self.env.config[
                    f"syntax_{option.replace("-", "_")}"
                ]

        self.model = self.load_model(self.arguments[0])
        self.note_deps(self.model)
        self.arguments = [self.model.get_name()]

        if "imports" not in self.options:
            self.options["imports"] = [
                i.get_name() for i in self.model.get_imports() if i.get_name()
            ]

        return super().run()

    def transform_content(self, content_node: sphinx.addnodes.desc_content) -> None:
        content_node += self.render_docs(
            self.model.get_model_docs(), self.model.get_path()
        )

        last_section = None
        honor_sections = (
            self.options["honor-sections"] and self.options["ordering"] == "by-source"
        )
        for rule in self.make_order(self.model):
            if honor_sections and rule.section is not last_section:
                last_section = rule.section
                if last_section:
                    content_node += self.render_docs(
                        last_section.docs, last_section.position.file
                    )

            content_node += AutoRuleDescription(
                name=f"syntax:rule",
                arguments=[str(self.model.get_path()), rule.name],
                options={
                    k: self.options[k]
                    for k in sphinx.directives.ObjectDescription.option_spec
                    if k in self.options
                },
                content=docutils.statemachine.StringList(),
                lineno=self.lineno,
                content_offset=self.content_offset,
                block_text=self.block_text,
                state=self.state,
                state_machine=self.state_machine,
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

    def make_order(self, model: Model) -> _t.Iterable[RuleBase]:
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

        if root_rule_info := self.get_root_rule():
            root_grammar, root_name = root_rule_info
            if root_grammar is None:
                root_model = model
            elif isinstance(root_grammar, Model):
                root_model = root_grammar
            else:
                base_path = pathlib.Path(model.get_path()).parent
                root_model = model.get_provider().from_name(
                    base_path,
                    root_grammar,
                    LoadingOptions(
                        use_c_char_literals=self.options["bison-c-char-literals"]
                    ),
                )
            if root_model:
                self.note_deps(root_model)
                root_rule = root_model.lookup(root_name)
                if root_rule:
                    reachable = find_reachable_rules(root_rule)
                    unique_rules = [r for r in unique_rules if r in reachable]

        if not self.options["undocumented"]:
            unique_rules = [r for r in unique_rules if r.documentation]

        return unique_rules

    def note_deps(self, top_level_model: Model):
        for model in top_level_model.iter_import_tree():
            self.env.note_dependency(model.get_path())
            for rule in model.get_all_rules():
                self.env.note_dependency(rule.position.file)
                if rule.section:
                    self.env.note_dependency(rule.section.position.file)


class AutoRuleDescription(AutoObjectMixin, RuleDescription):
    required_arguments = 2
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        **RuleDescription.option_spec,
    }

    def run(self) -> list[docutils.nodes.Node]:
        self.name = self.name.replace("auto", "")

        self.process_flags()
        # self.options.update(self.get_autodoc_options())

        self.model = self.load_model(self.arguments[0])
        self.env.note_dependency(self.model.get_path())
        rule = self.model.lookup_local(self.arguments[1])
        if rule is None:
            if non_local_rule := self.model.lookup(self.arguments[1]):
                raise self.error(
                    f"can't find rule {self.arguments[1]} "
                    f"in grammar {self.model.get_path()}. "
                    f"Note: this rule is available in grammar "
                    f"{non_local_rule.model.get_path()}"
                )
            else:
                raise self.error(
                    f"can't find rule {self.arguments[1]} "
                    f"in grammar {self.model.get_path()}"
                )
        parent_grammar = self.env.ref_context.get(f"syntax:grammar")
        if not parent_grammar:
            raise self.error(f"{self.name} can't be used outside of a diagram")
        elif parent_grammar != self.model.get_name():
            raise self.error(
                f"trying to document rule {self.arguments[1]} "
                f"as part of grammar {parent_grammar}, but the rule is defined "
                f"in grammar {self.model.get_name()}"
            )
        self.rule = rule
        self.arguments = [self.rule.name]
        if "name" not in self.options:
            if self.rule.display_name:
                self.options["name"] = self.rule.display_name
            elif self.options["cc-to-dash"]:
                self.options["name"] = to_dash_case(self.rule.name)

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
                name=f"syntax:diagram",
                arguments=[],
                options={},
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
        self.diagram = diagram
        super().__init__(*args, **kwargs)

    def get_data(self) -> _t.Any:
        return self.diagram
