Diagrams
========

.. container:: regression

   .. syntax:diagram::

      - Foo
      - Bar

   .. syntax:diagram::
      :alt: Some title
      :align: right
      :class: custom-css-class
      :name: diagram-name

      - Foo
      - Bar

   .. syntax:diagram::
      :loading: link

      - Foo
      - Bar

   .. syntax:diagram::
      :loading: link
      :alt: Some title
      :align: right
      :class: custom-css-class
      :name: diagram-name-2

      - Foo
      - Bar

   .. syntax:diagram::

      - terminal: NodeWithLink
        href: "#anchor"
        title: "Go to anchor"

   .. syntax:lexer-diagram:: FOO_BAR 'FooBar'

   .. syntax:parser-diagram:: FooBar 'FooBar'
