from source import tokenize, parse_expr, print_tree


reqTests = [

    # =========================
    # 7.2 Grammar and precedence
    # =========================

    # 10 - low operators are left associative
    [
        "A union B minus C",
        (
            "MINUS",
            (
                "UNION",
                ("RELATION", "A"),
                ("RELATION", "B")
            ),
            ("RELATION", "C")
        )
    ],

    # 11 - minus is left associative
    [
        "A minus B minus C",
        (
            "MINUS",
            (
                "MINUS",
                ("RELATION", "A"),
                ("RELATION", "B")
            ),
            ("RELATION", "C")
        )
    ],

    # 12 - not > and > or
    [
        "select[not (a=1 and b=2) or c>3](R)",
        (
            "SELECT",
            ("RELATION", "R"),
            (
                "OR",
                (
                    "NOT",
                    (
                        "AND",
                        (
                            "COMPARISON",
                            (
                                "EQ",
                                ("ATTRIBUTE", "a"),
                                ("NUM", 1)
                            )
                        ),
                        (
                            "COMPARISON",
                            (
                                "EQ",
                                ("ATTRIBUTE", "b"),
                                ("NUM", 2)
                            )
                        )
                    )
                ),
                (
                    "COMPARISON",
                    (
                        "GT",
                        ("ATTRIBUTE", "c"),
                        ("NUM", 3)
                    )
                )
            )
        )
    ],

    # 13 - and > or
    [
        "select[a=1 and b=2 or c=3](R)",
        (
            "SELECT",
            ("RELATION", "R"),
            (
                "OR",
                (
                    "AND",
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "a"),
                            ("NUM", 1)
                        )
                    ),
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "b"),
                            ("NUM", 2)
                        )
                    )
                ),
                (
                    "COMPARISON",
                    (
                        "EQ",
                        ("ATTRIBUTE", "c"),
                        ("NUM", 3)
                    )
                )
            )
        )
    ],

    # 14 - three levels of nesting
    [
        "project[Name](select[Age>30](select[DID='D1'](Employees)))",
        (
            "PROJECT",
            (
                "SELECT",
                (
                    "SELECT",
                    ("RELATION", "Employees"),
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "DID"),
                            ("STR", "D1")
                        )
                    )
                ),
                (
                    "COMPARISON",
                    (
                        "GT",
                        ("ATTRIBUTE", "Age"),
                        ("NUM", 30)
                    )
                )
            ),
            ("ATTRIBUTE_LIST", ["Name"])
        )
    ],

    # 15 - parentheses override precedence
    [
        "(A union B) minus (C intersect D)",
        (
            "MINUS",
            (
                "UNION",
                ("RELATION", "A"),
                ("RELATION", "B")
            ),
            (
                "INTERSECT",
                ("RELATION", "C"),
                ("RELATION", "D")
            )
        )
    ],

    # 16 - missing closing parenthesis
    [
        "select[Age>30](R",
        None
    ],

    # 17 - empty projection list
    [
        "project[](R)",
        None
    ]
]


