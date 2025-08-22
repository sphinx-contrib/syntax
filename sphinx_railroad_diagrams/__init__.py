import neat_railroad_diagrams as rr

import sphinx.application
from sphinx.transforms.post_transforms import SphinxTransform
import docutils.nodes
import docutils.parsers.rst.directives.images
import sphinx.util.docutils
import typing as _t
import yaml


class DiagramNode(
    docutils.nodes.General, docutils.nodes.Inline, docutils.nodes.Element
):
    pass


class DiagramDirective(sphinx.util.docutils.SphinxDirective):
    option_spec = {**(docutils.parsers.rst.directives.images.Image.option_spec or {})}
    has_content = True

    def run(self) -> list[docutils.nodes.Node]:
        return [DiagramNode("")]


class HrefResolver(rr.HrefResolver):
    def resolve(self, text: str, href: str | None, title_is_weak: bool):
        return super().resolve(text, href, title_is_weak)


class TransformDiagramsToAsciiArt(SphinxTransform):
    default_priority = 100

    def apply(self, **kwargs: _t.Any):
        pass

    def handle(self, node: DiagramNode):
        pass


def setup(app: sphinx.application.Sphinx):
    app.add_transform(TransformDiagramsToAsciiArt)
    app.add_config_value(
        "railroad_diagrams_text_settings",
        rr.TextRenderSettings(),
        "html",
        rr.TextRenderSettings,
    )
    app.add_config_value(
        "railroad_diagrams_svg_settings",
        rr.SvgRenderSettings(css_style=None),
        "html",
        rr.SvgRenderSettings,
    )
