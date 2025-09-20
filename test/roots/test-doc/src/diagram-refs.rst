Diagram refs
============

.. container:: regression

   .. syntax:diagram::

      - ref-foo
      - ref-bar
      - ref-baz
      - some-rule
      - ref-target-in-other-file.some-rule
      - ref-target-in-other-file.some-other-rule
      - ~ref-target-in-other-file.some-rule

   .. syntax:grammar:: ref-qux

      .. syntax:rule:: duo

      .. syntax:diagram::

         - ref-qux
         - duo

Targets
-------

.. syntax:rule:: ref-foo

.. syntax:grammar:: ref-bar

.. syntax:rule:: ref-baz
   :name: Human readable Baz
