# BitrateGenius

This code is submitted to the Grand Challenge on Video Complexity at IEEE International Conference on Image Processing (ICIP). 
The challenge is to predict the bitrate of a video encoded using the libx264 codec with a medium preset and a constant rate factor (CRF) of 26. 
Videos from the Inter-4K dataset is used for training the models to predict bitrate when encoded using x264 implementation in FFmpeg 6.1.1. 
We employ light-weight content-complexity features extracted using video complexity analyzer (VCA) for prediction. 
