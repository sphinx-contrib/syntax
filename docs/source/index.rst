Sphinx Railroad Diagrams
========================

.. syntax:diagram::

    - optional:
      - "WITH"
      - optional: "RECURSIVE"
      - one_or_more:
        - non_terminal: "common-table-expression"
        repeat: ","
    - one_or_more:
      - choice:
        -
          - "SELECT"
          - choice:
            -
            - "DISTINCT"
            - "ALL"
          - one_or_more:
            - non_terminal: "result-column"
            repeat: ","
          - optional:
            - "FROM"
            - choice:
              - one_or_more:
                - non_terminal: "table-or-subquery"
                repeat: ","
              - non_terminal: "join-clause"
          - optional:
            - "WHERE"
            - non_terminal: "expr"
          - optional:
            - "GROUP"
            - "BY"
            - one_or_more:
              - non_terminal: "expr"
              repeat: ","
          - optional:
            - "HAVING"
            - non_terminal: "expr"
          - optional:
            - "WINDOW"
            - one_or_more:
              - non_terminal: "window-name"
              - "AS"
              - non_terminal: "window-defn"
              repeat: ","
        -
          - "VALUES"
          - one_or_more:
            - "("
            - one_or_more:
                non_terminal: "expr"
              repeat: ","
            - ")"
            repeat: ","
      repeat:
        non_terminal: "compound-operator"
    - optional:
      - "ORDER"
      - "BY"
      - one_or_more:
        - non_terminal: "ordering-term"
        repeat: ","
    - optional:
      - "LIMIT"
      - non_terminal: "expr"
      - choice:
        -
        -
          - "OFFSET"
          - non_terminal: "expr"
        -
          - ","
          - non_terminal: "expr"

.. toctree::
   :maxdepth: 2
   :caption: Contents:
