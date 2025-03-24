Now I want to create a loop system which should use the following scripts
 first script : Code Functionalities Explained as Points
Load ML Model:

The script loads a pre-trained XGBoost model (xgboost_green_model.pkl) for predicting green light durations based on traffic data.
Connect to SUMO Simulation:

Starts the SUMO simulation with a specified configuration file (simulation.sumocfg) using traci.start().
Define Detectors:

Maps lane detectors (e.g., detector_west_8) to corresponding traffic light phases (e.g., westbound, southbound).
Traffic Light ID:

Specifies the traffic light to control (traffic_light_id).
Initialize Data Logging:

Creates a DataFrame to store real-time traffic metrics and predictions, including vehicle counts, speeds, occupancy, and green/red light durations.
Simulate Traffic:

Runs a loop until the simulation ends:
Step 1: Collect real-time traffic data from lane detectors (e.g., vehicles seen, mean speed, occupancy).
Step 2: Calculate traffic density for each lane as a sum of vehicles seen and occupancy.
Determine Lane Priority:

Identifies the lane with the highest traffic density.
If the calculated phase index is invalid, defaults to phase 0.
Collect Features for Prediction:

Gathers traffic metrics (e.g., vehicles entered, seen, speed) for the highest-density lane to prepare features for the model.
Predict and Apply Green Light Duration:

Uses the ML model to predict the green light duration for the highest-density lane.
Ensures minimum green and red durations (10 seconds each).
Adjusts the traffic light's phase and duration dynamically.
Log Data:

Logs real-time traffic metrics, predicted durations, and the applied phase into the data_log DataFrame.
Introduce Speed Limits:

Dynamically adjusts the speed limit for all lanes to simulate slower vehicle speeds (10.0 m/s).
Simulation Step:

Advances the simulation step-by-step while handling potential FatalTraCIError exceptions.
Save Results:

At the end of the simulation, saves the logged data to a CSV file (traffic_data_log.csv) for analysis.
Exception Handling:

Gracefully handles simulation errors to ensure smooth execution.
Purpose:

Optimizes traffic flow by dynamically adjusting green light durations and simulating congestion using real-time traffic data and ML predictions.


second script : which should load the data generated the 
	### **Code Functionalities Explained as Points**

1. **Dataset Loading**:
   - Loads traffic data from an Excel file (`output_with_durations.xlsx`).
   - The data includes features like `Vehicles Entered`, `Vehicles Seen`, `Mean Speed`, `Mean Occupancy`, and `Max Occupancy`.

2. **Feature and Target Selection**:
   - Defines input features (**X**) and target variables (**y_green** for green duration, **y_red** for red duration).

3. **Train-Test Split**:
   - Splits the data into training and testing sets (80% train, 20% test) for both green and red light durations.

4. **Feature Scaling**:
   - Scales the features using `StandardScaler` to normalize data for improved model performance.

5. **ML Models Initialization**:
   - Initializes four regression models: 
     - **Linear Regression** (for simple relationships).
     - **Decision Tree Regressor** (for non-linear relationships).
     - **Random Forest Regressor** (ensemble model for higher accuracy).
     - **XGBoost Regressor** (gradient boosting for complex patterns).

6. **Hyperparameter Tuning**:
   - Defines parameter grids for **Random Forest** and **XGBoost** to fine-tune the models using `GridSearchCV`.

7. **Directory Management**:
   - Creates directories to save trained models and predictions.
   - Moves old files to a timestamped archive folder (`old_files`).

8. **Training Models for Green Duration**:
   - Trains each model on the green duration data.
   - Applies hyperparameter tuning if applicable.
   - Saves the best model as a `.pkl` file.

9. **Evaluating Green Duration Predictions**:
   - Makes predictions on the test data.
   - Evaluates model performance using:
     - **Mean Squared Error (MSE)**: Measures average prediction error.
     - **R² Score**: Measures the proportion of variance explained by the model.

