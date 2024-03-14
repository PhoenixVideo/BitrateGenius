# BitrateGenius

This code is submitted to the Grand Challenge on Video Complexity at IEEE International Conference on Image Processing (ICIP). 
The challenge is to predict the bitrate of a 3840x2160 (UHD) 60 fps video encoded using the libx264 codec with a medium preset and a constant rate factor (CRF) of 26. 
Videos from the Inter-4K dataset is used for training the models to predict bitrate when encoded using x264 implementation in FFmpeg 6.1.1. 
We employ light-weight content-complexity features extracted using video complexity analyzer (VCA) for prediction. 

# Building instructions

The software is tested in Windows OS. The steps to build the project in Windows are explained below.

## Prerequisites
 1. [Python](https://www.python.org/) version 3.12 or higher.

## Instructions to run in Windows

  1. Open Command prompt and Clone Repository :
  
     git clone --recurse-submodules https://github.com/PhoenixVideo/BitrateGenius

  2. Navigate to Project Directory :

     cd `<project_directory>`
	 
  3. Create and Activate Virtual Environment:

     python -m venv `<venv_name>`
     
     <venv_name>\Scripts\activate

  4. Install Dependencies:

     pip install -r requirements.txt

  6. Run the Application with the required CLI option and corresponding values, input video type should be either .y4m or .yuv:

     Sample command line:

     `python main.py --inputvideo <video_path>`

  7. Deactivate Virtual Environment:
  
     deactivate


Make sure to replace `<project_directory>`, and `<venv_name>` with the appropriate values for the project. Step 1 and Step 4 have to be done only the first time.
