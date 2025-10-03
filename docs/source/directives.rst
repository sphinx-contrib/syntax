Declaring objects
=================

Objects
-------

.. rst:directive:: .. syntax:grammar:: name

    Directive for documenting grammars:

    .. code-block:: rst

        .. syntax:grammar:: MyGrammar

            Description.

    .. dropdown:: Example output

        .. syntax:grammar:: MyGrammar
            :no-index:

            Description.

    Grammars can't be nested, they also can't appear inside production rules.

.. rst:directive:: .. syntax:rule:: name

    Directive for documenting production rules:

    .. code-block:: rst

        .. syntax:rule:: MyRule

            Description.

    .. dropdown:: Example output

        .. syntax:rule:: MyRule
            :no-index:

            Description.

    Rules can't be nested.


Parameters
----------

All of the above directives accept the standard parameters:

.. rst:directive:option:: no-index
                          no-index-entry
                          no-contents-entry
                          no-typesetting

    The `standard Sphinx options`__ available to all object descriptions.

    __ https://www.sphinx-doc.org/en/master/usage/domains/index.html#basic-markup

.. rst:directive:option:: name: <text>

    Sets a human readable name for a rule or a grammar.

    The primary name is used to refer to an object in documentation; it's used
    in HTML paths, anchors, and serves as a unique object identifier.

    The human readable name is used to display object to a user; it's used
    when rendering documentation and cross-references.

    **Example:**

    .. code-block:: rst

        .. syntax:grammar:: PrimaryName
            :name: Human readable name

            Notice that anchor for this grammar uses its primary name.

        When referring to an object, we use primary name: :syntax:g:`PrimaryName`.
        When this cross-reference is rendered, though,
        it will use a human readable name.

    .. dropdown:: Example output

        .. syntax:grammar:: PrimaryName
            :name: Human readable name

            Notice that anchor for this grammar uses its primary name.

        When referring to an object, we use primary name: :syntax:g:`PrimaryName`.
        When this cross-reference is rendered, though,
        it will use a human readable name.

.. rst:directive:option:: imports: <list of diagram names>

    If your parser generators allows importing grammars, you can use ``imports``
    option to specify which diagrams are imported from the documented one.

    This will affect object resolution for cross-references and diagrams.

    **Example:**

    .. code-block:: rst

        .. syntax:grammar:: BaseGrammar

            .. syntax:rule:: BaseRule

        .. syntax:grammar:: DownstreamGrammar
            :imports: BaseGrammar

            This grammar imports :syntax:g:`BaseGrammar`, so it can reference
            its rules without prefixing them with grammar name:
            :syntax:r:`BaseRule`.

            This also works in diagrams:

            .. syntax:diagram:: BaseRule

    .. dropdown:: Example output

        .. syntax:grammar:: BaseGrammar

            .. syntax:rule:: BaseRule

        .. syntax:grammar:: DownstreamGrammar
            :imports: BaseGrammar

            This grammar imports :syntax:g:`BaseGrammar`, so it can reference
            its rules without prefixing them with grammar name:
            :syntax:r:`BaseRule`.

            This also works in diagrams:

            .. syntax:diagram:: BaseRule

.. rst:directive:option:: diagram-*

    You can add any option from :rst:dir:`syntax:diagram` to an object description
    by prefixing it with ``diagram-``. This option will be used in all diagrams
    that appear within object's description.

    **Example:**

    .. code-block:: rst

        .. syntax:grammar:: MyGrammar
            :diagram-end-class: simple

            All diagrams in this grammar will use simple end class:

            .. syntax:diagram:: Simple end class

            Unless they override it manually:

            .. syntax:diagram:: Complex end class
                :end-class: complex

    .. dropdown:: Example output

        .. syntax:grammar:: MyGrammar
            :no-index:
            :diagram-end-class: simple

            All diagrams in this grammar will use simple end class:

            .. syntax:diagram:: Simple end class

            Unless they override it manually:

            .. syntax:diagram:: Complex end class
                :end-class: complex


