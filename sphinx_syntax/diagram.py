import dataclasses
import hashlib
import json
import typing as _t

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
from sphinx_syntax._version import __version__, __version_tuple__

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


class DiagramDirective(sphinx_syntax.domain.ContextManagerMixin):
    option_spec = {
        "force-text": directives.flag,
        **sphinx_syntax.domain.OPTION_SPEC_DIAGRAMS,
        **(docutils.parsers.rst.directives.images.Image.option_spec or {}),
    }
    has_content = True

    def run(self) -> list[docutils.nodes.Node]:
        for option in ["height", "width", "scale", "target"]:
            if option in self.options:
                _logger.warning(
                    "%s doesn't support option %s, ignored",
                    self.name,
                    option,
                    location=self.get_location(),
                    type="sphinx_syntax",
                )
                del self.options[option]

        data = self.get_data()

        hash = hashlib.sha1(
            json.dumps(data, sort_keys=True).encode(), usedforsecurity=False
        ).hexdigest()
        uri = f"data:syntax-diagram;{hash}.svg"

        options = self.get_diagram_options(prefix="")

        return [
            DiagramNode(
                self.block_text,
                *self.make_image(uri),
                data=data,
                refdomain=self.domain,
                grammar=self.get_context_grammar(),
                force_text="force-text" in self.options,
                **options,
            )
        ]

    def get_data(self) -> _t.Any:
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


@dataclasses.dataclass
class HrefResolverData:
    text_is_weak: bool = True


class HrefResolver(rr.HrefResolver[HrefResolverData]):
    """
    Resolves links against the syntax domain.

    """

    def __init__(
        self,
        env: sphinx.environment.BuildEnvironment,
        domain_name: str,
        grammar: str | None,
    ):
        self._env = env
        self._grammar = grammar

        domain = env.get_domain(domain_name)
        assert isinstance(domain, sphinx_syntax.domain.SyntaxDomain)
        self._domain = domain

    def resolve(
        self,
        text: str,
        href: str | None,
        title: str | None,
        resolver_data: HrefResolverData | None,
    ):
        if href:
            return text, href, text
        text_is_weak = True
        if resolver_data:
            text_is_weak = resolver_data.text_is_weak

        text, target = text, text
        text = text.lstrip(".")
        target = target.lstrip("~")
        if text[0:1] == "~":
            text = text[1:]
            dot = text.rfind(".")
            if dot != -1:
                text = text[dot + 1 :]

        xref = sphinx.addnodes.pending_xref(
            "",
            refdoc=self._env.docname,
            refdomain=self._domain.name,
            reftype="_auto",
            refexplicit=not text_is_weak,
            refwarn=False,
        )

        xref[f"{self._domain.name}:grammar"] = self._grammar

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
            if self.app.builder.supported_image_types and not node["force_text"]:
                self.render_svg(image, node, diagram)
            else:
                self.render_text(image, node, diagram)
        node.replace_self(node.children)

    def render_svg(
        self,
        image: docutils.nodes.image,
        node: DiagramNode,
        diagram: rr.Element[HrefResolverData],
    ):
        settings: rr.SvgRenderSettings = self.config["syntax_diagrams_svg_settings"]

        classes = list(
            filter(None, ["syntax-diagram", image.get("class"), settings.css_class])
        )
        if "align" in image:
            classes.append(f"align-{image["align"]}")

        settings = dataclasses.replace(
            settings,
            css_class=" ".join(classes),
            end_class=node.get("end-class", settings.end_class),
            reverse=node.get("reverse", settings.reverse),
            **{
                (name_attr := name.removeprefix("svg-").replace("-", "_")): node.get(
                    name, getattr(settings, name_attr)
                )
                for name in sphinx_syntax.domain.OPTION_SPEC_DIAGRAMS
                if name.startswith("svg-")
            },
        )

        if (
            isinstance(self.app.builder, sphinx.builders.html.StandaloneHTMLBuilder)
            and image.get("loading", "embed") == "embed"
        ):
            settings = dataclasses.replace(
                settings,
                css_style=None,
                title=image.get("alt"),
            )
            content = rr.render_svg(
                diagram,
                settings=settings,
                href_resolver=HrefResolver(
                    self.env, node["refdomain"] or "syntax", node["grammar"]
                ),
            )
            raw = docutils.nodes.raw(image.rawsource, content, format="html")
            if "name" in image:
                raw["name"] = image["name"]
            image.replace_self(raw)
            return

        content = rr.render_svg(diagram, settings=settings)

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
        settings: rr.TextRenderSettings = self.config["syntax_diagrams_text_settings"]

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

        content = rr.render_text(diagram, settings=settings)
        image.replace_self(docutils.nodes.literal_block(image.rawsource, content))

    @property
    def imagedir(self):
        return self.env.app.doctreedir / "images"
