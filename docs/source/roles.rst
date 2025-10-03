Cross-referencing objects
=========================

.. rst:role:: syntax:grammar
              syntax:g

    Grammars are simply referenced by their name:

    .. code-block:: rst

        Reference to :syntax:g:`Json` grammar.

    .. dropdown:: Example output

        Reference to :syntax:g:`Json` grammar.

.. rst:role:: syntax:rule
              syntax:r

    Rules can be referenced by their name when references appear within their grammar
    description. Otherwise, rules are referenced by full path which includes diagram
    name and rule name separated by a dot:

    .. code-block:: rst

        Reference to :syntax:r:`TargetGrammar.TargetRule`.

        .. syntax:grammar:: TargetGrammar

            Reference to :syntax:r:`TargetRule`.

            .. syntax:rule:: TargetRule

    .. dropdown:: Example output

        Reference to :syntax:r:`TargetGrammar.TargetRule`.

        .. syntax:grammar:: TargetGrammar
            :no-index-entry:
            :no-contents-entry:

            Reference to :syntax:r:`TargetRule`.

            .. syntax:rule:: TargetRule
                :no-index-entry:
                :no-contents-entry:

    If you specify a fully qualified object name, and would like to hide its prefix,
    you can add a tilde (``~``) to the object's path:

    .. code-block:: rst

        Reference to :syntax:r:`~TargetGrammar.TargetRule`.

    .. dropdown:: Example output

        Reference to :syntax:r:`~TargetGrammar.TargetRule`.

    When searching for a rule, Sphinx Syntax will first check the current grammar,
    then any imported grammar, and finally global namespace.

.. rst:role:: syntax:obj

    This is a universal role that searches for a rule first, then for a grammar.


Cross-referencing from diagrams
-------------------------------

Diagram nodes will be linked to their rules automatically, as if using
:rst:role:`syntax:rule`:

.. code-block:: rst

    .. syntax:diagram::

        "TargetGrammar.TargetRule"

    Equivalent to :syntax:rule:`TargetGrammar.TargetRule`.

.. dropdown:: Example output

    .. syntax:diagram::

        "TargetGrammar.TargetRule"

    Equivalent to :syntax:rule:`TargetGrammar.TargetRule`.


If ``href`` option is given, then it is used as a target,
while node's text is used as an explicit title:

.. code-block:: rst

    .. syntax:diagram::

        terminal: "TargetRule"
        href: "TargetGrammar.TargetRule"

    Equivalent to :syntax:rule:`TargetRule <TargetGrammar.TargetRule>`.

.. dropdown:: Example output

    .. syntax:diagram::

        terminal: "TargetRule"
        href: "TargetGrammar.TargetRule"

    Equivalent to :syntax:rule:`TargetRule <TargetGrammar.TargetRule>`.

If ``resolve`` option is set to ``false``, node is not linked:

.. code-block:: rst

    .. syntax:diagram::

        terminal: "TargetRule"
        resolve: false

    Node is not linked.

.. dropdown:: Example output

    .. syntax:diagram::

        terminal: "TargetRule"
        resolve: false

    Node is not linked.
