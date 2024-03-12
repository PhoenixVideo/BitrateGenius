import subprocess
import os
import pickle
import pandas as pd
import time
import platform
import math
import argparse
import sys


def run_executable_in_build(system_platform, build_dir, parameters):
    os.chdir(build_dir)
    executable_path = None
    if system_platform == 'Windows':
        executable_path = os.path.join(build_dir, "vca_release.exe")
        try:
            subprocess.run([executable_path] + parameters, check=True)
            print("Executable ran successfully!")
        except subprocess.CalledProcessError:
            print("Error: Failed to execute the executable.")
    elif system_platform == 'Linux':
        dist = platform.dist()
        if dist[0].lower() == 'ubuntu':
            executable_path = os.path.join(build_dir, "vca_release")
        try:
            subprocess.run([executable_path] + parameters, check=True)
            print("Executable ran successfully!")
        except subprocess.CalledProcessError:
            print("Error: Failed to execute the executable.")
    else:
        print("BitrateGenius currently works only in Windows or Ubuntu")


def predict_bitrate(parameters_vector):
    bitrate_pred_model = pickle.load(open(os.path.join(build_directory, 'bitrate_predictor.pkl'), 'rb'))
    pred_bitrate = bitrate_pred_model.predict(parameters_vector)
    return pred_bitrate


def clean_up():
    file_path = os.path.dirname(os.path.abspath(__file__)) + "/build/temp.csv"
    if os.path.exists(file_path):
        os.remove(file_path)


if __name__ == "__main__":

    # input arguments
    parser = argparse.ArgumentParser(
        description="BitrateGenius: Predict bitrate of x264 CRF26 2160p 60fps encoding (medium preset).")
    parser.add_argument("--inputvideo", help="Input file path",
                        default="C:\\Users\\amrit\\Desktop\\Video_streaming_papers\\0001.y4m")
    args = parser.parse_args()
    input_video_file = args.inputvideo

    sys_platform = platform.system()

    current_directory = os.path.dirname(os.path.abspath(__file__))
    build_directory = current_directory + "/build/"

    video_file_extension = os.path.splitext(input_video_file)[1]
    if video_file_extension == '.y4m':
        vca_parameters = ["--input", input_video_file, "--complexity-csv", current_directory + "/build/temp.csv", "--no-edgedensity", "--no-dctenergy-chroma"]
    elif video_file_extension == '.yuv':
        vca_parameters = ["--input", input_video_file, "--input-res", "3840x2160", "--fps", "60", "--complexity-csv",
                          current_directory + "/build/temp.csv", "--no-edgedensity", "--no-dctenergy-chroma"]
    else:
        print("Video extension other than .y4m and .yuv is not supported")
        sys.exit()

    start_time = time.time()

    run_executable_in_build(sys_platform, build_directory, vca_parameters)

    df = pd.read_csv(current_directory + "/build/temp.csv")
    E_max = df["E"].max()
    E_std = df["E"].std()
    h_mean = df["h"].mean()
    h_std = df["h"].std()
    L_mean = df["L"].mean()
    entropy_max = df["entropy"].max()
    entropyDiff_mean = df["entropyDiff"].mean()
    entropyU_max = df["entropyU"].max()
    entropyV_max = df["entropyV"].max()
    model_parameters = [
        [E_max, E_std, h_mean, h_std, L_mean, entropy_max, entropyDiff_mean, entropyU_max, entropyV_max]]

    predicted_bitrate = predict_bitrate(model_parameters)

    end_time = time.time()

    total_execution_time = end_time - start_time

    print("total_execution_time", total_execution_time, "seconds")

    print("The predicted bitrate (in kbps) is: " + str(math.exp(predicted_bitrate[0])) + " kbps")

    clean_up()
