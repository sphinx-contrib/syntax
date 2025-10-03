from __future__ import annotations

import dataclasses
import hashlib
import json
import pathlib
import typing as _t
from enum import Enum

import docutils.nodes
import docutils.parsers.rst.directives.images
import sphinx.addnodes
import sphinx.builders.html
import sphinx.environment
import sphinx.util.logging
import syntax_diagrams as rr
import yaml
from docutils.parsers.rst import directives
from sphinx.transforms import SphinxTransform

import sphinx_syntax.domain
from sphinx_syntax.model import HrefResolverData, Model
from sphinx_syntax.model_renderer import render

_logger = sphinx.util.logging.getLogger("sphinx_syntax")


class DiagramNode(
    docutils.nodes.General, docutils.nodes.Inline, docutils.nodes.Element
):
    """
    Diagram node contains settings for rendering a diagram and wraps an `<image>`
    node. Upon transforming, the `<image>` node inside will be replaced with
    inline SVG. If translator doesn't support inline SVG, the diagram will be
    rendered to a file, and `<image>`'s URI will be updated.

    """


class _JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o) and not isinstance(o, type):
            d = dataclasses.asdict(o)
            return d
        elif isinstance(o, Enum):
            return o.value
        return super().default(o)


class DiagramDirective(sphinx_syntax.domain.ContextManagerMixin):
    option_spec = {
        "force-text": directives.flag,
        **sphinx_syntax.domain.OPTION_SPEC_DIAGRAMS,
        **(docutils.parsers.rst.directives.images.Image.option_spec or {}),
    }
    disabled_options = {"height", "width", "scale", "target", "name"}
    has_content = True

    def run(self) -> list[docutils.nodes.Node]:
        self.process_flags()

        if self.options.get("mark-root-rule") and "end-class" not in self.options:
            self.set_end_class()

        for option in self.disabled_options:
            if option in self.options:
                _logger.warning(
                    f"'{self.name}' directive doesn't support option :{option}:",
                    location=self.get_location(),
                    type="sphinx_syntax",
                    subtype="deprecation_warning",
                    once=True,
                )
                del self.options[option]

        data = self.get_data()

        hash = hashlib.sha1(
            json.dumps(data, sort_keys=True, cls=_JSONEncoder).encode(),
            usedforsecurity=False,
        ).hexdigest()
        uri = f"data:syntax-diagram;{hash}.svg"

        diagram_options = {}
        diagram_options.update(
            {
                name: self.options[key]
                for name in sphinx_syntax.domain.OPTION_SPEC_DIAGRAMS
                if (key := "diagram-" + name) in self.options
            }
        )
        diagram_options.update(
            {
                name: self.options[name]
                for name in sphinx_syntax.domain.OPTION_SPEC_DIAGRAMS
                if name in self.options
            }
        )
        if diagram_options.get("end-class") is None:
            if end_class := self.env.config["syntax_end_class"]:
                diagram_options["end-class"] = rr.EndClass(end_class)

        return [
            docutils.nodes.paragraph(
                self.block_text,
                "",
                DiagramNode(
                    self.block_text,
                    *self.make_image(uri),
                    data=data,
                    grammar=self.get_context_grammar(),
                    force_text="force-text" in self.options,
                    **diagram_options,
                ),
            )
        ]

    def set_end_class(self):
        current_grammar = self.env.ref_context.get("syntax:grammar", "")
        current_rule = self.env.ref_context.get("syntax:rule")
        if not current_grammar or not current_rule:
            return
        root_rule_data = self.get_root_rule()
        if root_rule_data is None:
            return
        grammar, rule = root_rule_data
        if grammar is None:
            grammar = current_grammar
        elif isinstance(grammar, Model):
            grammar = grammar.get_name()
        if current_grammar == grammar and current_rule == f"{grammar}.{rule}":
            self.options["end-class"] = rr.EndClass.COMPLEX
        else:
            self.options["end-class"] = rr.EndClass.SIMPLE

    def get_data(self) -> rr.Element[HrefResolverData]:
        """
        Load and return yaml data for rendering a diagram.

        """

        try:
            return yaml.safe_load("\n".join(self.content.data))
        except yaml.error.MarkedYAMLError as e:
            if e.context_mark is not None:
                self._translate_yaml_mark(e.context_mark)
            if e.problem_mark is not None:
                self._translate_yaml_mark(e.problem_mark)
            raise self.error(f"can't parse syntax diagram description: {e}")
        except yaml.error.YAMLError as e:
            raise self.error(f"can't parse syntax diagram description: {e}")

    def make_image(self, uri: str) -> list[docutils.nodes.Node]:
        """
        Create an `<image>` node that will be wrapped into the `DiagramNode`.

        This method can return an arbitrary doctree, and all `<image>` nodes within it
        will be replaced with the rendered diagram.

        """

        return list(
            docutils.parsers.rst.directives.images.Image(
                "image",
                [uri],
                self.options,
                self.content,
                self.lineno,
                self.content_offset,
                self.block_text,
                self.state,
                self.state_machine,
            ).run()
        )

    def _translate_yaml_mark(self, mark: yaml.error.Mark):
        try:
            name, line = self.content.info(mark.line)
        except IndexError:
            name, line = self.state.document.source, self.content_offset
        mark.name = name or "<syntax diagram description>"
        mark.line = line or self.content_offset


