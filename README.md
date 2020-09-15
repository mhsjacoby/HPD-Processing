# Introduction
Author: Maggie Jacoby
Updated: 2020-09-15

This repository contains the processing and inferencing code for the HPD mobile project.
Helper files used: 
- gen_argparse.py
- my_functions.py


# To-Do
- Modify `post_img.py` to generate a grouped confidence value.
- Move and update unpickling code.
- Update `Image_Resize.py` to conform to newer practices.
- Modify `confidence.py` to use `gen_argparse` functions (need to change how `yolo` specific arguments are passed).
- Write code to print bounding boxes with confidence level on images that are saved via `copy_image.py`.


# Process-Images
After images were collected by the HPDmobile system, they were either pickled and then transferred (most of the homes), or transferred directly (first few homes).

- Need to move in the code from previous repository that unpickles images. 

- Image_Resize.py

    Images were originally saved in 336x336 pixels. 
    For pickled images they were saved as 112x112 pixels, which is the sized expected by the classifier.
    For the public database, images will be resized to 32x32 pixles.

- copy_img.py

    This code looks at the inferences created (at 1 second frequency) and copies the files into labeled folders, depending on classification confidence level.

# Inference-Images
Image inferencing is done via yolo (You Only Look Once) version 5 (<https://github.com/ultralytics/yolov5>) algorithm. Additional documentation is in `/yolov5/Source-Documentation`. The trained models and weights may not be updated online because of their size. 


## Steps for generating inferences on images:
1. confidence.py and detect.py

    These are parallel files. detect.py outputs just a binary occupancy prediction (`1 = occupied`). Only one needs to be run. Confidence.py outputs the highest confidence level, above some threshold (`default = 0.1`) from the yolov5 algorithm, as well as a binary prediciton based on a different threshold (`default = 0.5`) for every second. Input to these files is path location to stored images (eg `/Volumes/TOSHIBA-18/H6-black/`) with optional additional arguments, and output is predictions and/or confidence on a 1-second frequency in day-wise CSVs (86,400 entries per day) stored in `.../H6-black/Inference_DB/BS3/img_1sec/`. These files take a long time to run (about 20-30 minutes per day of data for a single hub, or upto 45-60 minutes if running multiple hubs simultaneously.)

2. post_img.py

    This takes in the daywise 1-second image csvs and averages to get a 10-second frequency. Output is stored in ```.../H6-black/Inference_DB/BS3/img_inf/``` in day-wise CSVs (8,640 long).
    **To-Do**: Make this file accept output from confidence.py (probably by using the maximum over the 10 second window). Currently only takes in outputs from detect.py.