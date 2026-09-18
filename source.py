





relations = {}






def create_relation(input: str):
    relation_name = input[:input.find(" ")]
    col_names = input[input.find("(") + 1:input.find(")")].split(", ")
    relation = [tuple(col_names)]
    info = input[input.find("{") + 1:input.find("}") - 1].split("\n")
    for row in info:
        row = row.strip()
        if row:
            split_row = row.split(", ")
            relation.append(tuple(split_row))
    relations[relation_name] = relation


def select(R: list[tuple[str]], condition: str):
    pass

def project(R: list[tuple[str]], cols: list[str]):
    indices = []
    projection = []
    for col in cols:
        indices.append(R[0].index(col))
        if indices[-1] == -1:
            print(f"Column {col} does not exist in relation {R}")
            return None
    for row in R:
        new_row = [row[i] for i in indices]
        projection.append(tuple(new_row))
    return projection
    

#Cartesian product
def times(R1: list[tuple[str]], R2: list[tuple[str]]):
    product = []
    titles = R1[0] + R2[0]
    product.append(titles)
    rows1, rows2 = R1[1:], R2[1:]
    for row1 in rows1:
        for row2 in rows2:
            product.append(row1+row2)
    return product


#Theta inner join
def join(R1: list[tuple[str]], R2: list[tuple[str]], condition: str):
    pass

def union(R1: list[tuple[str]], R2: list[tuple[str]]):
    if len(R1[0]) != len(R2[0]):
        print("Error: Relations must have same number of columns for union\n")
        return None
    R2_copy = R2.copy()
    union = []
    union.append(R1[0])
    for row1 in R1[1:]:
        union.append(row1)
        for row2 in R2_copy[1:]:
            if row1 == row2:
                R2_copy.remove(row2)
    for row in R2_copy[1:]:
        union.append(row)
    return union

def intersect(R1: list[tuple[str]], R2: list[tuple[str]]):
    if len(R1[0]) != len(R2[0]):
        print("Error: Relations must have same number of columns for union\n")
        return None
    intersect = []
    intersect.append(R1[0])
    for row1 in R1[1:]:
        for row2 in R2[1:]:
            if row1 == row2:
                intersect.append(row1)
    return intersect

def minus(R1: list[tuple[str]], R2: list[tuple[str]]):
    if len(R1[0]) != len(R2[0]):
        print("Error: Relations must have same number of columns for union\n")
        return None
    minus = []
    minus.append(R1[0])
    for row1 in R1[1:]:
        skip = False
        for row2 in R2[1:]:
            if row1 == row2:
                skip = True
                break
        if skip:
            continue
        minus.append(row1)
    return minus

def rename(R1: str, name: str):
    if not relations.get(R1):
        print(f"Relation {R1} does not exist")
        return None
    relations[name] = relations[R1]
    del relations[R1]

def print_table(R: list[tuple[str]]):
    widths = [
        max(len(str(row[i])) for row in R)
        for i in range(len(R[0]))
    ]

    for row in R:
        print(" | ".join(
            str(value).ljust(widths[i])
            for i, value in enumerate(row)
        ))

        if row == R[0]:
            print("-+-".join("-" * width for width in widths))
    print("\n")