10. **Training Models for Red Duration**:
    - Repeats the process for red duration, including training, hyperparameter tuning, and saving the models.

11. **Evaluating Red Duration Predictions**:
    - Similar to green duration, evaluates performance using MSE and R² scores.

12. **Saving Predictions**:
    - Combines actual and predicted values for both green and red durations with input features.
    - Saves the results as an Excel file for each model.

13. **Model Output Files**:
    - Saves trained models (`.pkl`) and prediction results (`.xlsx`) to the `data/ml_outputs` directory.

14. **Purpose**:
    - Predict optimal green and red light durations for traffic control based on historical data.
    - Compare multiple ML models to identify the best-performing approach for real-world implementation.
    
    Now the data collected in the first script need to be used in the second scripts and train for all Machine learning the models.
now use all the models in the second scripts need to applied for the first scripts. now for each simulations the data generated plot the waiting time scripts 
### **Code Functionalities Explained as Points**

1. **Load the Data**:
   - Reads a CSV file containing traffic simulation data into a Pandas DataFrame.
   - The file includes metrics like `Time Step`, `Mean Speed`, and `Vehicles Entered`.

2. **Define a Waiting Threshold**:
   - Sets a threshold (`speed_threshold = 1.0`) to identify vehicles that are "waiting" (i.e., moving slowly or stopped).

3. **Calculate Wait Time per Time Step**:
   - Adds a new column `Wait Time`:
     - For each row, if `Mean Speed` is below the threshold, `Wait Time = 1` (indicating waiting).
     - Otherwise, `Wait Time = 0`.

4. **Compute Total Wait Time**:
   - Sums the `Wait Time` column to get the total number of time steps where vehicles were waiting.

5. **Compute Total Vehicles Entered**:
   - Sums the `Vehicles Entered` column to get the total count of vehicles processed during the simulation.

6. **Calculate Average Wait Time**:
   - Divides `Total Wait Time` by `Total Vehicles Entered` to compute the **average wait time per vehicle**.
   - Handles cases where no vehicles have entered (prevents division by zero).

7. **Plot Average Wait Time Over Time**:
   - Creates a cumulative plot of **Average Wait Time** across time steps.
   - X-axis: `Time Step` (progression of the simulation).
   - Y-axis: Average wait time (in seconds).
   - Displays trends in waiting time over the duration of the simulation.

8. **Visualization**:
   - Adds labels, a title, and a legend for better understanding of the plot.
   - Provides insights into whether the traffic system's performance is improving or deteriorating over time.

9. **Purpose**:
   - Measures and visualizes traffic system efficiency based on how long vehicles are waiting.
   - Identifies potential areas for optimization in traffic management.
 
Now simulate the data for all the models 
and for that data generated plot the average waiting time
and for that data is generated use the same models data for training the models and  and save the models and use the latest models in the simulation to control the traffic.

act as professional and very intelligent project thinker and planner of data scienctist with 15 years of experience create a process how to build the project in a step by step manner   I am also attaching the scripts and for reference and suggest the changes what need to be done. 



FINAL_MODIFIED/
├── code_files/
│   ├── initial_output_files_simulate/
│   ├── simulated_data/          # Contains traffic simulation output CSV files
│   ├── data/                    # Contains initial data and training data
│   ├── logs/                    # Contains log files for each run
│   ├── ml_outputs/              # Contains trained models and predicted outputs
│   ├── plots/                   # Contains average wait time plots
│   └── traffic_data_log.csv     # Main data log for traffic simulation
├── scripts/
│   ├── main_project_flow.py     # Main control script for the project
│   ├── traffic_simulate_data_generate.py  # Traffic simulation script
│   ├── ml_training.py           # Model training script
│   ├── average_wait_time.py     # Wait time calculation and plotting script
│   └── data_analysis.ipynb      # Optional: For exploratory data analysis
