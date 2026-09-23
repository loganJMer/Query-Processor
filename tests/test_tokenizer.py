from source import tokenize

reqTests = [

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
    ],


    # =========================
    # 7.2 Grammar and precedence
    # =========================

    # 10
    [
        "A union B minus C",
        [
            "RELATION:A",
            "UNION:union",
            "RELATION:B",
            "MINUS:minus",
            "RELATION:C"
        ]
    ],

    # 11
    [
        "A minus B minus C",
        [
            "RELATION:A",
            "MINUS:minus",
            "RELATION:B",
            "MINUS:minus",
            "RELATION:C"
        ]
    ],

    # 12
    [
        "select[not (a=1 and b=2) or c>3](R)",
        [
            "SELECT:select",
            "LEFTS:[",
            "NOT:not",
            "LEFTP:(",
            "RELATION:a",
            "EQ:=",
            "NUM:1",
            "AND:and",
            "RELATION:b",
            "EQ:=",
            "NUM:2",
            "RIGHTP:)",
            "OR:or",
            "RELATION:c",
            "GT:>",
            "NUM:3",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
    ],

    # 13
    [
        "select[a=1 and b=2 or c=3](R)",
        [
            "SELECT:select",
            "LEFTS:[",
            "RELATION:a",
            "EQ:=",
            "NUM:1",
            "AND:and",
            "RELATION:b",
            "EQ:=",
            "NUM:2",
            "OR:or",
            "RELATION:c",
            "EQ:=",
            "NUM:3",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
    ],

    # 14
    [
        "project[Name](select[Age>30](select[DID='D1'](Employees)))",
        [
            "PROJECT:project",
            "LEFTS:[",
            "RELATION:Name",
            "RIGHTS:]",
            "LEFTP:(",

            "SELECT:select",
            "LEFTS:[",
            "RELATION:Age",
            "GT:>",
            "NUM:30",
            "RIGHTS:]",
            "LEFTP:(",

            "SELECT:select",
            "LEFTS:[",
            "RELATION:DID",
            "EQ:=",
            "STR:D1",
            "RIGHTS:]",
            "LEFTP:(",

            "RELATION:Employees",
            "RIGHTP:)",
            "RIGHTP:)",
            "RIGHTP:)"
        ]
    ],

    # 15
    [
        "(A union B) minus (C intersect D)",
        [
            "LEFTP:(",
            "RELATION:A",
            "UNION:union",
            "RELATION:B",
            "RIGHTP:)",
            "MINUS:minus",
            "LEFTP:(",
            "RELATION:C",
            "INTERSECT:intersect",
            "RELATION:D",
            "RIGHTP:)"
        ]
    ],

    # 16
    [
        "select[Age>30](R",
        [
            "SELECT:select",
            "LEFTS:[",
            "RELATION:Age",
            "GT:>",
            "NUM:30",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
        ]
    ],

    # 17
    [
        "project[](R)",
        [
            "PROJECT:project",
            "LEFTS:[",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)",
        ]
    ],


    # =========================
    # 7.3 Semantics
    # =========================

    # 18
    [
        "select[A=B](R)",
        [
            "SELECT:select",
            "LEFTS:[",
            "RELATION:A",
            "EQ:=",
            "RELATION:B",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
    ],

    # 19
    [
        "Emp join[Emp.DID=Dept.DID] Dept",
        [
            "RELATION:Emp",
            "JOIN:join",
            "LEFTS:[",
            "RELATION:Emp.DID",
            "EQ:=",
            "RELATION:Dept.DID",
            "RIGHTS:]",
            "RELATION:Dept"
        ]
    ],

    # 20
    [
        "rename[E2](Emp) join[Emp.MgrID=E2.EID] Emp",
        [
            "RENAME:rename",
            "LEFTS:[",
            "RELATION:E2",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:Emp",
            "RIGHTP:)",
            "JOIN:join",
            "LEFTS:[",
            "RELATION:Emp.MgrID",
            "EQ:=",
            "RELATION:E2.EID",
            "RIGHTS:]",
            "RELATION:Emp"
        ]
    ],

    # 21
    [
        "R union S",
        [
            "RELATION:R",
            "UNION:union",
            "RELATION:S"
        ]
    ],

    # 22
    [
        "select[Age>'30'](R)",
        [
            "SELECT:select",
            "LEFTS:[",
            "RELATION:Age",
            "GT:>",
            "STR:30",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
    ],

    # 23
    [
        "project[DID](Employees)",
        [
            "PROJECT:project",
            "LEFTS:[",
            "RELATION:DID",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:Employees",
            "RIGHTP:)"
        ]
    ],

    # 24
    [
        "project[Name, Name](R)",
        [
            "PROJECT:project",
            "LEFTS:[",
            "RELATION:Name",
            "COMMA:,",
            "RELATION:Name",
            "RIGHTS:]",
            "LEFTP:(",
            "RELATION:R",
            "RIGHTP:)"
        ]
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
        output = tokenize(query)
        success = expectedOutput == output
        if not success:
            failCount += 1
            print(f"Query: {query}\nOutput:          {output}\nExpected Output: {expectedOutput}\nFailure!\n")
        else:
            print(f"Query: {query}\nOutput: {output}\nSuccess!\n")
    return failCount


if __name__ == "__main__":
    main()