class HrefResolver(rr.HrefResolver[HrefResolverData]):
    """
    Resolves links against the syntax domain.

    """

    def __init__(
        self,
        env: sphinx.environment.BuildEnvironment,
        grammar: str | None,
    ):
        self._env = env
        self._grammar = grammar

        domain = env.get_domain("syntax")
        assert isinstance(domain, sphinx_syntax.domain.SyntaxDomain)
        self._domain = domain

    def resolve(
        self,
        text: str,
        href: str | None,
        title: str | None,
        resolver_data: HrefResolverData | None,
    ):
        if href is not None and (
            href.startswith("http://")
            or href.startswith("https://")
            or href.startswith("/")
            or href.startswith("./")
            or href.startswith("../")
            or href.startswith("#")
            or href in [".", ".."]
        ):
            return text, href, title

        resolver_data = resolver_data or HrefResolverData()

        title = text
        if href is None:
            target = text
            explicit_title = False
        else:
            target = href
            explicit_title = not resolver_data.text_is_weak

        xref = sphinx.addnodes.pending_xref(
            "",
            refdoc=self._env.docname,
            refdomain="syntax",
            reftype="_auto",
            refexplicit=explicit_title,
            refwarn=False,
        )

        xref[f"syntax:grammar"] = self._grammar

        refnodes = self._domain.resolve_any_xref(
            self._env,
            self._env.docname,
            self._env.app.builder,
            target,
            xref,
            docutils.nodes.literal("", text),
        )

        if len(refnodes) == 0:
            return text, None, title
        else:
            refnode = refnodes[0][1]
            if "refid" in refnode:
                return (
                    refnode.astext(),
                    f"#{refnode["refid"]}",
                    refnode.get("reftitle", title),
                )
            elif "refuri" in refnode:
                return (
                    refnode.astext(),
                    f"#{refnode["refuri"]}",
                    refnode.get("reftitle", title),
                )
            else:
                return refnode.astext(), None, refnode.get("reftitle", title)


_LATEX_TEXT_MEASSURE = rr.SimpleTextMeasure(
    character_advance=7.23,
    wide_character_advance=16.48,
    font_size=12,
    line_height=12 * 1.1,
    ascent=10,
)


