# %matplotlib inline
from ultralytics import YOLO
import pandas as pd
import re
import cv2
import math
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

BATSMAN_HEIGHT=191
CORNER_POINT_A=(-140,0,0)
CORNER_POINT_B=(140,0,0)
CORNER_POINT_C=(166, -321,0)
CORNER_POINT_D=(-166, -321,0)

PERSPECTIVE_TRANSFORMED_CORNER_POINT_A=(-140,0,0)
PERSPECTIVE_TRANSFORMED_CORNER_POINT_B=(140,0,0)
PERSPECTIVE_TRANSFORMED_CORNER_POINT_C=(140, -1876,0)
PERSPECTIVE_TRANSFORMED_CORNER_POINT_D=(-140, -1876,0)


def open_video(video_path):
    vid = list()
    cap = cv2.VideoCapture(video_path)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
    # fc=0
    while True:
        ret, frame = cap.read()
        if not ret: break  # break if no next frame

        # buf[fc]=frame # append frame
        # fc+=1
        vid.append(frame)
    # release and destroy windows
    cap.release()
    cv2.destroyAllWindows()
    return vid


def frame_height(vid):
    frame=vid[0]
    height=len(frame)
    return height


def frame_width(vid):
    frame=vid[0]
    width=len(frame[0])
    return width


def save_video(vid,name):
    fourcc = cv2.VideoWriter_fourcc(*'MPV4')
    frame_width=len(vid[0][0])
    frame_height=len(vid[0])
    out = cv2.VideoWriter(name, fourcc, 25.0, (frame_width, frame_height))
    for frame in vid:
        out.write(frame)
    out.release


def suppress_duplicates(detections):
    # assuming your data frame is named `detections`
    # and has the columns `Frame`, `Class`, and `Confidence`

    # group by frame number and class name
    groups = detections.groupby(['Frame', 'Class'])

    # filter rows to keep only the detection with the highest confidence score for each group
    filtered_detections = groups.apply(lambda x: x.loc[x['Confidence'].idxmax()])

    # reset index of the filtered data frame
    filtered_detections = filtered_detections.reset_index(drop=True)

    return filtered_detections


def detect(vid):
    # model=YOLO('v2.pt')
    model=YOLO('./models/v3.pt')
    results=model(vid)
    df=pd.DataFrame(columns=["Frame","Class","Confidence","Xmin","Ymin","Xmax","Ymax","Xc","Yc","W","H","A"])
    for result in results:
        for box in result.boxes:
            xyxy=box.xyxy.numpy()[0]
            xywh=box.xywh.numpy()[0]
            frame_number=int(re.search('(?<=image)\d+',result.path).group())
            # cls="Bat" if box.cls==2 else "Ball" if box.cls==0 else "Batsman"
            cls=model.names[int(box.cls[0])]
            df.loc[len(df)]=[frame_number,cls,int(float(box.conf)*100),xyxy[0],xyxy[1],xyxy[2],xyxy[3],xywh[0],xywh[1],xywh[2],xywh[3],xywh[2]*xywh[3]]
    return suppress_duplicates(df)


