import subprocess
import os
import sys
import pandas as pd
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
        #subprocess.run([executable_path, "--input", user_input, "--input-res", "3840x2160", "--input-fps", "60", "--complexity-csv", filename], check=True)
        subprocess.run([executable_path] + parameters, check=True)
        print("Executable ran successfully!")
    except subprocess.CalledProcessError:
        print("Error: Failed to execute the executable.")

# Example usage:
if __name__ == "__main__":

    # build_directory = "build/"
    # run_cmake_build(build_directory)
    #
    # if len(sys.argv) != 3:
    #     print("Usage: python script.py <user_input> <filename>")
    #     sys.exit(1)
    #
    # build_directory = "path/to/your/build/folder"
    # user_input = sys.argv[1]
    # filename = sys.argv[2]
    build_directory = "C:\\Users\\amrit\\Documents\\GitHub\\BitrateGenius\\build\\source\\apps\\vca\\Debug"
    # parameters = ["--input", "C:\\Users\\amrit\\Downloads\\elephants_dream_360p24.y4m\\elephants_dream_360p24.y4m", "--input-res", "640x360", "--input-fps", "60", "--complexity-csv",
    #               "filename"]

    # parameters = [""]

    parameters = ["--input", "C:\\Users\\amrit\\Downloads\\elephants_dream_360p24.y4m\\elephants_dream_360p24.y4m", "--complexity-csv",
                  "C:\\Users\\amrit\\Documents\\GitHub\\BitrateGenius\\build\\temp.csv", "--frames",  "100"]
    run_executable_in_build(build_directory, parameters)

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
    print("All Done")






#features_selected = ['E_max', 'E_std','h_mean', 'h_std','L_mean','entropy_max','entropyDiff_mean', 'entropyU_max', 'entropyV_max']




