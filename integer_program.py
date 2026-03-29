import pulp

#sets
S = ['s1', 's2', 's3']          # Students
P = ['p1', 'p2', 'p3']          # Projects
F = ['f1', 'f2']                # Professors

# Projects per professor
P_k = {
    'f1': ['p1', 'p2'],
    'f2': ['p3']
}

# Acceptable pairs (E)
E = [('s1','p1'), ('s1','p2'), ('s2','p2'), ('s3','p3')]


# Utility values w_sp
w = {
    ('s1','p1'): 10,
    ('s1','p2'): 8,
    ('s2','p2'): 9,
    ('s3','p3'): 7
}

# Professor capacities
C = {
    'f1': 2,
    'f2': 1
}


model = pulp.LpProblem("Student_Project_Matching", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", E, cat='Binary')
y = pulp.LpVariable.dicts("y", P, cat='Binary')

model += pulp.lpSum(w[(s,p)] * x[(s,p)] for (s,p) in E)


for s in S:
    model += pulp.lpSum(x[(s,p)] for (s,p) in E if s == s) == 1

for p in P:
    model += pulp.lpSum(x[(s,p)] for (s,p) in E if p == p) <= y[p]

for k in F:
    model += pulp.lpSum(y[p] for p in P_k[k]) <= C[k]

model.solve()

print("Status:", pulp.LpStatus[model.status])

for (s,p) in E:
    if pulp.value(x[(s,p)]) == 1:
        print(f"Student {s} assigned to Project {p}")

for p in P:
    if pulp.value(y[p]) == 1:
        print(f"Project {p} is selected")
