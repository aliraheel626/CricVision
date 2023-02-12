from ObjectDetector.detect_objects import detect_objects
from Video.buffer_video import buffer_video


video_file_path=''                                                  #video file path
frame_buffer=buffer_video(video_file_path)                          #use buffer_video function to get np.narray of video and store it in a frame buffer
detection=detect_objects(frame_buffer)                              #use frame_buffer in detect_objects as parameter and than use it to fill detection table