def visualize_bounding_boxes(detections, vid, classes):
    # create a list to store the output frames
    output_frames = []

    # loop over each frame in the video
    for frame_number, frame in enumerate(vid):
        # create a copy of the frame
        output_frame = np.copy(frame)

        # select rows for the specified classes
        selected_rows = detections[detections['Class'].isin(classes) & (detections['Frame'] == frame_number)]

        # loop over the selected rows and draw bounding boxes on the output frame
        for index, row in selected_rows.iterrows():
            class_name = row['Class']
            xmin = int(row['Xmin'])
            ymin = int(row['Ymin'])
            xmax = int(row['Xmax'])
            ymax = int(row['Ymax'])
            color = (0, 255, 0)  # set the color for the bounding box

            # draw the bounding box on the output frame
            cv2.rectangle(output_frame, (xmin, ymin), (xmax, ymax), color, 2)
            cv2.putText(output_frame, class_name, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # add the output frame to the list of output frames
        output_frames.append(output_frame)

    # return the list of output frames
    return output_frames


def calculate_distances(detections):
    bat_ball = detections.loc[detections['Class'].isin(['Bat', 'Ball'])]

    # group rows by Frame
    groups = bat_ball.groupby('Frame')

    # compute distance between Bat and Ball coordinates for each group
    distances = []
    for name, group in groups:
        bat_coords = group.loc[group['Class'] == 'Bat', ['Xc', 'Yc']].values
        ball_coords = group.loc[group['Class'] == 'Ball', ['Xc', 'Yc']].values
        if len(bat_coords) > 0 and len(ball_coords) > 0:
            # distance = np.linalg.norm(bat_coords - ball_coords)
            distance=math.dist(bat_coords[0],ball_coords[0])
            distances.append((name, distance))

    # create a new data frame with the distances
    distances_df = pd.DataFrame(distances, columns=['Frame', 'Distance'])
    return distances_df


def detect_impact_frame(detections):
    distances_df=calculate_distances(detections)
    try:
        f_impact=distances_df.loc[distances_df['Distance'].idxmin()]["Frame"]
        return int(f_impact)
    except:
        return None


def detect_bounce_frame(detections,f_impact):
    grad0=(CORNER_POINT_D[1]-CORNER_POINT_A[1])/(CORNER_POINT_D[0]-CORNER_POINT_A[0])
    grad1=(CORNER_POINT_C[1]-CORNER_POINT_B[1])/(CORNER_POINT_C[0]-CORNER_POINT_B[0])
    c0=CORNER_POINT_A[1]-grad0*CORNER_POINT_A[0]
    c1=CORNER_POINT_B[1]-grad1*CORNER_POINT_B[0]
    ball_detections=detections.loc[(detections["Class"]=="Ball") & (detections["Frame"]<f_impact)] #class is ball and frame is before impact frame
    ball_detections[['Xz','Yz']]=ball_detections.apply(lambda x:calc_coords_of_ball_relative_to_batsman(detections,"Ball",x['Frame']),axis=1).tolist()
    ball_detections[['Xz','Yz']]=ball_detections.apply(lambda x:unzoom(x["Xz"],x["Yz"],detections,x["Frame"]),axis=1).tolist()
    ball_detections=ball_detections.loc[(ball_detections['Yz']>CORNER_POINT_C[1])&(ball_detections['Xz']>((ball_detections['Yz']-c0)/grad0))&(ball_detections['Xz']<((ball_detections['Yz']-c1)/grad1))]
    try:
        f_bounce=ball_detections.loc[ball_detections['Yc'].idxmax()]["Frame"] #get point where y-axis is max
        return int(f_bounce)
    except:
        return None


def estimate_bowling_side(detections):
    bat_ball = detections.loc[detections['Class'].isin(['Ball', 'Batsman'])]

    # group rows by Frame
    groups = bat_ball.groupby('Frame')

    # compute distance between Bat and Ball coordinates for each group
    distances = []
    for name, group in groups:
        batsman_coords = group.loc[group['Class'] == 'Batsman', ['Xc', 'Yc']].values
        ball_coords = group.loc[group['Class'] == 'Ball', ['Xc', 'Yc']].values
        if len(batsman_coords) > 0 and len(ball_coords) > 0:
            # distance = np.linalg.norm(bat_coords - ball_coords)
            x_vect=batsman_coords[0][0]-ball_coords[0][0]
            if x_vect>0:
                return "LEFT"
            else:
                return "RIGHT"


def estimate_btasman_side(detections):
    bat_batsmann = detections.loc[detections['Class'].isin(['Bat', 'Batsman'])]

    # group rows by Frame
    groups = bat_batsmann.groupby('Frame')

    # compute distance between Bat and Btasman coordinates for each group
    distances = []
    i = 0
    for name, group in groups:
        batsman_coords = group.loc[group['Class'] == 'Batsman', ['Xc', 'Yc']].values
        bat_coords = group.loc[group['Class'] == 'Bat', ['Xc', 'Yc']].values
        if len(batsman_coords) > 0 and len(bat_coords) > 0:
            x_vect=batsman_coords[0][0]-bat_coords[0][0]
            if x_vect>0:
                return "RIGHT HANDED BATSMAN"
            else:
                return "LEFT HANDED BATSMAN"


def unzoom(x,y,detections,frame):
    d_height=191
    f_height=int(detections.loc[(detections["Class"].isin(["Batsman"]))&(detections["Frame"]==frame)]["H"])
    zf=f_height/d_height
    x/=zf
    y/=zf
    return (int(x),int(y))


def to_horizontal_plane(x,y):
    return (x,y,0)


def to_vertical_plane(x,y):
    return (x,0,y)


def calc_coords_of_ball_relative_to_batsman(detections, cls, f):
    Batsman = detections.loc[detections["Class"].isin(["Batsman"]) & (detections["Frame"] == f)]
    Ball = detections.loc[detections["Class"].isin([cls]) & (detections["Frame"] == f)]
    P_X_Batsman = (Batsman["Xmin"] + Batsman["Xmax"]) / 2
    P_Y_Batsman = Batsman["Ymax"]
    try:
        X = int(Ball['Xc']) - int(P_X_Batsman)
        Y = int(P_Y_Batsman) - int(Ball['Yc'])
        return (X, Y)
    except:
        return (None,None)


def estimate_bounce_point(detections):
    f_impact=detect_impact_frame(detections)
    f_bounce=detect_bounce_frame(detections,f_impact)
    (X,Y)=calc_coords_of_ball_relative_to_batsman(detections,"Ball",f_bounce)
    try:
        if Y>0:
            Y=0
        (X,Y)=unzoom(X,Y,detections,f_bounce)
        return (X,Y)
    except:
        return (None,None)


def estimate_impact_point(detections):
    f_impact=detect_impact_frame(detections)
    (X,Y)=calc_coords_of_ball_relative_to_batsman(detections,"Ball",f_impact)
    try:
        (X,Y)=unzoom(X,Y,detections,f_impact)
        return (X,Y)
    except:
        return (None,None)


def estimate_trajectory(detections):
    f_impact=detect_impact_frame(detections)
    Ball=detections.loc[detections["Class"].isin(["Ball"]) & (detections["Frame"]>f_impact)]
    # Assuming your dataframe is named "Ball"
    try:
        # first_row = Ball.tail(1)  # Select the first row (when Ball detect after impact point)
        first_row = Ball.iloc[0]
        f_after_impact = int(first_row['Frame'])  # Access the value of the 'Frame' column in the first row
        (X,Y)=calc_coords_of_ball_relative_to_batsman(detections,"Ball",f_after_impact)
        (X,Y)=unzoom(X,Y,detections,f_impact)
        return (X,Y)
    except:
        return (None,None)


def estimate_release_point(bowlingSide):
    if bowlingSide == "LEFT":
        return (-83,-321,BATSMAN_HEIGHT)
    else:
        return (83,-321,BATSMAN_HEIGHT)




