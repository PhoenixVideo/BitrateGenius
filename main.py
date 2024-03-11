import subprocess
import os
import pickle
import pandas as pd
import time
def run_cmake_build(build_dir):
    # Change directory to the build folder
    os.chdir(build_dir)

    # Configure the build with CMake
    cmake_configure_cmd = ["cmake", "-DCMAKE_BUILD_TYPE=Release", "../VCA/"]
    subprocess.run(cmake_configure_cmd, check=True)

    # Build the project
    cmake_build_cmd = ["cmake", "--build", "."]
    try:
        subprocess.run(cmake_build_cmd, check=True)
        print("Build completed successfully!")
    except subprocess.CalledProcessError:
        print("Build failed!")

def run_executable_in_build(build_dir,parameters):
    # Change directory to the build folder
    os.chdir(build_dir)

    # Construct the path to the executable
    executable_path = os.path.join(build_dir, "vca.exe")

    # Execute the executable with the provided parameters
    try:
        subprocess.run([executable_path] + parameters, check=True)
        print("Executable ran successfully!")
    except subprocess.CalledProcessError:
        print("Error: Failed to execute the executable.")

def predict_bitrate(parameters_vector):
    # Load the pickled model
    loaded_model = pickle.load(open('C:\\Users\\amrit\\Desktop\\Video streaming papers\\ICIP Challenge\\best_br_model.pkl', 'rb'))

    # Assuming you have new data X_new for prediction
    y_pred_new = loaded_model.predict(parameters_vector)

    return y_pred_new


# Example usage:
if __name__ == "__main__":

    #build_directory = "build/"
    #run_cmake_build(build_directory)
    build_directory = "C:\\Users\\amrit\\Documents\\GitHub\\BitrateGenius\\build\\source\\apps\\vca\\Debug"

    parameters = ["--input", "C:\\Users\\amrit\\Downloads\\elephants_dream_360p24.y4m\\elephants_dream_360p24.y4m", "--complexity-csv",
                  "C:\\Users\\amrit\\Documents\\GitHub\\BitrateGenius\\build\\temp.csv", "--frames",  "100","--no-edgedensity" ]

    start_time_exe = time.time()
    run_executable_in_build(build_directory, parameters)
    end_time_exe = time.time()
    execution_time =  end_time_exe - start_time_exe
    print("Execution time exe:", execution_time, "seconds")
    start_time_csv = time.time()
    df = pd.read_csv("C:\\Users\\amrit\\Documents\\GitHub\\BitrateGenius\\build\\temp.csv")
    E_max = df["E"].max()
    E_std = df["E"].std()
    h_mean = df["h"].mean()
    h_std = df["h"].std()
    L_mean = df["L"].mean()
    entropy_max = df["entropy"].max()
    entropyDiff_mean = df["entropyDiff"].mean()
    entropyU_max = df["entropyU"].max()
    entropyV_max = df["entropyV"].max()
    parameters_vector = [[E_max, E_std,h_mean, h_std,L_mean,entropy_max,entropyDiff_mean,entropyU_max,entropyV_max]]
    print(parameters_vector)

    y_pred_new = predict_bitrate(parameters_vector)

    end_time_csv = time.time()
    execution_time_csv = end_time_csv - start_time_csv

    total_execution_time = execution_time + execution_time_csv
    print("total_execution_time", total_execution_time, "seconds")


    # Print or use the predictions
    print(y_pred_new)

    print("All Done")










