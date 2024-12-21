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
