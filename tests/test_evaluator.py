import source

# ============================================================
# Test source.relations
# ============================================================

source.relations.clear()

source.relations["A"] = [
    "A",
    ("X",),
    (1,),
    (2,),
    (3,)
]

source.relations["B"] = [
    "B",
    ("X",),
    (2,),
    (3,),
    (4,)
]

source.relations["C"] = [
    "C",
    ("X",),
    (3,),
    (4,),
    (5,)
]

source.relations["D"] = [
    "D",
    ("Y",),
    (10,),
    (20,)
]

source.relations["Employees"] = [
    "Employees",
    ("EID", "Name", "Age", "DID"),
    ("E1", "John", 32, "D1"),
    ("E2", "Alice", 28, "D2"),
    ("E3", "Bob", 29, "D1"),
    ("E4", "John", 35, "D2")
]

source.relations["Departments"] = [
    "Departments",
    ("DID", "DeptName"),
    ("D1", "Engineering"),
    ("D2", "History")
]

source.relations["Managers"] = [
    "Managers",
    ("EID", "MgrID"),
    ("E1", "E3"),
    ("E2", "E1"),
    ("E3", "E3")
]

source.relations["Emp"] = [
    "Emp",
    ("EID", "MgrID", "DID"),
    ("E1", "E3", "D1"),
    ("E2", "E1", "D2"),
    ("E3", "E3", "D1")
]

source.relations["Dept"] = [
    "Dept",
    ("DID", "Name"),
    ("D1", "Engineering"),
    ("D2", "History")
]


# ============================================================
# Required tests
# ============================================================

reqTests = [

    # =========================
    # 18 - attribute vs attribute
    # =========================

    [
        "select[A=B](R)",
        None
    ],

    # =========================
    # 19 - qualified join
    # =========================

    [
        "Emp join[Emp.DID=Dept.DID] Dept",
        [
            'Emp',
            ('Emp.EID', 'Emp.MgrID', 'Emp.DID', 'Dept.DID', 'Dept.Name'),
            ('E1', 'E3', 'D1', 'D1', 'Engineering'),
            ('E2', 'E1', 'D2', 'D2', 'History'),
            ('E3', 'E3', 'D1', 'D1', 'Engineering')
        ]
    ],

    # =========================
    # 20 - self join
    # =========================

    [
        "rename[E2](Emp) join[Emp.MgrID=E2.EID] Emp",
        [
            'E2',
            ('E2.EID', 'E2.MgrID', 'E2.DID',
            'Emp.EID', 'Emp.MgrID', 'Emp.DID'),
            ('E1', 'E3', 'D1', 'E2', 'E1', 'D2'),
            ('E3', 'E3', 'D1', 'E1', 'E3', 'D1'),
            ('E3', 'E3', 'D1', 'E3', 'E3', 'D1')
        ]
    ],

    # =========================
    # 21 - incompatible schemas
    # =========================

    [
        "A union D",
        None
    ],

    # =========================
    # 22 - number vs string
    # =========================

    [
        "select[Age>'30'](Employees)",
        None
    ],

    # =========================
    # 23 - projection removes duplicates
    # =========================

    [
        "project[DID](Employees)",
        [
            "Employees",
            ("DID",),
            ("D1",),
            ("D2",)
        ]
    ],

    # =========================
    # 25 - query returning no tuples
    # =========================

    [
        "select[Age>100](Employees)",
        [
            "Employees",
            ("EID", "Name", "Age", "DID")
        ]
    ]
]


# ============================================================
# Extra tests
# ============================================================

