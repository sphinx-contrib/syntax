Sphinx Syntax
=============

A comprehensive Sphinx extension for documenting language grammars.

Features:

- A new domain with ``grammar`` and ``rule`` directives called ``syntax``.

- Directives for rendering syntax diagrams, such as this one:

  .. syntax:diagram::
     - choice:
       - terminal: 'parser'
       -
       - terminal: 'lexer '
       default: 1
     - terminal: 'grammar'
     - non_terminal: 'identifier'
     - terminal: ';'

- Directive for extracting documentation comments and rendering docs and
  diagrams from ANTLR4 and Bison/YACC source files.

.. toctree::
    :maxdepth: 1

    quickstart
    directives
    roles
    autodoc
    settings
    example
    sphinx-a4doc
    api

.. toctree::
    :hidden:
    :caption: Links

    GitHub <https://github.com/sphinx-contrib/syntax/>
    Issues <https://github.com/sphinx-contrib/syntax/issues>
    Changelog <https://github.com/sphinx-contrib/syntax/blob/main/CHANGELOG.md>
