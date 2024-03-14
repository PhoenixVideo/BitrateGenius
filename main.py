# Copyright (C) 2024 Amritha Premkumar, Prajit T Rajendran, Vignesh V Menon
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import subprocess
import os
import pickle
import pandas as pd
import numpy as np
import time
import platform
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


def predict_bitrate(parameters_vector, path):
    bitrate_pred_model = pickle.load(open(path, 'rb'))
    pred_bitrate = bitrate_pred_model.predict(parameters_vector)
    return pred_bitrate


def clean_up(file_path):
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
    build_directory = os.path.join(current_directory, "build")
    temp_csv_path = os.path.join(build_directory, "temp.csv")
    model_path = os.path.join(build_directory, 'bitrate_predictor.pkl')

    video_file_extension = os.path.splitext(input_video_file)[1]
    if video_file_extension == '.y4m':
        vca_parameters = ["--input", input_video_file, "--complexity-csv", temp_csv_path, "--no-edgedensity",
                          "--no-dctenergy-chroma"]
    elif video_file_extension == '.yuv':
        vca_parameters = ["--input", input_video_file, "--input-res", "3840x2160", "--input-fps", "60", "--complexity-csv",
                          temp_csv_path, "--no-edgedensity", "--no-dctenergy-chroma"]
    else:
        print("Video extension other than .y4m and .yuv is not supported")
        sys.exit()

    start_time = time.time()

    run_executable_in_build(sys_platform, build_directory, vca_parameters)

    df = pd.read_csv(os.path.join(temp_csv_path))

    h_mean = df["h"].mean()
    E_max = df["E"].max()
    entropy_max = df["entropy"].max()
    entropyDiff_max = df["entropyDiff"].max()
    entropyU_max = df["entropyU"].max()
    entropyV_max = df["entropyV"].max()

    model_parameters = [
        [h_mean, E_max, entropy_max, entropyDiff_max, entropyU_max, entropyV_max]]

    predicted_bitrate = predict_bitrate(model_parameters, model_path)

    end_time = time.time()

    total_execution_time = end_time - start_time

    print("total_execution_time", total_execution_time, "seconds")

    print("The predicted bitrate (in kbps) is: " + str(np.power(10, predicted_bitrate[0])) + " kbps")

    clean_up(temp_csv_path)
