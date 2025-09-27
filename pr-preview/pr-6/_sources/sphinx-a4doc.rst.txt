Migrating from Sphinx-A4Doc
===========================

1.  Install ``sphinx-syntax``:

    .. code-block:: console

        $ pip install 'sphinx-syntax'

2.  In your ``conf.py``:

    -   replace ``"sphinx_a4doc"`` extension with ``"sphinx_syntax"``.

        .. code-block:: python

            extensions = [
                "sphinx_syntax",
            ]

    -   replace ``a4_base_path`` with `syntax_base_path`.

        Paths are now resolved relative to directory of ``conf.py``,
        so you can remove ``dirname(__file__)``.

    -   set ``syntax_a4doc_compat_links = True`` to generate link anchors compatible with
        Sphinx-A4Doc's naming. This will keep old links to your documentation working.

    -   if you're building LaTeX documentation,
        add an extension to `convert SVGs to PDFs`__:

        __ https://github.com/missinglinkelectronics/sphinxcontrib-svg2pdfconverter

        .. code-block:: console

            $ pip install 'sphinxcontrib-svg2pdfconverter[CairoSVG]'

        .. code-block:: python

            extensions = [
                # ...
                "sphinxcontrib.cairosvgconverter",
            ]

        .. tip::

            See extension's README__ if you want to use Inkscape or RSVG
            instead of CairoSVG.

            __ https://github.com/missinglinkelectronics/sphinxcontrib-svg2pdfconverter

2.  Convert your RST files with our utility (a.k.a. a bunch of regexes).

    -   Check expected diff:

        .. code-block:: console

            $ python -m sphinx_syntax.ext.antlr4.sphinx_a4doc_convert --diff .

    -   Apply diff:

        .. code-block:: console

            $ python -m sphinx_syntax.ext.antlr4.sphinx_a4doc_convert --run .

3.  If you were using ``a4_railroad_diagram.css`` or ``a4_railroad_diagram_latex.css``,
    rename them to ``syntax-diagrams-latex.css`` and ``syntax-diagrams.css``.


Differences between Sphinx Syntax and Sphinx-A4Doc
--------------------------------------------------

Sphinx Syntax is a refactored version of Sphinx-A4Doc.

-   Domain ``a4`` was renamed to ``syntax``. This unties documentation from
    implementation details, allowing us to support other parser generators in future.

-   Some directives and flags were renamed, the automatic conversion script will take
    care of those.

-   Syntax diagrams can now be rendered using ASCII art, so they'll show up
    in text and man page output.

-   Diagram rendering engine was reworked. It includes more optimizations for optional
    elements, recursive rules, and so on. For example, it can now collapse nested
    optionals so that they use less vertical space:

    .. syntax:lexer-diagram:: HEX (HEX (HEX HEX?)?)?

-   Options for :rst:dir:`syntax:diagram` were prefixed with ``text-`` and ``svg-``:

    ===========================  ======================================================================================================
    Old name                     New name
    ===========================  ======================================================================================================
    ``:end-class:``              not renamed
    ``:padding:``                ``:svg-padding:``, ``:text-padding:``
    ``:vertical-separation:``    ``:svg-vertical-choice-separation:``, ``:svg-vertical-seq-separation:``
    ``:horizontal-separation:``  ``:svg-horizontal-seq-separation:``
    ``:arc-radius:``             ``:svg-arc-radius:``, ``:svg-arc-margin:``
    ``:translate-half-pixel:``   removed
    ``:internal-alignment:``     removed
    ``:character-advance:``      removed, available from ``conf.py``
    ``:max-width:``              removed
    ``:literal-rendering:``      not renamed, but only affects :rst:dir:`syntax:lexer-diagram` and :rst:dir:`syntax:parser-diagram` now
    ``:cc-to-dash:``             not renamed, but only affects :rst:dir:`syntax:lexer-diagram` and :rst:dir:`syntax:parser-diagram` now
    ``:alt:``                    not renamed, but only affects SVG accessibility attributes now
    ===========================  ======================================================================================================

-   Directives ``a4:autorule``, ``docstring-marker``, and ``members-marker``
    were removed. As far as I can see, there's no code on GitHub that uses them.
