import streamlit as st
from library import *
from animation_3D import *
import copy
import cv2
import numpy as np
from tqdm import tqdm as tq
from PIL import Image
import tempfile
from Visualization import *
from trimming import *
import base64
import time
from pathlib import Path

video_file = None
# video_path = None
classes = []
# vid = None
detections = None
run_once = True
process = None
# page = None

st.set_page_config(layout="wide")
# st.theme("dark")


def make_grid(rows, cols):
    grid = [0]*rows
    for i in range(rows):
        with st.container():
            grid[i] = st.columns(cols)
    return grid


# Pages logic
if 'page' not in st.session_state:
    st.session_state.page = 0

def nextPage():
    st.session_state.page += 1


def firstPage():
    st.session_state.page = 0


ph = st.empty()


def imagebase64(img):
    with open(img, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def home():
    video_file = None
    # global process
    with ph.container():
        backh = imagebase64('backh.jpg')
        st.markdown(
            f"""
            <style>
                [data-testid="stAppViewContainer"] > .main{{
                background-image: url("data:image/png;base64,{backh}");
                background-size: cover;
                background-position: relative;
                background-repeat: no-repeat;
                background-attachment: local;}}
            </style>
            """,
            unsafe_allow_html=True
        )
        mygridc = make_grid(1, 2)
        mygridc[0][0].title("CricVision")
        mygridc[0][0].markdown("**Cricket Analytics and Estimations**")
        mygrid1 = make_grid(4, 3)
        mygrid1[0][0].image("GIFbat1.gif")
        mygridc[0][1].title("Home")
        mygrid1[0][2].image("wicket.gif")
        # Add content for the home page
        mygrid1[3][0].title("Video Input")
        # mygrid1[2][0].markdown("Select one option")
        selection = mygrid1[2][0].radio("Select one option", ('Single Video Processing', 'Batch Video Processing', 'Trimming a Video'))
        st.session_state.selection = selection

        if selection == 'Single Video Processing':
            video_file = st.file_uploader("Upload your video file", type=["mp4", "avi"])
            # if a file is uploaded, save it temporarily and get the path
            if video_file is not None:
                # create a temporary file to save the uploaded video
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(video_file.read())
                    video_path = tmp_file.name
                    st.video(video_path)
                    st.session_state.video_path = video_path
                mygrid2 = make_grid(1, 3)
                mygrid2[0][1].button("PROCESS VIDEO", on_click=nextPage)

        if selection == 'Batch Video Processing':
            # batch = True
            # st.write(video_file)
            video_files = st.file_uploader("Upload your video file", type=["mp4", "avi"], accept_multiple_files=True)
            if video_files is not None and video_files:
                videos_count = len(video_files)
                st.session_state.videos_count = videos_count
                # st.write(len(video_files))
                mygrid3 = make_grid(1, len(video_files))
                v = 0
                tmp_file_paths = []

                for uploaded_file in video_files:
                    # if video_file is not None:
                    # create a temporary file to save the uploaded video
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        video_paths = tmp_file.name
                        # Use the video file as needed (e.g., display or process it)
                        mygrid3[0][v].video(video_paths)
                        tmp_file_paths.append(video_paths)
                        # st.video(video_path)
                    v = v + 1

                st.session_state.tmp_file_paths = tmp_file_paths
                mygrid4 = make_grid(1, 3)
                mygrid4[0][1].button("PROCESS VIDEO", on_click=nextPage)
                # st.write(tmp_file_paths)
                st.session_state.tmp_file_paths = tmp_file_paths

        if selection == 'Trimming a Video':
            video_file_t = st.file_uploader("Upload your video file", type=["mp4", "avi"])
            # if a file is uploaded, save it temporarily and get the path
            if video_file_t is not None:
                # create a temporary file to save the uploaded video
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(video_file_t.read())
                    video_path_t = tmp_file.name
                    st.video(video_path_t)
                    st.session_state.video_path_t = video_path_t
                mygrid4 = make_grid(1, 3)
                mygrid4[0][1].button("PROCESS VIDEO", on_click=nextPage)


def processing():
    global video_path
    global classes
    global vid
    global detections
    # global process
    mygridpr = make_grid(2, 1)
    mygridp = make_grid(1,4)
    selection = st.session_state.selection
    if selection == 'Single Video Processing':
        video_path = st.session_state.video_path
        # if video_path:
        # Add a progress bar to track the execution progress
        progress_bar = mygridpr[0][0].progress(0)
        time.sleep(1)
        progress_bar.progress(0.1)

        # if detected:
        vid = open_video(video_path)
        detections = detect(vid)
        # st.session_state.detected = detected
        st.session_state.vid = vid
        st.session_state.detections = detections
        progress_bar.progress(0.7)
        time.sleep(1)
        progress_bar.progress(1.0)
        if detections is not None:
            mygridpr[1][0].success('THE VIDEO IS SUCCESSFULLY PROCESSED!', icon="✅")
        mygridp[0][1].button("GO BACK TO HOME", on_click=firstPage)
        mygridp[0][2].button("PROCEED TO DASHBOARD", on_click=nextPage)

    if selection == 'Batch Video Processing':
        tmp_file_paths = st.session_state.tmp_file_paths
        videos_count = st.session_state.videos_count
        detectionss = []
        vids = []
        co = 0
        # Add a progress bar to track the execution progress
        progress_bar = mygridpr[0][0].progress(0)
        for i in tmp_file_paths:
            vid1 = open_video(i)
            detection1 = detect(vid1)
            vids.append(vid1)
            detectionss.append(detection1)
            progress = (co + 1) / len(tmp_file_paths)
            progress_bar.progress(progress)
            co = co + 1

        st.session_state.vids = vids
        st.session_state.detectionss = detectionss
        if detectionss is not None:
            mygridpr[1][0].success(f'ALL {len(tmp_file_paths)} VIDEOS ARE SUCCESSFULLY PROCESSED!', icon="✅")
        mygridp[0][1].button("GO BACK TO HOME", on_click=firstPage)
        mygridp[0][2].button("PROCEED TO DASHBOARD", on_click=nextPage)

    if selection == 'Trimming a Video':
        video_path_t = st.session_state.video_path_t
        progress_bar = mygridpr[0][0].progress(0)
        time.sleep(1)
        progress_bar.progress(0.1)
        trim_folder = "trimmed_videos"
        trimmed_videos = auto_trim_video(video_path_t, trim_folder)
        progress_bar.progress(0.7)
        time.sleep(1)
        progress_bar.progress(1.0)
        if video_path_t is not None:
            mygridpr[1][0].success(f'THE VIDEO IS SUCCESSFULLY PROCESSED AND TRIMMED AND SAVED TO "{trim_folder}" FOLDER IN CURRENT DIRECTORY !', icon="✅")
        mygridp[0][1].button("GO BACK TO HOME", on_click=firstPage)
        # mygridp[0][2].button("PROCEED TO DASHBOARD", on_click=nextPage)


def dashboard():
    global video_path
    global classes
    global vid
    global detections
    with ph.container():
        backd = imagebase64('backd.jpg')
        st.markdown(
            f"""
            <style>
                [data-testid="stAppViewContainer"] > .main{{
                background-image: url("data:image/png;base64,{backd}");
                background-size: cover;
                background-position: relative;
                background-repeat: no-repeat;
                background-attachment: local;}}
            </style>
            """,
            unsafe_allow_html=True
        )
        mygridc1 = make_grid(1, 2)
        mygridc1[0][0].title("CricVision")
        mygridc1[0][0].markdown("**Cricket Analytics and Estimations**")
        video_path = st.session_state.video_path
        detections = st.session_state.detections
        vid = st.session_state.vid
        st.button("GO TO HOME", on_click=firstPage)
        mygridc1[0][1].title("Dashboard")
        mygridl = make_grid(1, 1)
        mygridl[0][0].markdown(
            " **_________________________________________________________________________________________________________________________________________________________________________**")

        mygrid = make_grid(5, 3)
        mygrid[0][0].markdown(" **Input Video**")
        mygrid[0][0].video(video_path)

        # Create checkbox
        mygrid[0][1].markdown(" **Select classes to visualize**")
        options = ['Ball', 'Bat', 'Batsman']
        if mygrid[0][1].checkbox(options[0]):
            # detected = st.session_state.detected
            vid = st.session_state.vid
            detections = st.session_state.detections
            classes.append(options[0])

        if mygrid[0][1].checkbox(options[1]):
            # detected = st.session_state.detected
            vid = st.session_state.vid
            detections = st.session_state.detections
            classes.append(options[1])

        if mygrid[0][1].checkbox(options[2]):
            # detected = st.session_state.detected
            vid = st.session_state.vid
            detections = st.session_state.detections
            classes.append(options[2])

        mygrid[0][1].markdown(" **After Selecting Classes, Press Visualize to Visualize Video**")

        visual = mygrid[0][2].button("Visualize")
        if visual:
            # detected = st.session_state.detected
            vid = st.session_state.vid
            detections = st.session_state.detections
            new_vid = copy.deepcopy(vid)
            video_to_display = visualize_bounding_boxes(detections, new_vid, classes)
            name = 'visual.mp4'
            save_video(video_to_display, name)

            # Read the video file into a bytes object
            with open(name, 'rb') as f:
                video_bytes = f.read()

            if video_bytes is not None:
                # create a temporary file to save the uploaded video
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(video_bytes)
                    video_visual = tmp_file.name
            classes = []
        if visual:
            mygrid[0][2].video(video_visual)
        else:
            mygrid[0][2].text_area(" ", "Video to be placed here")

        # vis = Visualization(detections)
        # impact_index = None
        if video_path:
            mygrid[1][0].markdown(" **Impact Frame**")
            impact_index = detect_impact_frame(detections)
            mygrid[1][0].image(vid[impact_index])

        if video_path:
            mygrid[1][1].markdown(" **Bounce Frame**")
            impact_index = detect_bounce_frame(detections, impact_index)
            mygrid[1][1].image(vid[impact_index])

        if video_path:
            mygrid[1][2].markdown(" **Bowling Side Estimation**")
            bowling_side = estimate_bowling_side(detections)
            if bowling_side == "LEFT":
                image = Image.open("left.png")
                resized_image = image.resize((1920, 1080))
                mygrid[1][2].image(resized_image)
                mygrid[1][2].markdown(bowling_side)
            if bowling_side == "RIGHT":
                image = Image.open("right.png")
                resized_image = image.resize((1920, 1080))
                mygrid[1][2].image(resized_image)
                mygrid[1][2].markdown(bowling_side)

        if video_path:
            mygrid[2][0].markdown(" **Impact Point Estimation**")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            ax = plot_impact1_2D(detections)
            ax.plot([1, 2, 3], [4, 5, 6])
            mygrid[2][0].pyplot()

        if video_path:
            mygrid[2][1].markdown(" **Bounce Point Estimation**")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            ax = plot_bounce_2D(detections)
            ax.plot([1, 2, 3], [4, 5, 6])
            mygrid[2][1].pyplot()

        if video_path:
            mygrid[2][2].markdown(" **Trajectory of Estimate Graph**")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            ax = plot_trajectory_2D(detections)
            ax.plot([1, 2, 3], [4, 5, 6])
            mygrid[2][2].pyplot()

        if video_path:
            mygrid[3][0].markdown(" **Plot of all Estimations**")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            ax = plot_all_2D(detections)
            ax.plot([1, 2, 3], [4, 5, 6])
            mygrid[3][0].pyplot()

        if video_path:
            mygrid[3][1].markdown(" **3D Plot of all Estimations**")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            ax = plot_all_3D(detections)
            ax.plot([1, 2, 3], [4, 5, 6])
            mygrid[3][1].pyplot()

        if video_path:
            mygrid[3][2].markdown(" **3D Animation of all Estimations**")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            # detections2 = pd.read_csv(f'detections/7.2.23/{4}.csv')
            gif_file = "animation.gif"
            animation3D(detections, gif_file)
            # ax.plot([1, 2, 3], [4, 5, 6])
            mygrid[3][2].image(gif_file)

        mygridl1 = make_grid(1, 1)
        mygridl1[0][0].markdown(
            " **_________________________________________________________________________________________________________________________________________________________________________**")


def dashboardstats():
    global video_path
    global classes
    global vid
    global detections
    with ph.container():
        backd = imagebase64('backd.jpg')
        st.markdown(
            f"""
                <style>
                    [data-testid="stAppViewContainer"] > .main{{
                    background-image: url("data:image/png;base64,{backd}");
                    background-size: cover;
                    background-position: relative;
                    background-repeat: no-repeat;
                    background-attachment: local;}}
                </style>
                """,
            unsafe_allow_html=True
        )

        # video_path = st.session_state.video_path
        # detections = st.session_state.detections
        # vid = st.session_state.vid
        mygridc2 = make_grid(1, 2)
        mygridc2[0][0].title("CricVision")
        mygridc2[0][0].markdown("**Cricket Analytics and Estimations**")
        st.button("GO TO HOME", on_click=firstPage)
        mygridc2[0][1].title("Dashboard")
        mygridl = make_grid(1, 1)
        mygridl[0][0].markdown(
            " **_________________________________________________________________________________________________________________________________________________________________________**")

        tmp_file_paths = st.session_state.tmp_file_paths
        videos_count = st.session_state.videos_count
        mygrids = make_grid(2, videos_count)
        mygrids[0][0].markdown(" **Input Videos**")
        vide = 0
        for files in tmp_file_paths:
            mygrids[1][vide].video(files)
            vide = vide + 1

        # # Create checkbox
        # mygrid[0][1].markdown(" **Select classes to visualize**")
        # options = ['Ball', 'Bat', 'Batsman']
        # if mygrid[0][1].checkbox(options[0]):
        #     # detected = st.session_state.detected
        #     vid = st.session_state.vid
        #     detections = st.session_state.detections
        #     classes.append(options[0])
        #
        # if mygrid[0][1].checkbox(options[1]):
        #     # detected = st.session_state.detected
        #     vid = st.session_state.vid
        #     detections = st.session_state.detections
        #     classes.append(options[1])
        #
        # if mygrid[0][1].checkbox(options[2]):
        #     # detected = st.session_state.detected
        #     vid = st.session_state.vid
        #     detections = st.session_state.detections
        #     classes.append(options[2])
        #
        # mygrid[0][1].markdown(" **After Selecting Classes, Press Visualize to Visualize Video**")
        #
        # visual = mygrid[0][2].button("Visualize")
        # if visual:
        #     # detected = st.session_state.detected
        #     vid = st.session_state.vid
        #     detections = st.session_state.detections
        #     new_vid = copy.deepcopy(vid)
        #     video_to_display = visualize_bounding_boxes(detections, new_vid, classes)
        #     name = 'visual.mp4'
        #     save_video(video_to_display, name)
        #
        #     # Read the video file into a bytes object
        #     with open(name, 'rb') as f:
        #         video_bytes = f.read()
        #
        #     if video_bytes is not None:
        #         # create a temporary file to save the uploaded video
        #         with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        #             tmp_file.write(video_bytes)
        #             video_visual = tmp_file.name
        #     classes = []
        # if visual:
        #     mygrid[0][2].video(video_visual)
        # else:
        #     mygrid[0][2].text_area(" ", "Video to be placed here")
        #
        # detectionss = []
        # for i in tmp_file_path:
        #     # detection=pd.read_csv(f'detections/7.2.23/{i}.csv')
        #     vid = open_video(i)
        #     detection1 = detect(vid)
        #     detectionss.append(detection1)
        #
        vids = st.session_state.vids
        detectionss = st.session_state.detectionss
        # mygrids1 = make_grid(5, videos_count)
        # mygrids1[0][0].markdown(" **Bounce Frames**")
        # if tmp_file_paths:
        #     mygrids1[0][0].markdown(" **Impact Frames**")
        #     ind = 0
        #     impacts = []
        #     for i in vids:
        #         impact_index = detect_impact_frame(detectionss[ind])
        #         # st.write(impact_index)
        #         if impact_index is not None:
        #             mygrids1[1][ind].image(vids[ind][impact_index])
        #             ind = ind + 1
        #             impacts.append(impact_index)
        # if tmp_file_paths:
        #     mygrids1[2][0].markdown(" **Bounce Frames**")
        #     ind = 0
        #     for i in vids:
        #         impact_index = detect_bounce_frame(detectionss[ind], impacts[ind])
        #         mygrids1[3][ind].image(vids[ind][impact_index])
        #         ind = ind + 1

        mygrids2 = make_grid(3, 2)
        if tmp_file_paths:
            mygrids2[0][0].markdown(" **Bounce Point Statistics**")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            ax = bounce_statistics(detectionss)
            ax.plot([1, 2, 3], [4, 5, 6])
            mygrids2[0][0].pyplot()

        if tmp_file_paths:
            mygrids2[0][1].markdown(" **Impact Point Statistics**")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            ax = impact_statistics(detectionss)
            ax.plot([1, 2, 3], [4, 5, 6])
            mygrids2[0][1].pyplot()

        if tmp_file_paths:
            mygrids2[1][0].markdown(" **Trajectory Statistics**")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            ax = trajectory_statistics(detectionss)
            ax.plot([1, 2, 3], [4, 5, 6])
            mygrids2[1][0].pyplot()

        if tmp_file_paths:
            mygrids2[1][1].markdown(" **All Points Statistics**")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            ax = all_stats_2D(detectionss)
            ax.plot([1, 2, 3], [4, 5, 6])
            mygrids2[1][1].pyplot()

        mygridl1 = make_grid(1, 1)
        mygridl1[0][0].markdown(
            " **_________________________________________________________________________________________________________________________________________________________________________**")


# Page 0
if st.session_state.page == 0:
    home()


# Page 1
elif st.session_state.page == 1:
    processing()

# Page 1
elif st.session_state.page == 2:
    selection = st.session_state.selection
    if selection == 'Batch Video Processing':
        dashboardstats()
    if selection == 'Single Video Processing':
        dashboard()