class ProcessDiagrams(SphinxTransform):
    """
    Processes all `DiagramNode`s in a tree, render diagrams and updates images.

    Doesn't handle converting SVGs to other formats, as this is outside of this
    extension's scope.

    """

    # We need to run before image converters, data extractors, etc.
    default_priority = 100

    def apply(self, **kwargs: _t.Any):
        node: DiagramNode
        for node in list(self.document.findall(DiagramNode)):
            self.handle(node)

    def handle(self, node: DiagramNode):
        image: docutils.nodes.image
        for image in node.findall(docutils.nodes.image):
            diagram = node["data"]
            try:
                if self.app.builder.supported_image_types and not node["force_text"]:
                    if (
                        isinstance(
                            self.app.builder, sphinx.builders.html.StandaloneHTMLBuilder
                        )
                        and image.get("loading", "embed") == "embed"
                    ):
                        self.render_svg(image, node, diagram)
                    else:
                        self.render_svg_latex(image, node, diagram)
                else:
                    self.render_text(image, node, diagram)
            except rr.LoadingError as e:
                _logger.error(
                    f"can't parse syntax diagram description: {e}",
                    location=image,
                    type="sphinx_syntax",
                )
            break
        node.replace_self(node.children)

    def render_svg(
        self,
        image: docutils.nodes.image,
        node: DiagramNode,
        diagram: rr.Element[HrefResolverData],
    ):
        settings = self.svg_settings

        classes = list(
            filter(None, ["syntax-diagram", image.get("class"), settings.css_class])
        )
        if "align" in image:
            classes.append(f"align-{image["align"]}")

        settings = dataclasses.replace(
            settings,
            title=image.get("alt", settings.title),
            css_class=" ".join(classes),
            css_style=None,
            end_class=node.get("end-class", settings.end_class),
            reverse=node.get("reverse", settings.reverse),
        )
        settings = dataclasses.replace(
            settings,
            **{
                (name_attr := name.removeprefix("svg-").replace("-", "_")): node.get(
                    name, getattr(settings, name_attr)
                )
                for name in sphinx_syntax.domain.OPTION_SPEC_DIAGRAMS
                if name.startswith("svg-")
            },
        )

        content = rr.render_svg(
            diagram,
            settings=settings,
            href_resolver=HrefResolver(self.env, node["grammar"]),
            convert_resolver_data=self.make_resolver_data_converter(image),
        )
        raw = docutils.nodes.raw(image.rawsource, content, format="html")
        if "name" in image:
            raw["name"] = image["name"]
        image.replace_self(raw)

    def render_svg_latex(
        self,
        image: docutils.nodes.image,
        node: DiagramNode,
        diagram: rr.Element[HrefResolverData],
    ):
        settings = self.svg_latex_settings

        classes = list(
            filter(None, ["syntax-diagram", image.get("class"), settings.css_class])
        )
        if "align" in image:
            classes.append(f"align-{image["align"]}")

        settings = dataclasses.replace(
            settings,
            title=image.get("alt", settings.title),
            css_class=" ".join(classes),
            css_style=None,
            end_class=node.get("end-class", settings.end_class),
            reverse=node.get("reverse", settings.reverse),
        )
        settings = dataclasses.replace(
            settings,
            **{
                (name_attr := name.removeprefix("svg-").replace("-", "_")): node.get(
                    name, getattr(settings, name_attr)
                )
                for name in sphinx_syntax.domain.OPTION_SPEC_DIAGRAMS
                if name.startswith("svg-")
            },
        )

        for basedir in self.config.html_static_path:
            path = pathlib.Path(
                self.app.builder.confdir, basedir, "syntax-diagrams-latex.css"
            )
            if path.exists() and path.is_file():
                settings = dataclasses.replace(settings, css_style=path.read_text())
                break

        content = rr.render_svg(
            diagram,
            settings=settings,
            convert_resolver_data=self.make_resolver_data_converter(image),
        )

        uri = image["uri"]
        if uri.startswith("data:syntax-diagram;"):
            uri = uri[len("data:syntax-diagram;") :]

        dest = self.imagedir / "syntax_diagrams" / image["uri"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)

        image["uri"] = str(dest)
        image["candidates"] = {"*": image["uri"], "image/svg+xml": image["uri"]}
        image["classes"] = classes

        self.env.images.add_file(self.env.docname, dest)

    def render_text(
        self,
        image: docutils.nodes.image,
        node: DiagramNode,
        diagram: rr.Element[HrefResolverData],
    ):
        settings = self.text_settings

        settings = dataclasses.replace(
            settings,
            end_class=node.get("end-class", settings.end_class),
            reverse=node.get("reverse", settings.reverse),
            **{
                **{
                    (
                        name_attr := name.removeprefix("text-").replace("-", "_")
                    ): node.get(name, getattr(settings, name_attr))
                    for name in sphinx_syntax.domain.OPTION_SPEC_DIAGRAMS
                    if name.startswith("text-")
                },
            },
        )

        content = rr.render_text(
            diagram,
            settings=settings,
            convert_resolver_data=self.make_resolver_data_converter(image),
        )
        image.replace_self(docutils.nodes.literal_block(image.rawsource, content))

    @staticmethod
    def make_resolver_data_converter(node: docutils.nodes.Node):
        def converter(data: _t.Any):
            if data is not None:
                _logger.warning(
                    "diagram descriptions can't have custom resolver_data",
                    location=node,
                    type="sphinx_syntax",
                    once=True,
                )
            return None

        return converter

    @property
    def svg_settings(self):
        settings: rr.SvgRenderSettings | dict[str, _t.Any] = self.config[
            "syntax_diagrams_svg_settings"
        ]
        if isinstance(settings, dict):
            settings = dataclasses.replace(
                rr.SvgRenderSettings(max_width=700), **settings
            )
        return settings

    @property
    def svg_latex_settings(self):
        settings: rr.SvgRenderSettings | dict[str, _t.Any] = self.config[
            "syntax_diagrams_svg_settings"
        ]
        if isinstance(settings, dict):
            settings = dataclasses.replace(
                rr.SvgRenderSettings(
                    max_width=600,
                    terminal_text_measure=_LATEX_TEXT_MEASSURE,
                    non_terminal_text_measure=_LATEX_TEXT_MEASSURE,
                    comment_text_measure=_LATEX_TEXT_MEASSURE,
                    group_text_measure=_LATEX_TEXT_MEASSURE,
                ),
                **settings,
            )
        return settings

    @property
    def text_settings(self):
        settings: rr.TextRenderSettings | dict[str, _t.Any] = self.config[
            "syntax_diagrams_text_settings"
        ]
        if isinstance(settings, dict):
            settings = dataclasses.replace(rr.TextRenderSettings(), **settings)
        return settings

    @property
    def imagedir(self):
        return self.env.app.doctreedir / "images"


