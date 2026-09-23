import source

source.relations["Emp"] = [
    "Emp",
    ("EID", "MgrID", "DID", "Age"),
    ("E1", "E3", "D1", "30"),
    ("E2", "E1", "D2", "25"),
    ("E3", "E3", "D1", "35")
]

source.relations["Dept"] = [
    "Dept",
    ("DID", "Name"),
    ("D1", "Engineering"),
    ("D2", "History")
]

tokenTests = [

    # =========================
    # 7.1 Tokenizer
    # =========================

    # 1
    [
        "select[x1=3](R)",
        [
            "SELECT:select",
            "LEFTS:[",
            "RELATION:x1",
            "EQ:=",
            "NUM:3",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
    ],

    # 2
    [
        "select[ x1 = 3 ](R)",
        [
            "SELECT:select",
            "LEFTS:[",
            "RELATION:x1",
            "EQ:=",
            "NUM:3",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
    ],

    # 3
    [
        "select[Age>=30](R)",
        [
            "SELECT:select",
            "LEFTS:[",
            "RELATION:Age",
            "GTE:>=",
            "NUM:30",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
    ],

    # 4
    [
        "select[Age>-30](R)",
        [
            "SELECT:select",
            "LEFTS:[",
            "RELATION:Age",
            "GT:>",
            "NUM:-30",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
    ],

    # 5
    [
        "select[Name='Bob)'](R)",
        [
            "SELECT:select",
            "LEFTS:[",
            "RELATION:Name",
            "EQ:=",
            "STR:Bob)",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
    ],

    # 6
    [
        "select[Name='a,b'](R)",
        [
            "SELECT:select",
            "LEFTS:[",
            "RELATION:Name",
            "EQ:=",
            "STR:a,b",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
    ],

    # 7
    [
        "select[Name='O''Brien'](R)",
        [
            "SELECT:select",
            "LEFTS:[",
            "RELATION:Name",
            "EQ:=",
            "STR:O'Brien",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
    ],

    # 8
    [
        "select[union=3](R)",
        [
            "SELECT:select",
            "LEFTS:[",
            "RELATION:union",
            "EQ:=",
            "NUM:3",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
    ],

    # 9
    [
        "select[Name='Bob](R)",
        "Lexical Error: String 'Bob](R) was never closed. Starts at position 12"
    ]

]

parseTests = [
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

evalTests = [

    # =========================
    # 18 - attribute vs attribute
    # =========================

    [
        "select[EID=DID](Emp)",
        ['Emp', ('EID', 'MgrID', 'DID', 'Age')]
    ],

    # =========================
    # 19 - qualified join
    # =========================

    [
        "Emp join[Emp.DID=Dept.DID] Dept",
        [
            'Emp',
            ('Emp.EID', 'Emp.MgrID', 'Emp.DID', 'Emp.Age', 'Dept.DID', 'Dept.Name'),
            ('E1', 'E3', 'D1', '30', 'D1', 'Engineering'),
            ('E2', 'E1', 'D2', '25', 'D2', 'History'),
            ('E3', 'E3', 'D1', '35', 'D1', 'Engineering')
        ]
    ],

    # =========================
    # 20 - self join
    # =========================

    [
        "rename[E2](Emp) join[Emp.MgrID=E2.EID] Emp",
        [
            'E2',
            ('E2.EID', 'E2.MgrID', 'E2.DID', 'E2.Age',
            'Emp.EID', 'Emp.MgrID', 'Emp.DID', 'Emp.Age'),
            ('E1', 'E3', 'D1', '30', 'E2', 'E1', 'D2', '25'),
            ('E3', 'E3', 'D1', '35', 'E1', 'E3', 'D1', '30'),
            ('E3', 'E3', 'D1', '35', 'E3', 'E3', 'D1', '35')
        ]
    ],

    # =========================
    # 21 - incompatible schemas
    # =========================

    [
        "Emp union Dept",
        None
    ],

    # =========================
    # 22 - number vs string
    # =========================

    [
        "select[Age>'30'](Emp)",
        None
    ],

    # =========================
    # 23 - projection removes duplicates
    # =========================

    [
        "project[DID](Emp)",
        [
            "Emp",
            ("DID",),
            ("D1",),
            ("D2",)
        ]
    ],

    # =========================
    # 25 - query returning no tuples
    # =========================

    [
        "select[Age>100](Emp)",
        [
            "Emp",
            ("EID", "MgrID", "DID", "Age")
        ]
    ]
]


def main():
    failCount = 0

    print("Tokenizer test cases\n")
    failCount += runTokenTests(tokenTests)

    print("Parser test cases (Grammar and precedence)\n")
    failCount += runParseTests(parseTests)

    print("Evaluator test cases (Semantics)\n")
    failCount += runEvalTests(evalTests)

    print(f"Fail count: {failCount}")

def runTokenTests(tests: list[list]):
    failCount = 0
    for test in tests:
        query = test[0]
        expectedOutput = test[1]
        output = source.tokenize(query)
        success = expectedOutput == output
        if not success:
            failCount += 1
            print(f"Query: {query}\nOutput:          {output}\nExpected Output: {expectedOutput}\nFailure!\n")
        else:
            print(f"Query: {query}\nOutput: {output}\nSuccess!\n")
    return failCount

def runParseTests(tests: list[list]):
    failCount = 0

    for test in tests:
        query = test[0]
        expectedOutput = test[1]

        tokens = source.tokenize(query)
        if isinstance(tokens, str):
            output = tokens
        else:
            result = source.parse_expr(tokens)

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
            source.print_tree(output)
            print("\n")

    return failCount

def runEvalTests(tests: list[list]):
    failCount = 0

    for test in tests:
        query = test[0]
        expectedOutput = test[1]

        tokens = source.tokenize(query)

        if isinstance(tokens, str):
            output = tokens
        else:
            result = source.parse_expr(tokens)

            if result is None:
                output = None
            else:
                tree = result[0]
                output = source.evaluate_expr(tree)

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