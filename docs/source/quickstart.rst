Quickstart
==========

Installation
------------

1.  Install ``sphinx-syntax`` using Pip:

    .. code-block:: console

        $ pip install sphinx-syntax

2.  Add it to the ``extensions`` list in your ``conf.py``:

    .. code-block:: python

        extensions = [
            "sphinx_syntax",
        ]

3.  If you plan to extract documentation from grammar files,
    set `syntax_base_path` in your ``conf.py``:

    .. code-block:: python

        # Path to the folder containing grammar files,
        # relative to the directory with `conf.py`.
        syntax_base_path = "../grammars/"

4.  If you're building LaTeX documentation,
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


Declaring objects
-----------------

Use :rst:dir:`syntax:grammar` to create grammars, and :rst:dir:`syntax:rule`
to create production rules:

.. code-block:: rst

    .. syntax:grammar:: MyGrammar

        A grammar for my DSL.

        .. syntax:rule:: root

            The root grammar rule.

.. dropdown:: Example output

    .. syntax:grammar:: MyGrammar
        :no-index-entry:
        :no-contents-entry:

        A grammar for my DSL.

        .. syntax:rule:: root
            :no-index-entry:
            :no-contents-entry:

            The root grammar rule.


Cross-referencing objects
-------------------------

Use :rst:role:`syntax:grammar` (:rst:role:`syntax:g`)
and :rst:role:`syntax:rule` (:rst:role:`syntax:r`)
to cross-reference grammars and rules:

.. code-block:: rst

    Grammar :syntax:g:`MyGrammar` has a root rule :syntax:r:`MyGrammar.root`.

.. dropdown:: Example output

    Grammar :syntax:g:`MyGrammar` has a root rule :syntax:r:`MyGrammar.root`.


Rendering diagrams
------------------

Use :rst:dir:`syntax:diagram` to create syntax diagrams. Diagrams described
using YAML__ format, its structure is detailed in documentation for the
`syntax-diagrams`__ library. You can also use `an online diagram editor`__.

__ https://en.wikipedia.org/wiki/YAML

__ https://syntax-diagrams.readthedocs.io/en/stable/describe.html

__ https://syntax-diagrams.readthedocs.io/en/stable/try

.. code-block:: rst

    .. syntax:diagram::

        - "class"
        - non_terminal: "name"
        - optional:
          - "("
          - non_terminal: "class-bases"
          - ")"
        - ":"

.. dropdown:: Example output

    .. syntax:diagram::

        - "class"
        - non_terminal: "name"
        - optional:
          - "("
          - non_terminal: "class-bases"
          - ")"
        - ":"

Alternatively, you can use ANTLR 4 syntax to describe diagrams. It's quicker,
but allows less customization. See :rst:dir:`syntax:lexer-diagram`
and :rst:dir:`syntax:parser-diagram`:

.. code-block:: rst

    .. syntax:parser-diagram:: 'class' name ('(' classBases ')')? ':'
        :literal-rendering: contents-unquoted
        :cc-to-dash:

.. dropdown:: Example output

    .. syntax:parser-diagram:: 'class' name ('(' classBases ')')? ':'
        :literal-rendering: contents-unquoted
        :cc-to-dash:


Automatic documentation generation
----------------------------------

Use :rst:dir:`syntax:autogrammar` and provide it with a path
to a grammar definition file relative to `syntax_base_path`:

.. code-block:: rst

    .. syntax:autogrammar:: Json.g4
