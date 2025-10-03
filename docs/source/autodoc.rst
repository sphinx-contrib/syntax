Generating documentation for grammars
=====================================

You can automatically generate documentation for a grammar.
We support ANTLR 4 (``.g4``) and YACC/Bison (``.y``) formats.


Autodoc directive
-----------------

.. rst:directive:: .. syntax:autogrammar:: <path>

    This directive parses the given grammar file and automatically generates
    documentation for it. The path is relative to `syntax_base_path`.

    ``autogrammar`` supports all options from :rst:dir:`syntax:grammar`, as well as some
    additional ones:

    .. rst:directive:option:: root-rule: <rule> | <grammar>.<rule> | <path> <rule>

        If given, ``autogrammar`` will only render rules that are reachable
        from this root. This is useful to exclude rules from imported grammars
        that are not used by the primary grammar.

        The value should be either name of a rule from the grammar that’s
        being documented, a grammar name and a rule name separated by a dot,
        or a grammar file and a rule name separated by a space.

        For example, suppose we're documenting ANTLR grammars ``Lexer.g4``
        and ``Parser.g4``. To filter lexer rules that are not used
        by parser grammar, use:

        .. code-block:: rst

            .. syntax:autogrammar:: Parser.g4
                :root-rule: Parser.root

            .. syntax:autogrammar:: Lexer.g4
                :root-rule: Parser.root

    .. rst:directive:option:: mark-root-rule
                              no-mark-root-rule

        If enabled, diagrams in the :rst:dir:`root-rule <syntax:autogrammar:root-rule>`
        will use complex line endings, while diagrams in other rules will use simple ones
        (see :rst:dir:`end-class <syntax:diagram:end-class>`).

    .. rst:directive:option:: diagrams
                              no-diagrams

        Enable automatic generation of syntax diagrams for all documented rules.

    .. rst:directive:option:: cc-to-dash
                              no-cc-to-dash

        For rules without explicit human-readable names, generate ones by converting
        rule name from ``CamelCase`` or ``snake_case`` to ``dash-case``.

    .. rst:directive:option:: lexer-rules
                              no-lexer-rules

        Controls whether lexer rules should appear in documentation.
        Enabled by default.

    .. rst:directive:option:: parser-rules
                              no-parser-rules

        Controls whether parser rules should appear in documentation.
        Enabled by default.

    .. rst:directive:option:: fragments
                              no-fragments

        Controls whether fragments should appear in documentation (for formats
        that support them). Disabled by default.

    .. rst:directive:option:: undocumented
                              no-undocumented

        Controls whether undocumented rules should appear in documentation.
        Disabled by default.

    .. rst:directive:option:: honor-sections
                              no-honor-sections

        If true, render :ref:`section comments <comments-syntax>`, treating them as paragraphs
        placed between rules.

        This setting has no effect unless
        :rst:dir:`ordering <syntax:autogrammar:ordering>` is ``by-source``.

    .. rst:directive:option:: bison-c-char-literals
                              no-bison-c-char-literals

        If true, Bison parser will expect C-like char literals or Rust-like lifetimes
        when parsing inline code in grammar files. Otherwise, it will expect
        single-quoted strings.

    .. rst:directive:option:: grouping: mixed | lexer-first | parser-first

        Controls how ``autogrammar`` groups rules that are extracted from sources.

        -   ``mixed`` -- there’s one group that contain all rules.

        -   ``lexer-first`` -- there are two group: one for parser rules
            and one for lexer rules and fragments. Lexer group goes first.

        -   ``parser-first`` -- like ``lexer-first``, but parser group precedes
            lexer group.

    .. rst:directive:option:: ordering: by-source | by-name

        Controls how ``autogrammar`` orders rules within each group
        (see grouping :rst:dir:`grouping <syntax:autogrammar:grouping>`).

        -   ``by-source`` -- rules are ordered as they appear in the grammar file.

        -   ``by-name`` -- rules are ordered lexicographically.

    .. rst:directive:option:: literal-rendering: name | contents | contents-unquoted

        Controls how literal rules (i.e. lexer rules that only consist
        of one string) are rendered. Available options are:

        -   ``name`` -- only name of the literal rule is displayed.

        -   ``contents`` -- quoted literal string is displayed.

            .. syntax:lexer-diagram:: 'hello\nworld'
                :literal-rendering: contents
                :svg-padding: 10 1 1 1

        -   ``contents-unquoted`` -- literal string is displayed, quotes stripped away.

            .. syntax:lexer-diagram:: 'hello\nworld'
                :literal-rendering: contents-unquoted
                :svg-padding: 10 1 1 1

