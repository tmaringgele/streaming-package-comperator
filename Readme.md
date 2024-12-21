## Decision Variables
1. **`x_i^month`** (Integer): Number of monthly subscriptions purchased for package `i`.  
2. **`x_i^year`** (Integer): Number of yearly subscriptions purchased for package `i`.  
3. **`z_{i,m}`** (Binary): 1 if package `i` is active in month `m` due to a monthly subscription, 0 otherwise.  
4. **`z_{i,y}`** (Binary): 1 if package `i` is active in year `y` due to a yearly subscription, 0 otherwise.

---

## Sets
- **`P`**: Set of all streaming packages.  
- **`G`**: Set of all games.  
- **`M`**: Set of all months in which games occur.  
- **`Y`**: Set of all years in which games occur.  
- **`P_g`**: Set of packages that can cover game `g`.  
- **`P_m`**: Set of packages that can cover games in month `m`.  
- **`P_y`**: Set of packages that can cover games in year `y`.

---

## Parameters
- **`C_i^month`**: Monthly price of package `i`.  
- **`C_i^year`**: Yearly price of package `i`.  
- **`m(g)`**: Month in which game `g` takes place.  
- **`y(g)`**: Year in which game `g` takes place.

---

## Objective Function
Minimize the total cost:
\[
\text{Minimize: } \sum_{i \in P} \left( C_i^{\text{month}} x_i^{\text{month}} + C_i^{\text{year}} x_i^{\text{year}} \right)
\]

---

## Constraints
### 1. Game Coverage
Each game must be covered by at least one active package, either through a monthly or yearly subscription:
\[
\sum_{i \in P_g} \left( z_{i,m(g)} + z_{i,y(g)} \right) \geq 1 \quad \forall g \in G
\]

### 2. Monthly Subscriptions Activate Packages
A package can be active in a specific month `m` only if it is purchased for a monthly subscription:
\[
z_{i,m} \leq x_i^{\text{month}} \quad \forall i \in P, \forall m \in M
\]

### 3. Yearly Subscriptions Activate Packages
A package can be active in a specific year `y` only if it is purchased for a yearly subscription:
\[
z_{i,y} \leq x_i^{\text{year}} \quad \forall i \in P, \forall y \in Y
\]

### 4. Monthly Coverage
For each month `m`, all games in that month must be covered by at least one active package:
\[
\sum_{i \in P_m} z_{i,m} \geq 1 \quad \forall m \in M
\]

### 5. Yearly Coverage
For each year `y`, all games in that year must be covered by at least one active package:
\[
\sum_{i \in P_y} z_{i,y} \geq 1 \quad \forall y \in Y
\]

### 6. Multiple Subscriptions Allowed
Monthly and yearly subscriptions can be purchased multiple times:
\[
x_i^{\text{month}}, x_i^{\text{year}} \geq 0 \quad \forall i \in P
\]

### 7. Binary Activation Variables
The activation variables `z_{i,m}` and `z_{i,y}` are binary:
\[
z_{i,m}, z_{i,y} \in \{0, 1\} \quad \forall i \in P, \forall m \in M, \forall y \in Y
\]

---

## Solver Output
The solver will provide:
1. **Number of Subscriptions**:
   - `x_i^month`: Number of monthly subscriptions purchased for package `i`.
   - `x_i^year`: Number of yearly subscriptions purchased for package `i`.
2. **Activation Details**:
   - `z_{i,m}`: Indicates whether package `i` is active in month `m`.
   - `z_{i,y}`: Indicates whether package `i` is active in year `y`.
3. **Total Cost**:
   - The minimized cost of the selected subscriptions.
