# File: VideoDisplay.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 18 Jan 2023
# Purpose:
#   A Basic video display tool.
# Notes:

from VideoStream import VideoStream
from FaceFeatures import FacialFeatures
import pygame as pg
from time import perf_counter, sleep

class VideoDisplay:
  # Precond:
  #   res is a tuple representing the resolution of the display.
  #   stream is a valid VideoStream object.
  #
  # Postcond:
  #   Initializes a video display.
  def __init__(self, stream):
    pg.display.init()
    self.res = stream.resolution()
    while self.res is None:
      sleep(10)
      self.res = stream.resolution()
    self.display = pg.display.set_mode(self.res)
    self.stream = stream

  # Precond:
  #   None.
  #
  # Postcond:
  #   Runs the video display.
  def run(self):
    facial_features = FacialFeatures(self.res)
    running = True
    f_delta = self.stream.f_delta
    print(f_delta)
    frame_start = perf_counter()
    while running:
      if perf_counter() - frame_start < f_delta:
        continue
      frame_start = perf_counter()
      frame = self.stream.grab_frame()
      if frame is not None:
        facial_features.update_features(frame)
        # frame = pg.image.frombuffer(frame.tostring(), frame.shape[1::-1], "BGR")
        # self.display.blit(frame, (0, 0))
        self.display.fill((0, 255, 0))
        facial_features.draw_to_surf(self.display)
        pg.display.flip()
      for event in pg.event.get():
        # only do something if the event is of type QUIT
        if event.type == pg.QUIT:
          # change the value to False, to exit the main loop
          running = False

    
if __name__ == '__main__':
  stream = VideoStream()
  display = VideoDisplay(stream)
  display.run()