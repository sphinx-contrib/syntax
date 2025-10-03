Root rule
=========

.. container:: regression

    .. syntax:grammar:: root-rule-1
        :root-rule: r1

        .. syntax:diagram:: c
            :force-text:

        .. syntax:rule:: r1

            .. syntax:diagram:: c
                :force-text:

        .. syntax:rule:: r2

            .. syntax:diagram:: s
                :force-text:

    .. syntax:grammar:: root-rule-2
        :root-rule: r1
        :diagram-end-class: simple

        .. syntax:diagram:: s
            :force-text:

        .. syntax:rule:: r1

            .. syntax:diagram:: c
                :force-text:

        .. syntax:rule:: r2

            .. syntax:diagram:: s
                :force-text:

    .. syntax:grammar:: root-rule-3
        :root-rule: r1
        :diagram-end-class: simple

        .. syntax:diagram:: s
            :force-text:

        .. syntax:rule:: r1

            .. syntax:diagram:: c
                :force-text:

        .. syntax:rule:: r2
            :diagram-end-class: complex

            .. syntax:diagram:: s
                :force-text:

    .. syntax:grammar:: root-rule-3
        :root-rule: r1
        :diagram-end-class: simple
        :no-mark-root-rule:

        .. syntax:diagram:: s
            :force-text:

        .. syntax:rule:: r1

            .. syntax:diagram:: s
                :force-text:

        .. syntax:rule:: r2
            :diagram-end-class: complex

            .. syntax:diagram:: c
                :force-text:
