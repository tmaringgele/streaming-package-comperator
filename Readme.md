Griaß eich! 🐄 This solution to the [GenDev Challenge 2024](https://github.com/check24-scholarships/check24-best-combination-challenge) employs ✨Mixed Integer Programming.✨

### 🚀 Live Demo
Demo: [https://streaming-package-comperator.vercel.app/](https://streaming-package-comperator.vercel.app/)  
(Note: This is hosted on a free tier. The first query may take up to one minute because the backend is automatically deactivated when idle.)

### 💡 Main Idea
At the core of this application lies a mathematical model known as a Mixed Integer Program (MIP), which determines the optimal combination of streaming packages to minimize the cost of watching a given set of games. 📊

This mathematical model is solved using the PuLP solver in Python. 🐍

📽️ Watch this video (TODO) where I showcase the application and delve deeper into the theory and implementation.

📚 For those who want to dive deeper into the mathematical details, see the `explanation_for_nerds.ipynb` file, which provides a detailed explanation of the underlying math.  

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
  * ⚡ Use a more advanced solver like [Gurobi](https://www.gurobi.com/) or [CPLEX](https://www.ibm.com/analytics/cplex-optimizer) for faster and more efficient performance, especially for larger queries or more complex constraints.

## 🛠️ Local Setup

### 🔙 Backend
0. **Ensure Python and pip are installed** 🐍.

1. **Install the required dependencies**:
    ```sh
    cd backend
    pip install -r requirements.txt
    ```

2. **Run the Flask application** 🚀:
    ```sh
    python app.py
    ```

The backend should now be running on `http://127.0.0.1:5000`.

---

### 🌐 Frontend
0. **Ensure Node.js and npm are installed** 🌳.

1. **Rename `example.env` to `.env`**:

   - **Linux/macOS** 🐧:
     ```sh
     cd frontend
     mv example.env .env
     ```

   - **Windows** 🪟:
     ```sh
     cd frontend
     ren example.env .env
     ```

2. **Install the required dependencies**:
    ```sh
    npm i
    ```

3. **Start the development server** 🔥:
    ```sh
    npm run dev
    ```

The frontend should now be running on `http://localhost:5173/`.
