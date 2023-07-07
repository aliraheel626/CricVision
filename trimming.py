import os
# %matplotlib inline
import matplotlib.pyplot as plt
from ultralytics import YOLO
import cv2


def is_present(frame):
    # Implement your logic to check if the object is present in the frame
    # Return True if the object is present, False otherwise
    model=YOLO('player.pt')
    result=model(frame, verbose=False)
    conf=[]
    for box in result[0].boxes:
        conf.append(float(box.conf)*100)
    if max(conf,default=0)<70 or len(conf)<=0:
        return False
    return True

def auto_trim_video(input_file, output_folder):
    video = cv2.VideoCapture(input_file)
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

    trimmed_video_buffer = []
    video_segment_counter = 0


    while True:
        ret, frame = video.read()

        if not ret:
            # No next frame, check if the trimmed video length is greater than 25 frames
            if len(trimmed_video_buffer) > int(fps):
                save_trimmed_video(trimmed_video_buffer, frame_width, frame_height, fps, video_segment_counter, output_folder)
                video_segment_counter += 1
            break


        if is_present(frame):
            trimmed_video_buffer.append(frame.copy())
        else:
            print(f"buffer Length: {len(trimmed_video_buffer)}")
            if len(trimmed_video_buffer) >int(fps):
                save_trimmed_video(trimmed_video_buffer, frame_width, frame_height, fps, video_segment_counter, output_folder)
                video_segment_counter += 1
            trimmed_video_buffer = []

    video.release()

def save_trimmed_video(trimmed_video_buffer, frame_width, frame_height, fps, segment_counter, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"{segment_counter}.mp4")
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*"MPV4"), fps, (frame_width, frame_height))

    for frame in trimmed_video_buffer:
        out.write(frame)

    out.release()

# # Example usage
# input_video_file = "0.mp4"
# output_folder_name = "output_folder"
# auto_trim_video(input_video_file, output_folder_name)