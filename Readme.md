Griaß eich! 🐄 This solution to the [GenDev Challenge 2024](https://github.com/check24-scholarships/check24-best-combination-challenge) employs ✨Mixed Integer Programming.✨

### 🚀 Live Demo
Demo: [https://streaming-package-comperator.vercel.app/](https://streaming-package-comperator.vercel.app/)  
(Note: This is hosted on a free tier. The first query may take up to one minute because the backend is automatically deactivated when idle.)

### 💡 Main Idea
At the core of this application lies a mathematical model known as a Mixed Integer Program (MIP), which determines the optimal combination of streaming packages to minimize the cost of watching a given set of games. 📊

This mathematical model is solved using the PuLP solver in Python. 🐍

📽️ Watch this video (TODO) where I showcase the application and delve deeper into the theory and implementation.

### 🔧 Possible Future Improvements
**Frontend** 🖥️:  
  * 📋 Implement a table view where users can select specific games.  
  * 🏆 Add a tournament selection feature.  
  * 💰 Create a 'set maximum cost' option: Remove the worst deals iteratively until ```total_cost < maximum_cost```.

**Backend** 🛠️:  
  * 📂 Currently, each query accesses the CSV files as provided in the problem statement. Accessing the data through a merged CSV file or a database could significantly improve speed.  
  * 🔄 The backend processes the dataframe in multiple loops. Consolidating operations into fewer loops could enhance performance.  
  * ✂️ The pruning logic (removal of the worst deals) is currently implemented on the frontend. Moving this to the backend could further optimize performance.

**Theory/Math** 📐:  
  * ❓ After pruning, there is no guarantee that the model remains optimal. Implementing methods from [Sensitivity Analysis](https://ocw.ehu.eus/pluginfile.php/40934/mod_resource/content/1/4_Sensitivity.pdf) could help verify if re-solving is necessary.  
  * 📦 There are alternative ways to model this use case and related scenarios. For example, if users set a maximum monthly or yearly budget, it could be modeled as a [Cutting Stock Problem](https://en.wikipedia.org/wiki/Cutting_stock_problem).



## Local Setup
## BackEnd

0. **Have python and pip installed**

1. **Install the required dependencies**:

    ```sh
    cd backend
    pip install -r requirements.txt
    ```

2. **Run the Flask application**:
    ```sh
    python app.py
    ```

The backend should now be running on `http://127.0.0.1:5000`.

## FrontEnd
0. **Have node and npm installed**
1. **Rename `example.env` to `.env`**:

- Under Linux:
   ```sh
   cd frontend
   mv example.env .env
   ```
- Under Windows:
   ```sh
   cd frontend
   ren example.env .env
   ```
2. **Install dependencies**
   ```sh
   npm i
   ```
3. **Fire up this baby**
   ```sh
   npm run dev
   ```

The frontend should now be running on `http://localhost:5173/`.


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