otherTests = [

    # =========================
    # Basic expressions
    # =========================

    # Single relation
    [
        "Employees",
        ("RELATION", "Employees")
    ],

    # Each binary operator individually
    [
        "A intersect B",
        (
            "INTERSECT",
            ("RELATION", "A"),
            ("RELATION", "B")
        )
    ],

    [
        "A times B",
        (
            "TIMES",
            ("RELATION", "A"),
            ("RELATION", "B")
        )
    ],

    # All low-precedence operators mixed together
    [
        "A times B intersect C union D minus E",
        (
            "MINUS",
            (
                "UNION",
                (
                    "INTERSECT",
                    (
                        "TIMES",
                        ("RELATION", "A"),
                        ("RELATION", "B")
                    ),
                    ("RELATION", "C")
                ),
                ("RELATION", "D")
            ),
            ("RELATION", "E")
        )
    ],


    # =========================
    # Join
    # =========================

    # Basic join
    [
        "A join[X=1] B",
        (
            "JOIN",
            ("RELATION", "A"),
            ("RELATION", "B"),
            (
                "COMPARISON",
                (
                    "EQ",
                    ("ATTRIBUTE", "X"),
                    ("NUM", 1)
                )
            )
        )
    ],

    # Qualified attributes
    [
        "Emp join[Emp.DID=Dept.DID] Dept",
        (
            "JOIN",
            ("RELATION", "Emp"),
            ("RELATION", "Dept"),
            (
                "COMPARISON",
                (
                    "EQ",
                    ("ATTRIBUTE", "Emp.DID"),
                    ("ATTRIBUTE", "Dept.DID")
                )
            )
        )
    ],

    # Different comparison operators
    [
        "A join[X!=1] B",
        (
            "JOIN",
            ("RELATION", "A"),
            ("RELATION", "B"),
            (
                "COMPARISON",
                (
                    "NEQ",
                    ("ATTRIBUTE", "X"),
                    ("NUM", 1)
                )
            )
        )
    ],

    [
        "A join[X>=1] B",
        (
            "JOIN",
            ("RELATION", "A"),
            ("RELATION", "B"),
            (
                "COMPARISON",
                (
                    "GTE",
                    ("ATTRIBUTE", "X"),
                    ("NUM", 1)
                )
            )
        )
    ],

    [
        "A join[X<=1] B",
        (
            "JOIN",
            ("RELATION", "A"),
            ("RELATION", "B"),
            (
                "COMPARISON",
                (
                    "LTE",
                    ("ATTRIBUTE", "X"),
                    ("NUM", 1)
                )
            )
        )
    ],

    [
        "A join[X<1] B",
        (
            "JOIN",
            ("RELATION", "A"),
            ("RELATION", "B"),
            (
                "COMPARISON",
                (
                    "LT",
                    ("ATTRIBUTE", "X"),
                    ("NUM", 1)
                )
            )
        )
    ],


    # =========================
    # Unary operations
    # =========================

    # Basic select
    [
        "select[Age=30](R)",
        (
            "SELECT",
            ("RELATION", "R"),
            (
                "COMPARISON",
                (
                    "EQ",
                    ("ATTRIBUTE", "Age"),
                    ("NUM", 30)
                )
            )
        )
    ],

    # Basic project
    [
        "project[Name,DID](R)",
        (
            "PROJECT",
            ("RELATION", "R"),
            ("ATTRIBUTE_LIST", ["Name", "DID"])
        )
    ],

    # Spaces in attribute list
    [
        "project[Name, DID, Age](R)",
        (
            "PROJECT",
            ("RELATION", "R"),
            ("ATTRIBUTE_LIST", ["Name", "DID", "Age"])
        )
    ],

    # Basic rename
    [
        "rename[Employees2](Employees)",
        (
            "RENAME",
            ("RELATION", "Employees"),
            ("STR", "Employees2")
        )
    ],

    # Rename with underscore
    [
        "rename[Employee_2](Employees)",
        (
            "RENAME",
            ("RELATION", "Employees"),
            ("STR", "Employee_2")
        )
    ],


    # =========================
    # Values / operands
    # =========================

    # Negative integer
    [
        "select[Age=-10](R)",
        (
            "SELECT",
            ("RELATION", "R"),
            (
                "COMPARISON",
                (
                    "EQ",
                    ("ATTRIBUTE", "Age"),
                    ("NUM", -10)
                )
            )
        )
    ],

    # String comparison
    [
        "select[Name='Bob'](R)",
        (
            "SELECT",
            ("RELATION", "R"),
            (
                "COMPARISON",
                (
                    "EQ",
                    ("ATTRIBUTE", "Name"),
                    ("STR", "Bob")
                )
            )
        )
    ],

    # Apostrophe inside string
    [
        "select[Name='O''Brien'](R)",
        (
            "SELECT",
            ("RELATION", "R"),
            (
                "COMPARISON",
                (
                    "EQ",
                    ("ATTRIBUTE", "Name"),
                    ("STR", "O'Brien")
                )
            )
        )
    ],


    # =========================
    # Condition precedence
    # =========================

    # AND chain
    [
        "select[a=1 and b=2 and c=3](R)",
        (
            "SELECT",
            ("RELATION", "R"),
            (
                "AND",
                (
                    "AND",
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "a"),
                            ("NUM", 1)
                        )
                    ),
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "b"),
                            ("NUM", 2)
                        )
                    )
                ),
                (
                    "COMPARISON",
                    (
                        "EQ",
                        ("ATTRIBUTE", "c"),
                        ("NUM", 3)
                    )
                )
            )
        )
    ],

    # OR chain
    [
        "select[a=1 or b=2 or c=3](R)",
        (
            "SELECT",
            ("RELATION", "R"),
            (
                "OR",
                (
                    "OR",
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "a"),
                            ("NUM", 1)
                        )
                    ),
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "b"),
                            ("NUM", 2)
                        )
                    )
                ),
                (
                    "COMPARISON",
                    (
                        "EQ",
                        ("ATTRIBUTE", "c"),
                        ("NUM", 3)
                    )
                )
            )
        )
    ],

    # Multiple NOTs
    [
        "select[not not not a=1](R)",
        (
            "SELECT",
            ("RELATION", "R"),
            (
                "NOT",
                (
                    "NOT",
                    (
                        "NOT",
                        (
                            "COMPARISON",
                            (
                                "EQ",
                                ("ATTRIBUTE", "a"),
                                ("NUM", 1)
                            )
                        )
                    )
                )
            )
        )
    ],


    # =========================
    # Parentheses / nesting
    # =========================

    # Parentheses around entire expression
    [
        "(A)",
        ("RELATION", "A")
    ],

    # Nested binary expressions
    [
        "((A union B) minus C)",
        (
            "MINUS",
            (
                "UNION",
                ("RELATION", "A"),
                ("RELATION", "B")
            ),
            ("RELATION", "C")
        )
    ],

    # Unary around parenthesized expression
    [
        "select[Age>30]((A union B))",
        (
            "SELECT",
            (
                "UNION",
                ("RELATION", "A"),
                ("RELATION", "B")
            ),
            (
                "COMPARISON",
                (
                    "GT",
                    ("ATTRIBUTE", "Age"),
                    ("NUM", 30)
                )
            )
        )
    ],

    # Binary expression containing nested unary expressions
    [
        "select[a=1](A) union project[B](C)",
        (
            "UNION",
            (
                "SELECT",
                ("RELATION", "A"),
                (
                    "COMPARISON",
                    (
                        "EQ",
                        ("ATTRIBUTE", "a"),
                        ("NUM", 1)
                    )
                )
            ),
            (
                "PROJECT",
                ("RELATION", "C"),
                ("ATTRIBUTE_LIST", ["B"])
            )
        )
    ],


    # =========================
    # Syntax errors
    # =========================

    # Binary operator with no right operand
    [
        "A union",
        None
    ],

    # Missing expression after join condition
    [
        "A join[X=1]",
        None
    ],

    # Empty join condition
    [
        "A join[] B",
        None
    ],

    # Empty select condition
    [
        "select[](R)",
        None
    ],

    # Missing expression after unary operation
    [
        "select[a=1]",
        None
    ],

    # Missing closing parenthesis
    [
        "(A union B",
        None
    ],

    # Missing opening parenthesis for unary expression
    [
        "select[a=1]R",
        None
    ],

    # Empty relation name
    [
        "",
        None
    ]
]


def main():
    failCount = 0

    print("Required test cases\n")
    failCount += runTests(reqTests)

    print("Personal added cases\n")
    failCount += runTests(otherTests)

    print(f"Fail count: {failCount}")


def runTests(tests: list[list]):
    failCount = 0

    for test in tests:
        query = test[0]
        expectedOutput = test[1]

        tokens = tokenize(query)
        if isinstance(tokens, str):
            output = tokens
        else:
            result = parse_expr(tokens)

            if result is None:
                output = None
            else:
                output = result[0]

        success = expectedOutput == output

        if not success:
            failCount += 1
            print(
                f"Query: {query}\n"
                f"Output:          {output}\n"
                f"Expected Output: {expectedOutput}\n"
                f"Failure!\n"
            )
        else:
            print(
                f"Query: {query}\n"
                f"Output: {output}\n"
                f"Success!\n"
            )
            print_tree(output)

    return failCount


if __name__ == "__main__":
    main()