Diagrams
--------

.. rst:directive:: .. syntax:diagram::

    This directive renders a syntax diagram. Its contents should be a valid
    YAML__ document containing a description of a diagram element.

    __ https://en.wikipedia.org/wiki/YAML

    Full specification with examples is available in documentation
    for the `syntax-diagrams`__ library. You can also use
    `an online diagram editor`__.

    __ https://syntax-diagrams.readthedocs.io/en/stable/describe.html

    __ https://syntax-diagrams.readthedocs.io/en/stable/try

    **Example:**

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

    **Options:**

    .. rst:directive:option:: alt: <text>

        Alternate text: a short description of the image,
        displayed by applications that cannot display images,
        or spoken by applications for visually impaired users.

    .. rst:directive:option:: align: top | middle | bottom | left | center | right

        The alignment of the image, equivalent to the HTML ``<img>`` tag's ``"align"``
        attribute or the corresponding ``vertical-align`` and ``text-align``
        CSS properties.

    .. rst:directive:option:: class: <text>

        Adds a CSS class to the corresponding ``<svg>`` or ``<img>`` element.

    .. rst:directive:option:: end-class: simple | complex

        Changes how ends of the diagram are rendered.

        .. list-table::
            :header-rows: 1

            * - Simple
              - Complex

            * - .. syntax:diagram::
                    :end-class: simple
                    :svg-padding: 10 10 10 10

                    Simple
              - .. syntax:diagram::
                    :end-class: complex
                    :svg-padding: 10 10 10 10

                    Complex

    .. rst:directive:option:: reverse
                            no-reverse

        Switches diagram direction to right-to-left.

    .. rst:directive:option:: svg-*
                            text-*

        Any other option from `syntax_diagrams_svg_settings`
        or `syntax_diagrams_text_settings` can be overridden as well.
        Replace all underscores in option name with dashes
        and add ``svg-`` or ``text-`` prefix:

        **Example:**

        .. code-block:: rst

            .. syntax:diagram::
                :svg-padding: 15 10 15 10
                :svg-arc-margin: 15
                :svg-arrow-style: triangle

                choice:
                -
                - statement
                - expression
                default: 2

        .. dropdown:: Example output

            .. syntax:diagram::
                :svg-padding: 15 10 15 10
                :svg-arc-margin: 15
                :svg-arrow-style: triangle

                choice:
                -
                - statement
                - expression
                default: 2


Simplified diagram directives
-----------------------------

You can use ANTLR 4 syntax for simple diagrams. It's quicker,
but allows less customization.

.. rst:directive:: syntax:lexer-diagram

    The body of this directive should contain a valid ANTLR 4 lexer rule description.

    **Example:**

    .. code-block:: rst

        .. syntax:lexer-diagram:: ('+' | '-')? ([1-9][0-9]* | '0')

    .. dropdown:: Example output

        .. syntax:lexer-diagram:: ('+' | '-')? ([1-9][0-9]* | '0')

    **Options**

    All options from the :rst:dir:`syntax:diagram` directive ara available,
    as well as :rst:dir:`syntax:autogrammar:cc-to-dash`
    and :rst:dir:`syntax:autogrammar:literal-rendering`.

.. rst:directive:: syntax:parser-diagram

    The body of this directive should contain a valid ANTLR 4 parser rule description.

    **Example:**

    .. code-block:: rst

        .. syntax:parser-diagram::

            SELECT DISTINCT? (
                '*' | expression (AS row_name)? (',' expression (AS row_name)?)*
            )

    .. dropdown:: Example output

        .. syntax:parser-diagram::

            SELECT DISTINCT? (
                '*' | expression (AS row_name)? (',' expression (AS row_name)?)*
            )

    **Options**

    All options from the :rst:dir:`syntax:diagram` directive ara available,
    as well as :rst:dir:`syntax:autogrammar:cc-to-dash`
    and :rst:dir:`syntax:autogrammar:literal-rendering`.
