# Pyomo Mixed Integer Programming Example

### 1. Setup 

This project utilizes a devcontainer, which runs on the `python:3.11-alpine` image found here:
- https://hub.docker.com/_/python/ 

The only notable requirement here is the package `glpk` (GNU Linear Programming Kit), found here:
- https://www.gnu.org/software/glpk/

### 2. Example from Wikipedia

I setup and ran the solver on Wikipedia's example found here:
- https://en.wikipedia.org/wiki/Integer_programming#Example

This is in `pyomo-wiki-example.py`. Running this script gives:
```python
x =  1.0
y =  2.0
```
which matches what Wikipedia has as a solution, so looks like I'm setting things up correctly, and we can move on to a more complex problem.

### 3. Example Problem

Consider a simplified warehouse location problem; a company wants to decide where to open warehouses to minimize total costs, incorporating both: 
- the costs of opening a warehouse, 
- and costs of shipping products to customers from the warehouses.

For this problem, we will instantiate a `ConreteModel()` in `pyomo`:
```python
model = ConcreteModel()
```
and add the components below to it. 

Note: the alternative to a `ConcreteModel()` is an `AbstractModel()` which according to the documentation, is empty (even if concrete components are attached to it) until `create_instance()` is called. 

#### Parameters
- There are $N$ potential warehouse locations and $M$ customers. In this example, we will use $N=3$, and $M=4$.
- Each warehouse location has a fixed cost $F_i$ for opening and a capacity $C_i$ for the number of customers it can reliably serve.
- The cost of shipping products from warehouse $i$ to customer $j$ is $S_{ij}$.
- Each customer must be served by exactly one warehouse.
  
#### Objective
Minimize the total cost, which is the sum of the fixed costs for opening warehouses and the shipping costs for serving all customers:
$$
\text{Minimize} \quad Z = \sum_{i=1}^{N} F_i x_i + \sum_{i=1}^{N} \sum_{j=1}^{M} S_{ij} y_{ij}
$$
The first summand is the sum of the fixed costs for opening each warehouse, and the second summand is the cost of shipping the products to the customers from each warehouse. This objective function is specified in `pyomo` via:
```python
model.obj = Objective(
    expr=sum(F[i] * model.x[i] for i in range(N)) + 
    sum(S[i][j] * model.y[i, j] for i in range(N) for j in range(M)),
    sense=minimize
    )
```

#### Decision Variables
- $x_i$ is a binary variable that is 1 if warehouse $i$ is open, and 0 otherwise.
- $y_{ij}$ is a binary variable that is 1 if customer $j$ is served by warehouse $i$, and 0 otherwise.

These binary variables can be specified in `pyomo` via:
```python
model.x = Var(range(N), domain=Binary)
model.y = Var(range(N), range(M), domain=Binary)
```


#### Constraints
1. Every customer must be served by exactly one warehouse: for example, for the second customer ($j=2$), only one $y_{i2}$ can be 1, the rest must be 0. As a constraint, this translates to: $$\sum_{i=1}^{N} y_{ij} = 1$$ for all (customers) $j$. In `pyomo`, we can declare this via:
```python
model.customer_served = Constraint(range(M), rule=lambda model, j: sum(model.y[i, j] for i in range(N)) == 1)
```
2. A warehouse must be open to serve a customer: as noted above, for each customer $j$, exactly one $y_{ij}$ will be 1, the rest will be 0. There are exactly 4(=2*2) cases that can occur here:
- warehouse $i$ is open ($x_i=1$), but customer $j$ is not served by it ($y_{ij}=0$),
- warehouse $i$ is open ($x_i=1$), and customer $j$ is served by it ($y_{ij}=1$),
- warehouse $i$ is not open ($x_i=0$), and customer $j$ is not served by it ($y_{ij}=0$),
- warehouse $i$ is not open ($x_i=0$), but customer $j$ is served by it ($y_{ij}=1$) (an impossibility!).

All possibilities but the last are OK, so our constraint here just ensures that the last possibility does not occur. This translates to $y_{ij} \leq x_i$ for all $i, j$, which in `pyomo` is declared via:
```python
model.warehouse_open = Constraint(range(N), range(M), rule=lambda model, i, j: model.y[i, j] <= model.x[i])
```
3. Capacity constraints: for each warehouse $i$, the number of customers served by the warehouse cannot exceed $C_i$, so this translates to $$\sum_{j=1}^{M} y_{ij} \leq C_i$$ for all $i$. In `pyomo`, we declare this via:
```python
model.capacity = Constraint(range(N), rule=lambda model, i: sum(model.y[i, j] for j in range(M)) <= C[i])
```

#### Solution

With the following data:
```python
N = 3  # Number of potential warehouse locations
M = 4  # Number of customers
F = [15000, 60000, 30000]  # Fixed costs for opening each warehouse
C = [2, 4, 3]  # Capacity of each warehouse
S = [
    [5000, 4000, 3000, 7000],
    [2000, 3000, 4000, 1000],
    [7000, 5000, 6000, 8000],
]  # Shipping costs from each warehouse to each customer
```
running the solver:
```python
solver = SolverFactory("glpk")
solver.solve(model)
```
and printing the solution gives:
```python
Objective value (Total Cost): 66000.0

Open warehouse 1
Open warehouse 3

Customer 1 is served by warehouse 1
Customer 2 is served by warehouse 3
Customer 3 is served by warehouse 1
Customer 4 is served by warehouse 3
```