otherTests = [

    # =========================
    # Basic relation lookup
    # =========================

    [
        "A",
        [
            "A",
            ("X",),
            (1,),
            (2,),
            (3,)
        ]
    ],

    # =========================
    # SELECT
    # =========================

    [
        "select[X=2](A)",
        [
            "A",
            ("X",),
            (2,)
        ]
    ],

    [
        "select[X>1](A)",
        [
            "A",
            ("X",),
            (2,),
            (3,)
        ]
    ],

    [
        "select[X>=2](A)",
        [
            "A",
            ("X",),
            (2,),
            (3,)
        ]
    ],

    [
        "select[X<3](A)",
        [
            "A",
            ("X",),
            (1,),
            (2,)
        ]
    ],

    [
        "select[X<=2](A)",
        [
            "A",
            ("X",),
            (1,),
            (2,)
        ]
    ],

    [
        "select[X!=2](A)",
        [
            "A",
            ("X",),
            (1,),
            (3,)
        ]
    ],

    # =========================
    # SELECT attribute vs attribute
    # =========================

    [
        "select[Age=Age](Employees)",
        [
            "Employees",
            ("EID", "Name", "Age", "DID"),
            ("E1", "John", 32, "D1"),
            ("E2", "Alice", 28, "D2"),
            ("E3", "Bob", 29, "D1"),
            ("E4", "John", 35, "D2")
        ]
    ],

    # =========================
    # SELECT string
    # =========================

    [
        "select[Name='John'](Employees)",
        [
            "Employees",
            ("EID", "Name", "Age", "DID"),
            ("E1", "John", 32, "D1"),
            ("E4", "John", 35, "D2")
        ]
    ],

    # =========================
    # SELECT AND / OR
    # =========================

    [
        "select[Age>30 and DID='D2'](Employees)",
        [
            "Employees",
            ("EID", "Name", "Age", "DID"),
            ("E4", "John", 35, "D2")
        ]
    ],

    [
        "select[Age<30 or DID='D2'](Employees)",
        [
            "Employees",
            ("EID", "Name", "Age", "DID"),
            ("E2", "Alice", 28, "D2"),
            ("E3", "Bob", 29, "D1"),
            ("E4", "John", 35, "D2")
        ]
    ],

    # =========================
    # SELECT NOT
    # =========================

    [
        "select[not Age>30](Employees)",
        [
            "Employees",
            ("EID", "Name", "Age", "DID"),
            ("E2", "Alice", 28, "D2"),
            ("E3", "Bob", 29, "D1")
        ]
    ],

    # =========================
    # PROJECT
    # =========================

    [
        "project[Name](Employees)",
        [
            "Employees",
            ("Name",),
            ("John",),
            ("Alice",),
            ("Bob",)
        ]
    ],

    [
        "project[Name,Age](Employees)",
        [
            "Employees",
            ("Name", "Age"),
            ("John", 32),
            ("Alice", 28),
            ("Bob", 29),
            ("John", 35)
        ]
    ],

    # Projection with reordered attributes
    [
        "project[DID,Name](Employees)",
        [
            "Employees",
            ("DID", "Name"),
            ("D1", "John"),
            ("D2", "Alice"),
            ("D1", "Bob"),
            ("D2", "John")
        ]
    ],

    # =========================
    # UNION
    # =========================

    [
        "A union B",
        [
            "A",
            ("X",),
            (1,),
            (2,),
            (3,),
            (4,)
        ]
    ],

    # UNION should remove duplicates
    [
        "B union C",
        [
            "B",
            ("X",),
            (2,),
            (3,),
            (4,),
            (5,)
        ]
    ],

    # =========================
    # INTERSECT
    # =========================

    [
        "A intersect B",
        [
            "A",
            ("X",),
            (2,),
            (3,)
        ]
    ],

    [
        "B intersect C",
        [
            "B",
            ("X",),
            (3,),
            (4,)
        ]
    ],

    # =========================
    # MINUS
    # =========================

    [
        "A minus B",
        [
            "A",
            ("X",),
            (1,)
        ]
    ],

    [
        "B minus A",
        [
            "B",
            ("X",),
            (4,)
        ]
    ],

    # =========================
    # TIMES
    # =========================

    [
        "A times D",
        [
            "A",
            ("A.X", "D.Y"),
            (1, 10),
            (1, 20),
            (2, 10),
            (2, 20),
            (3, 10),
            (3, 20)
        ]
    ],

    # =========================
    # JOIN
    # =========================

    [
        "A join[A.X=B.X] B",
        [
            "A",
            ("A.X", "B.X"),
            (2, 2),
            (3, 3)
        ]
    ],

    # Join with a non-equality condition
    [
        "A join[A.X<B.X] B",
        [
            "A",
            ("A.X", "B.X"),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 3),
            (2, 4),
            (3, 4)
        ]
    ],

    # =========================
    # Realistic department join
    # =========================

    [
        "Employees join[Employees.DID=Departments.DID] Departments",
        [
            "Employees",
            (
                "Employees.EID",
                "Employees.Name",
                "Employees.Age",
                "Employees.DID",
                "Departments.DID",
                "Departments.DeptName"
            ),
            (
                "E1",
                "John",
                32,
                "D1",
                "D1",
                "Engineering"
            ),
            (
                "E2",
                "Alice",
                28,
                "D2",
                "D2",
                "History"
            ),
            (
                "E3",
                "Bob",
                29,
                "D1",
                "D1",
                "Engineering"
            ),
            (
                "E4",
                "John",
                35,
                "D2",
                "D2",
                "History"
            )
        ]
    ],

    # =========================
    # RENAME
    # =========================

    [
        "rename[E2](Employees)",
        [
            "E2",
            ("EID", "Name", "Age", "DID"),
            ("E1", "John", 32, "D1"),
            ("E2", "Alice", 28, "D2"),
            ("E3", "Bob", 29, "D1"),
            ("E4", "John", 35, "D2")
        ]
    ],

    # =========================
    # Self join
    # =========================

    [
        "rename[E2](Managers) join[Managers.MgrID=E2.EID] Managers",
        [
            'E2',
            ('E2.EID', 'E2.MgrID', 'Managers.EID', 'Managers.MgrID'),
            ('E1', 'E3', 'E2', 'E1'),
            ('E3', 'E3', 'E1', 'E3'),
            ('E3', 'E3', 'E3', 'E3')
        ]
    ],

    # =========================
    # Nested operations
    # =========================

    [
        "project[Name](select[Age>30](Employees))",
        [
            "Employees",
            ("Name",),
            ("John",)
        ]
    ],

    [
        "select[X>1](A union B)",
        [
            "A",
            ("X",),
            (2,),
            (3,),
            (4,)
        ]
    ],

    [
        "project[X](A intersect B)",
        [
            "A",
            ("X",),
            (2,),
            (3,)
        ]
    ],

    # =========================
    # Precedence / evaluation
    # =========================

    [
        "A union B minus C",
        [
            "A",
            ("X",),
            (1,),
            (2,)
        ]
    ],

    [
        "A minus B minus C",
        [
            "A",
            ("X",),
            (1,)
        ]
    ],

    [
        "(A union B) minus (C intersect B)",
        [
            "A",
            ("X",),
            (1,),
            (2,)
        ]
    ],

    # =========================
    # Empty results
    # =========================

    [
        "select[X>100](A)",
        [
            "A",
            ("X",)
        ]
    ],

    [
        "A intersect C",
        [
            "A",
            ("X",),
            (3,)
        ]
    ],

    [
        "A minus A",
        [
            "A",
            ("X",)
        ]
    ]
]


def main():
    failCount = 0

    print("Required evaluator test cases\n")
    failCount += runTests(reqTests)

    print("Personal added evaluator cases\n")
    failCount += runTests(otherTests)

    print(f"Fail count: {failCount}")


def runTests(tests: list[list]):
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