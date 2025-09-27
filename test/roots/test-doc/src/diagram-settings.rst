Diagram settings
================

.. container:: regression

   .. syntax:diagram::
      :force-text:

      - Foo
      - Bar

   .. syntax:diagram::
      :force-text:
      :reverse:
      :end-class: simple
      :text-padding: 2 4 2 4
      :text-vertical-choice-separation: 2
      :text-vertical-seq-separation: 2
      :text-horizontal-seq-separation: 2
      :text-max-width: 50

      - Foo
      - Bar
      - Foo
      - Bar
      - Foo
      - Bar
      - Foo
      - Bar
      - Foo

   .. syntax:diagram::
      :force-text:
      :no-reverse:

      - Foo
      - Bar

   .. syntax:diagram::
      :svg-padding: 50 50 50 50
      :svg-arc-radius: 0

      - Foo
      - Bar

   .. syntax:diagram::
      :reverse:

      - Foo
      - Bar

   .. syntax:diagram::
      :no-reverse:

      - Foo
      - Bar

   .. syntax:lexer-diagram:: FOO_BAR 'Foo\nBar'
      :force-text:
      :cc-to-dash:

   .. syntax:lexer-diagram:: FOO_BAR 'Foo\nBar'
      :force-text:
      :literal-rendering: name

   .. syntax:lexer-diagram:: FOO_BAR 'Foo\nBar'
      :force-text:
      :literal-rendering: contents

   .. syntax:lexer-diagram:: FOO_BAR 'Foo\nBar'
      :force-text:
      :literal-rendering: contents-unquoted
