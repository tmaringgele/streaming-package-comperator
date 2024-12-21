### Mixed Integer Programming (MIP) Model

#### Decision Variables
1. \(x_i^{\text{month}} \in \mathbb{Z}_{\geq 0}\): Number of monthly subscriptions purchased for package \(i\).
2. \(x_i^{\text{year}} \in \mathbb{Z}_{\geq 0}\): Number of yearly subscriptions purchased for package \(i\).
3. \(z_{i,m} \in \{0, 1\}\): Binary variable, 1 if package \(i\) is active for month \(m\) due to a monthly subscription.
4. \(z_{i,y} \in \{0, 1\}\): Binary variable, 1 if package \(i\) is active for year \(y\) due to a yearly subscription.

---

#### Sets
1. \(P\): Set of all streaming packages.
2. \(G\): Set of all games.
3. \(M\): Set of all months in which games occur.
4. \(Y\): Set of all years in which games occur.
5. \(P_g\): Set of packages that can cover game \(g\).
6. \(P_m\): Set of packages that can cover games in month \(m\).
7. \(P_y\): Set of packages that can cover games in year \(y\).

---

#### Parameters
1. \(C_i^{\text{month}}\): Monthly price of package \(i\).
2. \(C_i^{\text{year}}\): Yearly price of package \(i\).
3. \(m(g)\): Month in which game \(g\) takes place.
4. \(y(g)\): Year in which game \(g\) takes place.

---

#### Objective Function
Minimize the total cost:
\[
\text{Minimize: } \sum_{i \in P} \left( C_i^{\text{month}} x_i^{\text{month}} + C_i^{\text{year}} x_i^{\text{year}} \right)
\]

---

#### Constraints
1. **Game Coverage**:
   \[
   \sum_{i \in P_g} \left( z_{i,m(g)} + z_{i,y(g)} \right) \geq 1 \quad \forall g \in G
   \]

2. **Monthly Subscriptions Activate Packages**:
   \[
   z_{i,m} \leq x_i^{\text{month}} \quad \forall i \in P, \forall m \in M
   \]

3. **Yearly Subscriptions Activate Packages**:
   \[
   z_{i,y} \leq x_i^{\text{year}} \quad \forall i \in P, \forall y \in Y
   \]

4. **Monthly Coverage**:
   \[
   \sum_{i \in P_m} z_{i,m} \geq 1 \quad \forall m \in M
   \]

5. **Yearly Coverage**:
   \[
   \sum_{i \in P_y} z_{i,y} \geq 1 \quad \forall y \in Y
   \]

6. **Multiple Subscriptions Allowed**:
   \[
   x_i^{\text{month}}, x_i^{\text{year}} \geq 0 \quad \forall i \in P
   \]

7. **Binary Activation Variables**:
   \[
   z_{i,m}, z_{i,y} \in \{0, 1\} \quad \forall i \in P, \forall m \in M, \forall y \in Y
   \]

---

#### Explanation
- **Objective Function**: Minimizes the total cost of purchasing monthly and yearly subscriptions for all selected packages.
- **Constraints**:
  - Games are covered by packages active in their respective months and years.
  - Monthly and yearly activations are linked to the respective number of subscriptions purchased.
  - Monthly and yearly packages can be purchased multiple times.

---

#### Solver Output
The solver will return:
1. **Number of Subscriptions**:
   - \(x_i^{\text{month}}\): Number of monthly subscriptions purchased for package \(i\).
   - \(x_i^{\text{year}}\): Number of yearly subscriptions purchased for package \(i\).
2. **Activation Details**:
   - \(z_{i,m}\): Indicates whether package \(i\) is active in month \(m\).
   - \(z_{i,y}\): Indicates whether package \(i\) is active in year \(y\).
3. **Total Cost**:
   - The minimized cost of the selected subscriptions.