.. rst:directive:: .. syntax:autorule:: <path> <name>

    Documents a single rule from the given grammar.

    This directive should be used inside :rst:dir:`syntax:grammar`; name of the
    current grammar should match name of the autorule's grammar.

    This directive supports all options from :rst:dir:`syntax:rule`,
    including overrides for :rst:dir:`syntax:lexer-diagram`,
    :rst:dir:`syntax:parser-diagram`, and automatically generated diagrams.


.. _comments-syntax:

Grammar comments and annotations
--------------------------------

The :rst:dir:`syntax:autogrammar` directive does not parse any comment that's found
in a grammar file. Instead, it searches for 'documentation' comments, i.e. ones
specially formatted. There are three types of such comments:

-   documentation comments are multiline comments that start with ``/**``
    (that is, a slash followed by double asterisk). These comments should contain
    valid rst-formatted text.

    Documentation comments can appear at the top of a file, before production rules,
    or within them.

    **Example:**

    .. tab-set::
        :sync-group: syntax

        .. tab-item:: ANTLR
            :sync: antlr

            .. code-block:: antlr
                :force:

                /**
                 * Documentation for a file.
                 */

                tokens {
                    /**
                     * Documentation for an externally-defined token.
                     */
                    NAME
                }

                /**
                 * Documentation for a rule.
                 */
                argument
                    : /** inline comment */ expr
                    | /** inline comment */ NAME '=' expr
                    ;

        .. tab-item:: Bison
            :sync: bison

            .. code-block:: bison

                /**
                 * Documentation for a file.
                 */

                /**
                 * Documentation for an externally-defined token.
                 *
                 * Also works with `%left`, `%right`, `%nonassoc`, `%precedence`, `%epp`.
                 */
                %token NAME

                /**
                 * You can also provide documentation for a token
                 * without telling Bison about it.
                 *
                 * As far as Bison is concerned, this is just a comment.
                 */
                //@ %token '+'

                %%

                /**
                 * Documentation for a rule.
                 */
                argument
                    : /** inline comment */ expr
                    | /** inline comment */ NAME "=" expr
                    ;

-   control comments are inline comments that start with ``//@``. Control
    comments contain special commands that affect rendering process.

    They can appear right before a documented object.

    **Example:**

    .. tab-set::
        :sync-group: syntax

        .. tab-item:: ANTLR
            :sync: antlr

            .. code-block:: antlr
                :force:

                tokens {
                    //@ doc:content [a-zA-Z_][a-zA-Z0-9_]*
                    NAME
                }

                //@ doc:inline
                moduleItem
                    : declaration
                    | statement
                    ;

        .. tab-item:: Bison
            :sync: bison

            .. code-block:: bison

                //@ doc:content [a-zA-Z_][a-zA-Z0-9_]*
                %token NAME

                %%

                //@ doc:inline
                moduleItem
                    : import
                    | symbol
                    ;

-   section comments are comments that start with ``///``. They're used to render text
    between production rules and split grammar definition in sections.

    **Example:**

    .. tab-set::
        :sync-group: syntax

        .. tab-item:: ANTLR
            :sync: antlr

            .. code-block:: antlr

                /// **Module definition**
                ///
                /// This paragraph describes the ``Module definition``
                /// section of the grammar.

                module
                    : moduleItem* EOF
                    ;

                moduleItem
                    : import
                    | symbol
                    ;

                /// **Imports**
                ///
                /// This paragraph describes the ``Imports``
                /// section of the grammar.

                import
                    : 'import' NAME
                    ;

        .. tab-item:: Bison
            :sync: bison

            .. code-block:: bison

                %%

                /// **Module definition**
                ///
                /// This paragraph describes the ``Module definition``
                /// section of the grammar.

                module
                    : module moduleItem
                    | %empty
                    ;

                moduleItem
                    : import
                    | symbol
                    ;

                /// **Imports**
                ///
                /// This paragraph describes the ``Imports``
                /// section of the grammar.

                import
                    : "import" NAME
                    ;


Control comments
----------------

The list of control comments includes:

-   ``//@ doc:no-doc`` -- exclude this rule from ``autogrammar`` output.

-   ``//@ doc:name <str>`` -- set a human-readable name for this rule.

-   ``//@ doc:inline`` -- exclude this rule from ``autogrammar`` output; any
    automatically generated railroad diagram that uses this rule will
    include its contents instead of a single node.

    Useful for fragments and simple lexer rules.

