# File: FaceFeatures.py
# Author: Michael Huelsman
# Copyright: Dr. Michael Andrew Huelsman 2023
# License: GNU GPLv3
# Created On: 18 Jan 2023
# Purpose:
#   Facial feature rescognizer/buffer for rigging the PNGTuber
# Notes:

import face_recognition as fr
import pygame as pg
import numpy as np

class FacialFeatures:
  # Precond:
  #   res is a tuple representing the resolution of the frames.
  #
  # Postcond:
  #   Sets up storage for facial feature tracking.
  def __init__(self, res):
    self.res = res
    self.features = None
    self.eyebrows = {}
    
  # Precond:
  #   frame is a valid openCV image.
  #
  # Postcond:
  #   Updates the facial features tracking based on the given frame.
  def update_features(self, frame):
    landmarks = fr.face_landmarks(frame)
    if len(landmarks) > 0:
      self.features = landmarks[0]
      self.eyebrows["left"] = self.features["left_eyebrow"]
      self.eyebrows["right"] = self.features["right_eyebrow"]
      del self.features["left_eyebrow"]
      del self.features["right_eyebrow"]
      del self.features["chin"]
      for feature in self.features:
        self.features[feature] = np.array(self.features[feature])
        min_vals = self.features[feature].min(axis=0)
        max_vals = self.features[feature].max(axis=0)
        self.features[feature] = (min_vals, max_vals)
    
  # Precond:
  #   surf is the surface to draw the features on.
  #
  # Postcond:
  #   Draws the features onto the surface.
  def draw_to_surf(self, surf):
    for brow in self.eyebrows:
      pg.draw.polygon(surf, (180, 0, 0), self.eyebrows[brow])
    for feature in self.features:
      upper_left = self.features[feature][0]
      dims = self.features[feature][1] - self.features[feature][0]
      pg.draw.rect(surf, (180, 0, 0), pg.Rect(upper_left, dims))
