





relations = {}






def create_relation(input: str):
    key = input[:input.find(" ")]
    input = input[input.find(" ") + 1:]
    col_names = input[input.find("(") + 1:input.find(")")].split(", ")
    relation = [tuple(col_names)]
    info = input[input.find("{") + 1:input.find("}") - 1].split("\n")
    for row in info:
        split_row = row.split()


def select(R: list[tuple[str]], condition: str):
    pass

def project(R: list[tuple[str]], cols: list[str]):
    pass

#Cartesian product
def times(R1: list[tuple[str]], R2: list[tuple[str]]):
    pass

#Theta inner join
def join(R1: list[tuple[str]], R2: list[tuple[str]], condition: str):
    pass

def union(R1: list[tuple[str]], R2: list[tuple[str]]):
    pass

def intersect(R1: list[tuple[str]], R2: list[tuple[str]]):
    pass

def minus(R1: list[tuple[str]], R2: list[tuple[str]]):
    pass

def rename(R1: list[tuple[str]], name: str):
    pass











