def tokenize(query: str):
    tokens = []
    position = 0
    failure = False

    while(position < len(query)):
        c = query[position]
        c2 = query[position + 1] if position + 1 < len(query) else None
        #First ascertain what type of token is next
        #Skip whitespace
        if c == ' ':
            position += 1
            continue
        #Check if string
        if c == "'":
            token, position = tokenize_str(query, position + 1)
            if not token:
                failure = True
                break
            tokens.append(f"STR:{token}")
            continue

        #Check if comparison operator
        if c in ["!", "=", "<", ">"]:
            if c == "!":
                if not c2 or c2 != "=":
                    print("Invalid != operator. ! must be followed by =")
                    failure = True
                    break
                tokens.append("NE:!=")
                position += 2
                continue
            if c == "<":
                if c2 and c2 == "=":
                    tokens.append("LTE:<=")
                    position += 2
                    continue
                else:
                    tokens.append("LT:<")
                    position += 1
                    continue
            if c == ">":
                if c2 and c2 == "=":
                    tokens.append("GTE:>=")
                    position += 2
                    continue
                else:
                    tokens.append("GT:>")
                    position += 1
                    continue
            if c == "=":
                tokens.append("IS:=")
                position += 1
                continue
    
        #Check if boolean operator
        if c in ["a", "o", "n"]:
            if c == "a":
                if position + 2 < len(query):
                    if query[position:position + 3] == "and":
                        tokens.append("AND:and")
                        position += 3
                        continue
            if c == "o":
                if c2 and c2 == "r":
                    tokens.append("OR:or")
                    position += 2
                    continue
            if c == "n":
                if position + 2 < len(query):
                    if query[position:position + 3] == "not":
                        tokens.append("NOT:not")
                        position += 3
                        continue

        brackets = {"(":"P1O:(", ")":"P1C:)", "[":"P2O:[", "]":"P2C:]", "{":"P3O:{", "}":"P3C:}"}
        #Check if bracket
        if c in ["(", ")", "[", "]", "{", "}"]:
            tokens.append(brackets.get(c))
            position += 1
            continue

        #Check if unary op/join
        if c in ["s", "r", "p", "j"]:
            if c == "s":
                if position + 6 < len(query):
                    if query[position:position + 7] == "select[":
                        tokens.append("SELECT:select")
                        position += 6
                        continue
            if c == "r":
                if position + 6 < len(query):
                    if query[position:position + 7] == "rename[":
                        tokens.append("RENAME:rename")
                        position += 6
                        continue
            if c == "p":
                if position + 7 < len(query):
                    if query[position:position + 8] == "project[":
                        tokens.append("PROJECT:project")
                        position += 7
                        continue
            if c == "j":
                if position + 4 < len(query):
                    if query[position:position + 5] == "join[":
                        tokens.append("JOIN:join")
                        position += 4
                        continue

        #Check if binary op except join
        if c in ["t", "u", "i", "m"]:
            if c == "t":
                if position + 5 < len(query):
                    if query[position - 1:position + 6] == " times ":
                        tokens.append("TIMES:times")
                        position += 5
                        continue
            if c == "u":
                if position + 5 < len(query):
                    if query[position - 1:position + 6] == " union ":
                        tokens.append("UNION:union")
                        position += 5
                        continue
            if c == "i":
                if position + 9 < len(query):
                    if query[position - 1:position + 10] == " intersect ":
                        tokens.append("INTERSECT:intersect")
                        position += 9
                        continue
            if c == "m":
                if position + 5 < len(query):
                    if query[position - 1:position + 6] == " minus ":
                        tokens.append("MINUS:minus")
                        position += 5
                        continue

        if c.isnumeric():
            token, position = tokenize_int(query, position)
            tokens.append(f"INT:{token}")
            continue

        

def tokenize_str(query: str, position: int):
    string = ""
    finished = False
    while(position < len(query)):
        c = query[position]
        if c != "'":
            string += c
            position += 1
            continue
        if position + 1 != len(query) and query[position + 1] == "'":
            string += c
            position += 2
            continue
        finished = True
        break
    if not finished:
        print(f"String {string} was never closed")
        return None, -1
    return string, position + 1

def tokenize_int(query: str, position: int):
    string = ""
    while(position < len(query)):
        c = query[position]
        if c.isnumeric():
            string += c
            position += 1
            continue
        break
    return string, position

def main():
    rel1 = """Employees (EID, Name, Age, DID) = {
    E1, John, 32, D1
    E2, Alice, 28, D2
    E3, Bob, 29, D3
    E4, Janice, 30, D2
    }"""
    rel2 = """Departments (DID, Name, Budget) = {
    D1, Finance, 20000
    D2, Sales, 30000
    D3, HR, 25000
    D4, IT, 15000
    }"""
    rel3 = """Employees2 (EID, Name, Age, DID) = {
    E2, Alice, 28, D2
    E4, Janice, 30, D2
    E5, John, 32, D1
    E6, David, 47, D4
    }"""
    create_relation(rel1)
    create_relation(rel2)
    create_relation(rel3)
    print_table(relations["Employees"])
    print_table(relations["Departments"])
    print_table(relations["Employees2"])
    print_table(project(relations["Departments"], ["DID"]))
    print_table(project(relations["Employees"], ["EID", "Age"]))
    print_table(times(relations["Employees"], relations["Departments"]))
    print_table(union(relations["Employees"], relations["Employees2"]))
    print_table(intersect(relations["Employees"], relations["Employees2"]))
    print_table(minus(relations["Employees"], relations["Employees2"]))
    print_table(minus(relations["Employees2"], relations["Employees"]))


if __name__ == "__main__":
    main()