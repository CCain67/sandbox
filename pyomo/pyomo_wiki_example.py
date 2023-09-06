"""
This is the MIP example from Wikipedia, found here:
- https://en.wikipedia.org/wiki/Integer_programming#Example
"""

from pyomo.environ import (
    ConcreteModel,
    Var,
    Objective,
    Constraint,
    SolverFactory,
    maximize,
    PositiveIntegers,
)


# Create a concrete model
model = ConcreteModel()

# Declare variables
model.x = Var(domain=PositiveIntegers)
model.y = Var(domain=PositiveIntegers)

# Objective function
model.obj = Objective(
    expr=model.y,
    sense=maximize,
)

# Constraints
model.constraint1 = Constraint(rule=lambda model: -1 * model.x + model.y <= 1)
model.constraint2 = Constraint(rule=lambda model: 3 * model.x + 2 * model.y <= 12)
model.constraint3 = Constraint(rule=lambda model: 2 * model.x + 3 * model.y <= 12)

# Solve
solver = SolverFactory("glpk")
solver.solve(model)

# Display result
print(f"x = {model.x()}")
print(f"y = {model.y()}")
