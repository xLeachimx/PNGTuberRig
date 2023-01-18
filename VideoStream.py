# File: VideoStream.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 18 Jan 2023
# Purpose:
#   A simple class for handling a video stream.
# Notes:


import cv2
from threading import Thread
from time import perf_counter


class VideoStream:
  # Precond:
  #   fps is an integer representing the number of frames in one second.
  #
  # Postcond:
  #   Creates a new video stream object and starts it running.
  def __init__(self, fps=30):
    self.fps = fps
    self.f_delta = 1 / self.fps
    self.last_frame = None
    self.video_cap = None
    self.video_thread = Thread(target=self.__grab_frame)
    self.video_thread.daemon = True
    self.video_active = True
    self.video_thread.start()
    
  # Precond:
  #   None.
  #
  # Postcond:
  #   Retrurns the last frame.
  def grab_frame(self):
    return self.last_frame
  
  # Precond:
  #   None.
  #
  # Postcond:
  #   Starts the video stream.
  def start(self):
    if not self.video_active:
      self.video_active = True
      self.video_thread.start()
  
  # Precond:
  #   None.
  #
  # Postcond:
  #   Stops the video stream and closes the thread.
  def stop(self):
    if self.video_active:
      self.video_active = False
      self.video_thread.join()
      
  # Precond:
  #   None.
  #
  # Postcond:
  #   Returns the resolution of the stream.
  def resolution(self):
    if self.video_cap is not None:
      x = self.video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
      y = self.video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
      return x, y
    return None
    
  # Precond:
  #   None.
  #
  # Postcond:
  #   A separate thread function to grab webcam frames.
  def __grab_frame(self):
    self.video_cap = cv2.VideoCapture(1)
    self.video_cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    frame_start = perf_counter()
    while self.video_active:
      if perf_counter() - frame_start < self.f_delta:
        continue
      frame_start = perf_counter()
      ret, img = self.video_cap.read()
      if ret:
        self.last_frame = img
    self.last_frame = None
    self.video_cap.release()
    cv2.destroyAllWindows()
    
    