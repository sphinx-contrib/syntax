import pathlib

import sphinx.application
from sphinx.config import ENUM
from syntax_diagrams import SvgRenderSettings, TextRenderSettings

import sphinx_syntax.autodoc
import sphinx_syntax.diagram
import sphinx_syntax.domain
from sphinx_syntax._version import *
from sphinx_syntax.model import *

__all__ = [
    "SvgRenderSettings",
    "TextRenderSettings",
    "HrefResolverData",
    "LoadingOptions",
    "ModelProvider",
    "Model",
    "ModelImpl",
    "Position",
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
    "WILDCARD",
    "EMPTY",
    "RuleContentVisitor",
    "CachedRuleContentVisitor",
    "register_provider",
]


def setup(app: sphinx.application.Sphinx):
    app.add_domain(sphinx_syntax.domain.SyntaxDomain)

    app.add_directive_to_domain(
        "syntax",
        "diagram",
        sphinx_syntax.diagram.DiagramDirective,
    )
    app.add_directive_to_domain(
        "syntax",
        "lexer-diagram",
        sphinx_syntax.diagram.LexerRuleDiagramDirective,
    )
    app.add_directive_to_domain(
        "syntax",
        "parser-diagram",
        sphinx_syntax.diagram.ParserRuleDiagramDirective,
    )
    app.add_directive_to_domain(
        "syntax",
        "autogrammar",
        sphinx_syntax.autodoc.AutoGrammarDescription,
    )
    app.add_directive_to_domain(
        "syntax",
        "autorule",
        sphinx_syntax.autodoc.AutoRuleDescription,
    )

    app.add_post_transform(sphinx_syntax.diagram.ProcessDiagrams)

    app.add_config_value(
        "syntax_a4doc_compat_links",
        False,
        "env",
        bool,
        "generate anchors compatible with sphinx-a4doc",
    )
    app.add_config_value(
        "syntax_base_path",
        ".",
        "env",
        (str, pathlib.Path),
        "base directory with grammar files",
    )
    app.add_config_value(
        "syntax_diagrams_text_settings",
        {},
        "html",
        (TextRenderSettings, dict),
        "settings for text diagram renderer",
    )
    app.add_config_value(
        "syntax_diagrams_svg_settings",
        {},
        "html",
        (SvgRenderSettings, dict),
        "settings for SVG diagram renderer",
    )
    app.add_config_value(
        "syntax_diagrams_svg_latex_settings",
        {},
        "html",
        (SvgRenderSettings, dict),
        "settings for SVG diagram renderer",
    )
    app.add_config_value(
        "syntax_end_class",
        None,
        "env",
        ENUM("simple", "complex", None),
        "end class used for diagrams",
    )
    app.add_config_value(
        "syntax_mark_root_rule",
        True,
        "env",
        bool,
        "whether to mark diagrams for root rule with complex end class",
    )
    app.add_config_value(
        "syntax_diagrams",
        True,
        "env",
        bool,
        "whether to render diagrams for automatically generated rule descriptions",
    )
    app.add_config_value(
        "syntax_cc_to_dash",
        False,
        "env",
        bool,
        "whether to convert rule names to dash case for automatically generated rule descriptions",
    )
    app.add_config_value(
        "syntax_lexer_rules",
        True,
        "env",
        bool,
        "whether to include lexer rules in automatically generated documentation",
    )
    app.add_config_value(
        "syntax_parser_rules",
        True,
        "env",
        bool,
        "whether to include parser rules in automatically generated documentation",
    )
    app.add_config_value(
        "syntax_fragments",
        False,
        "env",
        bool,
        "whether to include fragments in automatically generated documentation",
    )
    app.add_config_value(
        "syntax_undocumented",
        False,
        "env",
        bool,
        "whether to include undocumented rules in automatically generated documentation",
    )
    app.add_config_value(
        "syntax_honor_sections",
        True,
        "env",
        bool,
        "whether to include section comments in automatically generated documentation",
    )
    app.add_config_value(
        "syntax_bison_c_char_literals",
        True,
        "env",
        bool,
        "whether to use c-like char literals or single quoting strings when parsing "
        "inline code in Bison grammars",
    )
    app.add_config_value(
        "syntax_grouping",
        "parser-first",
        "env",
        ENUM("mixed", "lexer-first", "parser-first"),
        "how to group rules in automatically generated documentation",
    )
    app.add_config_value(
        "syntax_ordering",
        "by-source",
        "env",
        ENUM("by-source", "by-name"),
        "how to order rules in automatically generated documentation",
    )
    app.add_config_value(
        "syntax_literal_rendering",
        "contents",
        "env",
        ENUM("name", "contents", "contents-unquoted"),
        "how to render literal lexer rules",
    )

    app.config.html_static_path.insert(0, str(pathlib.Path(__file__).parent / "static"))
    app.add_css_file("syntax-diagrams.css")
    app.add_css_file("syntax-diagrams-ext.css")

    app.setup_extension("sphinx_syntax.ext.antlr4")
    app.setup_extension("sphinx_syntax.ext.bison")

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
