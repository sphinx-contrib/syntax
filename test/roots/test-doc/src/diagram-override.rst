Diagram override
================

.. container:: regression

   .. syntax:grammar:: override-g
      :diagram-reverse:
      :diagram-end-class: simple

      .. syntax:diagram::
         :force-text:

         - A
         - B

      .. syntax:diagram::
         :force-text:
         :no-reverse:

         - A
         - B

      .. syntax:rule:: override-r
         :diagram-end-class: complex

         .. syntax:diagram::
            :force-text:

            - A
            - B

   .. syntax:diagram::
      :force-text:

      - A
      - B
