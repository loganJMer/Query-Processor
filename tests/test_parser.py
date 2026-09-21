from source import tokenize, parse_expr


reqTests = [

    # =========================
    # 7.2 Grammar and precedence
    # =========================

    # 1
    [
        "A",
        ("RELATION", "A")
    ],

    # 2
    [
        "A union B",
        (
            "UNION",
            ("RELATION", "A"),
            ("RELATION", "B")
        )
    ],

    # 3
    [
        "A intersect B",
        (
            "INTERSECT",
            ("RELATION", "A"),
            ("RELATION", "B")
        )
    ],

    # 4
    [
        "A minus B",
        (
            "MINUS",
            ("RELATION", "A"),
            ("RELATION", "B")
        )
    ],

    # 5
    [
        "A times B",
        (
            "TIMES",
            ("RELATION", "A"),
            ("RELATION", "B")
        )
    ],

    # 6 - left associativity
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

    # 7 - left associativity
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

    # 8 - all low operators have same precedence
    [
        "A intersect B union C minus D",
        (
            "MINUS",
            (
                "UNION",
                (
                    "INTERSECT",
                    ("RELATION", "A"),
                    ("RELATION", "B")
                ),
                ("RELATION", "C")
            ),
            ("RELATION", "D")
        )
    ],

    # 9 - join has higher precedence
    [
        "A join[X=1] B union C",
        (
            "UNION",
            (
                "JOIN",
                ("RELATION", "A"),
                ("RELATION", "B"),
                (
                    "COMPARISON",
                    (
                        "EQ",
                        ("ATTRIBUTE", "X"),
                        ("INT", 1)
                    )
                )
            ),
            ("RELATION", "C")
        )
    ],

    # 10 - join binds to the right operand before union
    [
        "A union B join[X=1] C",
        (
            "UNION",
            ("RELATION", "A"),
            (
                "JOIN",
                ("RELATION", "B"),
                ("RELATION", "C"),
                (
                    "COMPARISON",
                    (
                        "EQ",
                        ("ATTRIBUTE", "X"),
                        ("INT", 1)
                    )
                )
            )
        )
    ],

    # 11 - multiple joins are left associative
    [
        "A join[X=1] B join[Y=2] C",
        (
            "JOIN",
            (
                "JOIN",
                ("RELATION", "A"),
                ("RELATION", "B"),
                (
                    "COMPARISON",
                    (
                        "EQ",
                        ("ATTRIBUTE", "X"),
                        ("INT", 1)
                    )
                )
            ),
            ("RELATION", "C"),
            (
                "COMPARISON",
                (
                    "EQ",
                    ("ATTRIBUTE", "Y"),
                    ("INT", 2)
                )
            )
        )
    ],

    # 12 - parentheses override precedence
    [
        "(A union B) minus C",
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

    # 13
    [
        "A union (B minus C)",
        (
            "UNION",
            ("RELATION", "A"),
            (
                "MINUS",
                ("RELATION", "B"),
                ("RELATION", "C")
            )
        )
    ],

    # 14
    [
        "(A union B) times (C intersect D)",
        (
            "TIMES",
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


    # =========================
    # Unary expressions
    # =========================

    # 15
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
                    ("INT", 30)
                )
            )
        )
    ],

    # 16
    [
        "project[Name](R)",
        (
            "PROJECT",
            ("RELATION", "R"),
            ("ATTRIBUTE_LIST", ["Name"])
        )
    ],

    # 17
    [
        "rename[E2](Emp)",
        (
            "RENAME",
            ("RELATION", "Emp"),
            ("STR", "E2")
        )
    ],

    # 18 - nested unary
    [
        "select[Age>30](select[DID='D1'](Employees))",
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
                    ("INT", 30)
                )
            )
        )
    ],

    # 19 - project over select
    [
        "project[Name](select[Age>30](R))",
        (
            "PROJECT",
            (
                "SELECT",
                ("RELATION", "R"),
                (
                    "COMPARISON",
                    (
                        "GT",
                        ("ATTRIBUTE", "Age"),
                        ("INT", 30)
                    )
                )
            ),
            ("ATTRIBUTE_LIST", ["Name"])
        )
    ],

    # 20 - unary expression containing binary expression
    [
        "select[Age>30](A union B)",
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
                    ("INT", 30)
                )
            )
        )
    ],

    # 21 - binary expression containing unary expression
    [
        "select[Age>30](A) union B",
        (
            "UNION",
            (
                "SELECT",
                ("RELATION", "A"),
                (
                    "COMPARISON",
                    (
                        "GT",
                        ("ATTRIBUTE", "Age"),
                        ("INT", 30)
                    )
                )
            ),
            ("RELATION", "B")
        )
    ],


    # =========================
    # Conditions
    # =========================

    # 22
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
                    ("INT", 1)
                )
            )
        )
    ],

    # 23 - qualified attributes
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

    # 24 - and has higher precedence than or
    [
        "A join[a=1 and b=2 or c=3] B",
        (
            "JOIN",
            ("RELATION", "A"),
            ("RELATION", "B"),
            (
                "OR",
                (
                    "AND",
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "a"),
                            ("INT", 1)
                        )
                    ),
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "b"),
                            ("INT", 2)
                        )
                    )
                ),
                (
                    "COMPARISON",
                    (
                        "EQ",
                        ("ATTRIBUTE", "c"),
                        ("INT", 3)
                    )
                )
            )
        )
    ],

    # 25 - not has higher precedence than and
    [
        "A join[not a=1 and b=2] B",
        (
            "JOIN",
            ("RELATION", "A"),
            ("RELATION", "B"),
            (
                "AND",
                (
                    "NOT",
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "a"),
                            ("INT", 1)
                        )
                    )
                ),
                (
                    "COMPARISON",
                    (
                        "EQ",
                        ("ATTRIBUTE", "b"),
                        ("INT", 2)
                    )
                )
            )
        )
    ],

    # 26 - not is right associative
    [
        "A join[not not a=1] B",
        (
            "JOIN",
            ("RELATION", "A"),
            ("RELATION", "B"),
            (
                "NOT",
                (
                    "NOT",
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "a"),
                            ("INT", 1)
                        )
                    )
                )
            )
        )
    ],

    # 27 - condition parentheses
    [
        "A join[(a=1 or b=2) and c=3] B",
        (
            "JOIN",
            ("RELATION", "A"),
            ("RELATION", "B"),
            (
                "AND",
                (
                    "OR",
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "a"),
                            ("INT", 1)
                        )
                    ),
                    (
                        "COMPARISON",
                        (
                            "EQ",
                            ("ATTRIBUTE", "b"),
                            ("INT", 2)
                        )
                    )
                ),
                (
                    "COMPARISON",
                    (
                        "EQ",
                        ("ATTRIBUTE", "c"),
                        ("INT", 3)
                    )
                )
            )
        )
    ],

    # 28 - strings
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

    # 29 - negative integer
    [
        "select[Age>-30](R)",
        (
            "SELECT",
            ("RELATION", "R"),
            (
                "COMPARISON",
                (
                    "GT",
                    ("ATTRIBUTE", "Age"),
                    ("INT", -30)
                )
            )
        )
    ],

    # 30 - projection list
    [
        "project[Name,DID](R)",
        (
            "PROJECT",
            ("RELATION", "R"),
            ("ATTRIBUTE_LIST", ["Name", "DID"])
        )
    ],

    # 31 - projection with spaces
    [
        "project[Name, DID](R)",
        (
            "PROJECT",
            ("RELATION", "R"),
            ("ATTRIBUTE_LIST", ["Name", "DID"])
        )
    ],

    # 32 - rename followed by join
    [
        "rename[E2](Emp) join[Emp.MgrID=E2.EID] Emp",
        (
            "JOIN",
            (
                "RENAME",
                ("RELATION", "Emp"),
                ("STR", "E2")
            ),
            ("RELATION", "Emp"),
            (
                "COMPARISON",
                (
                    "EQ",
                    ("ATTRIBUTE", "Emp.MgrID"),
                    ("ATTRIBUTE", "E2.EID")
                )
            )
        )
    ]
]


otherTests = []


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

    return failCount


if __name__ == "__main__":
    main()