# Setup

use Python 3.9.13

install packages using "python -m pip install -r requirements.txt"

run the application using "python -m streamlit run main.py"

# User Manual

## Home

![Home](https://github.com/aliraheel626/CricVision/assets/56185696/1ef5ed59-b083-422f-b6fd-417ec78cdf70)

1. The user selects one option from the radio buttons.
>  Single Video Processing \
>  Batch Video Processing \
> Video Trimming

2. the user than uses browse video to select videos or video's from explorer

3. The user than clicks on process video

## Single Video Processing

![dashboard](https://github.com/aliraheel626/CricVision/assets/56185696/43b9209f-447c-41a6-8fe0-462a5f7f3ee5)

- If the user has selected single video processing, than he processes a single video
-  In The top left corner, he can view the original video
-  The radio button represents the classes he can visualize within the video
-  Clicking on the visualize button at the top right will cause a new video to be generated with the detections visualized based on the selection of classes.
-  The Visualizations are at the bottom and are labelled appropriately.

## Batch Processing

![Batch](https://github.com/aliraheel626/CricVision/assets/56185696/bd1ca8f1-5483-4169-9ac8-ab0d3c762438)

Batch processing processes multiple videos and generates there cumulative graphs

## Video Trimming

In video trimming a longer video is selected. The module automatically trims the video and generates a folder called output_folder at the root directory
