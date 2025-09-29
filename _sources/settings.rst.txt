Settings
========

.. py:data:: syntax_base_path
    :type: str | pathlib.Path

    Base directory for grammar file paths, relative to the location of ``conf.py``.

.. py:data:: syntax_diagrams_text_settings
    :type: dict

    Settings for text diagram renderer. You can override any option from
    `~syntax_diagrams.TextRenderSettings` by adding it to this dict.

.. py:data:: syntax_diagrams_svg_settings
    :type: dict

    Settings for HTML diagram renderer. You can override any option from
    `~syntax_diagrams.SvgRenderSettings` by adding it to this dict.
    The only option that you can't override
    is `~syntax_diagrams.SvgRenderSettings.css_style`,
    styling should be done :ref:`via CSS files <styling-diagrams>` instead.

.. py:data:: syntax_diagrams_svg_latex_settings
    :type: dict

    Settings for LaTeX diagram renderer. You can override any option from
    `~syntax_diagrams.SvgRenderSettings` by adding it to this dict.
    The only option that you can't override
    is `~syntax_diagrams.SvgRenderSettings.css_style`,
    styling should be done :ref:`via CSS files <styling-diagrams>` instead.

.. py:data:: syntax_end_class
    :type: "simple" | "complex" | None

    Default value for :rst:dir:`end-class <syntax:diagram:end-class>` option.

.. py:data:: syntax_mark_root_rule
    :type: bool

    Default value for :rst:dir:`mark-root-rule <syntax:autogrammar:mark-root-rule>` option.

.. py:data:: syntax_diagrams
    :type: bool

    Default value for :rst:dir:`diagrams <syntax:autogrammar:diagrams>` option.

.. py:data:: syntax_cc_to_dash
    :type: bool

    Default value for :rst:dir:`cc-to-dash <syntax:autogrammar:cc-to-dash>` option.

.. py:data:: syntax_lexer_rules
    :type: bool

    Default value for :rst:dir:`lexer-rules <syntax:autogrammar:lexer-rules>` option.

.. py:data:: syntax_parser_rules
    :type: bool

    Default value for :rst:dir:`parser-rules <syntax:autogrammar:parser-rules>` option.

.. py:data:: syntax_fragments
    :type: bool

    Default value for :rst:dir:`fragments <syntax:autogrammar:fragments>` option.

.. py:data:: syntax_undocumented
    :type: bool

    Default value for :rst:dir:`undocumented <syntax:autogrammar:undocumented>` option.

.. py:data:: syntax_honor_sections
    :type: bool

    Default value for :rst:dir:`honor-sections <syntax:autogrammar:honor-sections>` option.

.. py:data:: syntax_bison_c_char_literals
    :type: bool

    Default value for :rst:dir:`honor-sections <syntax:autogrammar:bison-c-char-literals>` option.

.. py:data:: syntax_grouping
    :type: "mixed" | "lexer-first" | "parser-first"

    Default value for :rst:dir:`grouping <syntax:autogrammar:grouping>` option.

.. py:data:: syntax_ordering
    :type: "by-source" | "by-name"

    Default value for :rst:dir:`ordering <syntax:autogrammar:ordering>` option.

.. py:data:: syntax_literal_rendering
    :type: "name" | "contents" | "contents-unquoted"

    Default value for :rst:dir:`literal-rendering <syntax:autogrammar:literal-rendering>` option.

.. py:data:: syntax_a4doc_compat_links
    :type: bool

    If set to `True`, Sphinx Syntax will add additional anchors compatible with
    naming scheme used in ``sphinx-a4doc`` extension.


.. _styling-diagrams:

Styling diagrams
----------------

Default CSS rules for syntax diagrams try to match your HTML theme by using
the ``currentColor`` keyword.

If you need to change them, can add ``syntax-diagrams-ext.css`` to your ``_static``
directory and use it to add additional styles. To completely replace default CSS,
use ``syntax-diagrams.css`` instead. To replace styles used in LaTeX builds,
use ``syntax-diagrams-latex.css``.

For example, this documentation customizes diagrams to look better with
`Furo's`__ dark theme:

__ https://github.com/pradyunsg/furo

.. code-block:: css

    @media (prefers-color-scheme: dark) {
        body[data-theme="auto"] svg.syntax-diagram path {
            stroke: var(--color-foreground-secondary);
        }
    }

    body[data-theme="dark"] svg.syntax-diagram path {
        stroke: var(--color-foreground-secondary);
    }

    svg.syntax-diagram .escape {
        fill: var(--color-api-name);
    }


Adjusting fonts used in diagrams
--------------------------------

Since SVGs can't grow and shrink dynamically, renderer needs to know dimensions
of nodes' text ahead of time. This makes changing fonts and sizes a bit of a hassle.

You will need to set the appropriate properties
via :ref:`CSS files <styling-diagrams>`; in addition to this, you'll need to update
`syntax_diagrams_svg_settings` and `syntax_diagrams_svg_latex_settings` by setting
correct ``*_text_measure`` properties.

See `syntax_diagrams.TextMeasure` for more info on how to do this.