class AntlrDiagramDirective(DiagramDirective):
    option_spec = {
        **sphinx_syntax.domain.OPTION_SPEC_AUTORULE,
        **DiagramDirective.option_spec,
    }


class LexerRuleDiagramDirective(AntlrDiagramDirective):
    def get_data(self):
        from sphinx_syntax.ext.antlr4 import PROVIDER

        raw = "\n".join(self.content)
        content = f"grammar X; ROOT : {raw} ;"
        model = PROVIDER.from_text(
            content,
            pathlib.Path(self.state_machine.reporter.source),
            offset=self.content_offset,
        )
        tree = model.lookup("ROOT")
        if tree is None or tree.content is None:
            raise self.error("cannot parse the rule")
        return render(
            tree, self.options["literal-rendering"], self.options["cc-to-dash"]
        )


class ParserRuleDiagramDirective(AntlrDiagramDirective):
    def get_data(self):
        from sphinx_syntax.ext.antlr4 import PROVIDER

        raw = "\n".join(self.content)
        content = f"grammar X; root : {raw} ;"
        model = PROVIDER.from_text(
            content,
            pathlib.Path(self.state_machine.reporter.source),
            offset=self.content_offset,
        )
        tree = model.lookup("root")
        if tree is None or tree.content is None:
            raise self.error("cannot parse the rule")
        return render(
            tree, self.options["literal-rendering"], self.options["cc-to-dash"]
        )
