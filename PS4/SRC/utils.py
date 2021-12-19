import os
from Literal import Literal

def read_files(path):
    if not os.path.exists(path):
            return None
    with open(path) as f:
        try:
            return [line.strip() for line in f]
        finally:
            f.close()


def write_files(path, status, clauses_arr, kb):
    temp = kb.clauses[:]
    with open(path, 'w') as fs:
        for clauses in clauses_arr:
            check_duplicate_and_remove(clauses, temp)
            temp = temp + clauses

            fs.write("{}\n".format(len(clauses)))
            for clause in clauses:
                if clause == "{}":
                    fs.write("{}\n")
                else:
                    if len(clause) > 1:
                        fs.write("{}\n".format(' OR '.join(literal.to_string() for literal in clause)))
                    else:
                        fs.write("{}\n".format(clause[0].to_string()))
        fs.write("YES" if status else "NO")


def process_line(line):
    list_elem = line.split('OR')
    list_elem = [item.strip() for item in list_elem]
    return list_elem


def data_structuring(lines):
    clauses = []
    alpha = process_line(lines[0])
    n = int(lines[1])
    for i in range(2, 2 + n):
        clauses.append(process_line(lines[i]))
    return alpha, clauses


def sort(clause):
    if clause == '{}':
        return
    n = len(clause)
    for i in range(n):
        for j in range(i + 1, n):
            if clause[i].greater_than(clause[j]):
                clause[i], clause[j] = clause[j], clause[i]


def remove(literal, clause):
    return [item for item in clause if item != literal]


def check_complement(new_clause):
    pairs = [(new_clause[i], new_clause[j]) for i in range(len(new_clause))
             for j in range(i+1, len(new_clause))]
    for (clause_i, clause_j) in pairs:
        if clause_i == clause_j.negative():
            return False
    return True


def issubset(this, src):
    for item in this:
        if not include(src, item):
            return False
    return True


def same_clause(clause_i, clause_j):
    res = False
    if len(clause_i) == len(clause_j):
        for index in range(len(clause_i)):
            if clause_i[index] != clause_j[index]:
                return False
            else:
                res = True
    return res


def include(clauses, current_clause):
    if current_clause == '{}':
        return False
    for clause in clauses:
        if same_clause(current_clause, clause):
            return True
    return False


def check_duplicate_and_remove(this, src):
    i = 0
    while i < len(this):
        item = this[i]
        sort(item)
        if item == "{}":
            i += 1
            continue
        for j in range(len(src)):
            src_item = src[j]
            if same_clause(item, src_item):
                this.remove(this[i])
                i -= 1
        i += 1


def PL_Resolve(clause_i, clause_j):
    clauses = []
    for literal_i in clause_i:
        for literal_j in clause_j:
            if literal_i == literal_j.negative() or literal_j.negative() == literal_j:
                new_clause = list(set(remove(literal_i, clause_i) + remove(literal_j, clause_j)))
                if len(new_clause) == 0:
                    clauses.append('{}')
                else:
                    if check_complement(new_clause):
                        clauses.append(new_clause)

    return clauses



def PL_Resolution(kb, alpha):
    alpha = [Literal(item).negative() for item in alpha]
    for negative_alpha in alpha:
        kb.clauses.append([negative_alpha])

    clauses = kb.clauses[:]
    result_arr = []
    new = []
    temp = []

    while True:
        temp = []
        n = len(clauses)
        pairs = [(clauses[i], clauses[j])
                 for i in range(n) for j in range(i+1, n)]
        
        for (clause_i, clause_j) in pairs:
            resolvents = PL_Resolve(clause_i, clause_j)
            sort(resolvents)
            new = list(new) + list(resolvents)

            if '{}'in resolvents:
                for new_clause in new:
                    if not include(clauses, new_clause):
                        clauses.append(new_clause)
                        temp.append(new_clause)
                        
                result_arr.append(temp)
                return (True, result_arr)
        
        for new_clause in new:
            sort(new_clause)

        if issubset(new, clauses):
            result_arr.append([])
            return (False, result_arr)
        
        for new_clause in new:
            if not include(clauses, new_clause):
                clauses.append(new_clause)
                temp.append(new_clause)                
        result_arr.append(temp)