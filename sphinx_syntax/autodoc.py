from docutils.nodes import Node
from sphinx_syntax.domain import GrammarDescription, RuleDescription
from sphinx_syntax.diagram import DiagramDirective
from sphinx_syntax.api import Grammar, Rule
from docutils.parsers.rst import directives
import sphinx.addnodes
import sphinx.util.parsing
import docutils.statemachine
import typing as _t


class AutoGrammarDescription(GrammarDescription):
    option_spec = {
        "root-rule": directives.unchanged,
        "mark-root-rule": directives.flag,
        "no-mark-root-rule": directives.flag,
        "diagrams": directives.flag,
        "no-diagrams": directives.flag,

        # "only-reachable-from": directives.unchanged,
        # "lexer-rules"
        # "parser-rules"
        # "fragments"
        # "undocumented"
        # "grouping"
        # "ordering"
        "member-order": lambda x: directives.choice(
            x, ("alphabetical", "groupwise", "bysource")
        ),
        **GrammarDescription.option_spec,
    }

    def __init__(
        self,
        *args,
        grammar: Grammar,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.grammar = grammar

    def run(self) -> list[Node]:
        self.arguments = [self.grammar.name]
        self.options = self.options.copy()
        self.options["name"] = self.grammar.human_readable_name
        self.options["imports"] = self.grammar.imports

        if self.grammar.dependencies:
            for dependency in self.grammar.dependencies:
                self.env.note_dependency(dependency)
        if self.grammar.file:
            self.env.note_dependency(self.grammar.file)

        return super().run()

    def transform_content(self, content_node: sphinx.addnodes.desc_content) -> None:
        if description := self.grammar.description:
            if isinstance(description, str):
                description = [
                    (line, i) for i, line in enumerate(description.splitlines())
                ]

            source = str(self.grammar.file) if self.grammar.file else None

            content = docutils.statemachine.StringList(
                initlist=[line[0] for line in description],
                items=description,
                source=source,
            )

            content_node += sphinx.util.parsing.nested_parse_to_nodes(
                self.state,
                content,
            )

        if rules := self.grammar.rules:
            for rule in rules:
                pass
                # content_node += AutoRuleDescription(
                #     name=f"{self.domain}:rule",
                #     arguments=[],
                #     options=self.options,
                #     content=docutils.statemachine.StringList(),
                #     lineno=self.lineno,
                #     content_offset=self.content_offset,
                #     block_text=self.block_text,
                #     state=self.state,
                #     state_machine=self.state_machine,
                #     rule=rule,
                # ).run()


class AutoRuleDescription(RuleDescription):
    def __init__(
        self,
        *args,
        rule: Rule,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.rule = rule

    def run(self) -> list[Node]:
        self.arguments = [self.rule.name]
        self.options = self.options.copy()
        self.options["name"] = self.rule.human_readable_name
        self.options.pop("imports", None)

        if self.rule.file:
            self.env.note_dependency(self.rule.file)

        return super().run()

    def transform_content(self, content_node: sphinx.addnodes.desc_content) -> None:
        if description := self.rule.description:
            if isinstance(description, str):
                description = [
                    (line, i) for i, line in enumerate(description.splitlines())
                ]

            source = str(self.rule.file) if self.rule.file else None

            content = docutils.statemachine.StringList(
                initlist=[line[0] for line in description],
                items=description,
                source=source,
            )

            content_node += sphinx.util.parsing.nested_parse_to_nodes(
                self.state,
                content,
            )

        render_diagram = self.rule.render_diagram
        if render_diagram is None:
            render_diagram = self.options.get("diagram", True)
        if render_diagram:
            content_node += AutoDiagramDirective(
                name=f"{self.domain}:diagram",
                arguments=[],
                options=self.options,
                content=docutils.statemachine.StringList(),
                lineno=self.lineno,
                content_offset=self.content_offset,
                block_text=self.block_text,
                state=self.state,
                state_machine=self.state_machine,
                diagram=self.rule.diagram,
            ).run()


class AutoDiagramDirective(DiagramDirective):
    def __init__(
        self,
        *args,
        diagram: _t.Any,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.diagram = diagram

    def get_data(self) -> _t.Any:
        return self.diagram