-   ``//@ doc:content <content>`` -- turns token into a literal with the given
    content. The content must be an ANTLR lexer rule.

    This is useful for tokens that don't have known contents, such as ones
    defined in ANTLR's ``tokens`` section or with bison's ``%token`` option.

    **Example:**

    .. tab-set::
        :sync-group: syntax

        .. tab-item:: ANTLR
            :sync: antlr

            .. code-block:: antlr
                :force:

                tokens {
                    //@ doc:content [a-zA-Z_][a-zA-Z0-9_]*
                    //@ doc:inline
                    NAME
                }

                import
                    : 'import' NAME
                    ;

        .. tab-item:: Bison
            :sync: bison

            .. code-block:: bison

                //@ doc:content [a-zA-Z_][a-zA-Z0-9_]*
                //@ doc:inline
                %token NAME

                %%

                import
                    : "import" NAME
                    ;

    .. dropdown:: Example output

        With ``content`` option:

        .. syntax:rule:: NAME
            :no-index:

            .. syntax:lexer-diagram:: [a-zA-Z_][a-zA-Z0-9_]*

        .. syntax:rule:: import
            :no-index:

            .. syntax:lexer-diagram:: 'import' [a-zA-Z_][a-zA-Z0-9_]*

        Without ``content`` option:

        .. syntax:rule:: NAME
            :no-index:

        .. syntax:rule:: import
            :no-index:

            .. syntax:lexer-diagram:: 'import' NAME

-   ``//@ doc:no-diagram`` -- do not generate railroad diagram.

-   ``//@ doc:importance <int>`` -- controls the 'importance' of a rule.

    By default, all rules have importance of ``1``.

    Rules with importance of ``0`` will be rendered off the main line in optional
    groups. In alternative groups, rule with the highest importance will be centered.

    **Example:**

    .. syntax:lexer-diagram:: R1? R0?;

        //@ doc:name Rule with importance 0
        //@ doc:importance 0
        R0 : EOF;

        //@ doc:name Rule with importance 1
        //@ doc:importance 1
        R1 : EOF

    .. syntax:lexer-diagram:: (R0 | R1) (R2 | R1);

        //@ doc:name Rule with importance 0
        //@ doc:importance 0
        R0 : EOF;

        //@ doc:name Rule with importance 1
        //@ doc:importance 1
        R1 : EOF;

        //@ doc:name Rule with importance 2
        //@ doc:importance 2
        R2 : EOF

-   ``//@ doc:unimportant`` -- set importance to ``0``.

-   ``//@ doc:keep-diagram-recursive`` -- disable optimizations for recursion
    when rendering a diagram.

    By default, Sphinx Syntax will try to convert recursive rules into cyclic ones.
    This works good for normal left recursion, but might generate bad results
    when using Bison's precedence declarations.

    **Example:**

    .. tab-set::
        :sync-group: syntax

        .. tab-item:: ANTLR
            :sync: antlr

            .. code-block:: antlr

                //@ doc:keep-diagram-recursive
                expr
                    : NUMBER
                    | expr '*' expr
                    | expr '/' expr
                    | '-' expr
                    | '(' expr ')'

        .. tab-item:: Bison
            :sync: bison

            .. code-block:: bison

                %left '*' '/'
                %precedence NEG

                %%

                //@ doc:keep-diagram-recursive
                expr
                    : NUMBER
                    | expr '*' expr
                    | expr '/' expr
                    | '-' expr %prec NEG
                    | '(' expr ')'

    .. dropdown:: Example output

        With ``keep-diagram-recursive`` option:

        .. syntax:rule:: expr
            :no-index:

            .. syntax:parser-diagram::

                expr;

                //@ doc:keep-diagram-recursive
                //@ doc:inline
                expr
                    : NUMBER
                    | expr '*' expr
                    | expr '/' expr
                    | '-' expr
                    | '(' expr ')'

        Without ``keep-diagram-recursive`` option:

        .. syntax:rule:: expr
            :no-index:

            .. syntax:parser-diagram::

                expr;

                //@ doc:inline
                expr
                    : NUMBER
                    | expr '*' expr
                    | expr '/' expr
                    | '-' expr
                    | '(' expr ')'

-   ``//@ doc:css-class`` -- add a custom CSS class to all diagram nodes
    referencing this rule.

-   ``//@ %token <name>`` -- special syntax for declaring a token in Bison grammar
    without affecting the Bison itself.

    This is useful when you need to declare two tokens with the same precedence
    and document both of them separately.

    **Example:**

    .. code-block:: bison

        /** Documentation for ``*``. */
        //@ %token '*'

        /** Documentation for ``/``. */
        //@ %token '/'

        %left '*' '/'
