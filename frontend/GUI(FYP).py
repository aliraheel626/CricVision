# import streamlit as st
# import numpy as np
# import cv2
# import matplotlib.pyplot as plt
#
# st.title("CricVision")
#
# btn = st.button("Press it")
# if btn:
#     st.title("Video Input Dashboard")
#     video_file = st.file_uploader("Upload your video file", type=["mp4", "avi"])
#     # if video_file is not None:
#     #     video_bytes = video_file.read()
#     #     st.video(video_bytes)
import streamlit as st


# Define a function for each page
def home():
    st.title("Home")
    # Add content for the home page
    st.title("Video Input Dashboard")
    video_file = st.file_uploader("Upload your video file", type=["mp4", "avi"])
    videodisp(video_file)


def videodisp(video_file):
    if video_file is not None:
        video_bytes = video_file.read()
        st.video(video_bytes)
    # return video_bytes


def about():
    st.title("Dashboard")
    # Add content for the about page
    col_widths = [3, 1, 2, 2]

    # Create the columns
    cols = st.columns(col_widths)
    cols[0].video("1.mp4")
    cols[0].radio('Show:', ['Ball', 'Pitch'])
    cols[1].text("Confidence")
    cols[1].text_area(label="")
    cols[2].markdown(" **:blue[Pitch Estimation]**")
    cols[2].text_area(label="1")
    cols[3].markdown(" **:blue[Player Side Estimation]**")
    cols[3].text_area(label="2")
    cols[2].markdown(" **:blue[Trajectoy of Estimate Graph]**")
    cols[2].text_area(label="3")
    cols[3].markdown(" **:blue[3d Plot of All Things Combined]**")
    cols[3].text_area(label="4")


# Define a dictionary to map page names to functions
pages = {
    "Home": home,
    "Dashboard": about
}


# Define a function to render the page
def render_page(page):
    # Call the function for the given page name
    pages[page]()


# Define the main function
def main():
    st.sidebar.title("Navigation")
    # Add a dropdown for page selection
    page = st.sidebar.selectbox("Select a page", tuple(pages.keys()))
    # page1 = st.sidebar.button("Home")
    # page2 = st.sidebar.button("Dashboard")
    # Render the selected page
    render_page(page)
    # if page1:
    #     home()
    # if page2:
    #     about()

if __name__ == "__main__":
    main()
