"""
A script which sets up and runs the MIP problem outlined in the README.md of this project.
"""

from pyomo.environ import (
    ConcreteModel,
    Var,
    Objective,
    Constraint,
    SolverFactory,
    minimize,
    Binary,
)

# Initialize data
N = 3  # Number of potential warehouse locations
M = 4  # Number of customers
F = [15000, 60000, 30000]  # Fixed costs for opening each warehouse
C = [2, 4, 3]  # Capacity of each warehouse
S = [
    [5000, 4000, 3000, 7000],
    [2000, 3000, 4000, 1000],
    [7000, 5000, 6000, 8000],
]  # Shipping costs from each warehouse to each customer

# Create a concrete model
model = ConcreteModel()

# Declare variables
model.x = Var(range(N), domain=Binary)  # x[i] = 1 if warehouse i is open, else 0
model.y = Var(
    range(N), range(M), domain=Binary
)  # y[i][j] = 1 if customer j is served by warehouse i, else 0

# Objective function
model.obj = Objective(
    expr=sum(F[i] * model.x[i] for i in range(N))
    + sum(S[i][j] * model.y[i, j] for i in range(N) for j in range(M)),
    sense=minimize,
)

# Constraints
# Every customer must be served by exactly one warehouse
model.customer_served = Constraint(
    range(M), rule=lambda model, j: sum(model.y[i, j] for i in range(N)) == 1
)

# A warehouse must be open to serve a customer
model.warehouse_open = Constraint(
    range(N), range(M), rule=lambda model, i, j: model.y[i, j] <= model.x[i]
)

# Capacity constraints
model.capacity = Constraint(
    range(N), rule=lambda model, i: sum(model.y[i, j] for j in range(M)) <= C[i]
)

# Create a solver and solve
solver = SolverFactory("glpk")
solver.solve(model)

# Display results
print("Objective value (Total Cost):", model.obj())

# Display which warehouses to open
for i in range(N):
    if model.x[i]() > 0:
        print(f"Open warehouse {i+1}")

# Display which customer is served by which warehouse
for j in range(M):
    for i in range(N):
        if model.y[i, j]() > 0:
            print(f"Customer {j+1} is served by warehouse {i+1}")
