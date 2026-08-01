import io
import cv2
import numpy as np
import streamlit as st
from PIL import  Image



def adjust_brightness(image_rgb: np.ndarray, brightness: int) -> np.ndarray:
    """
    Adjust brightness by adding a scalar offset to pixel values.
    brightness range: -100 to 100
    """
    return cv2.convertScaleAbs(image_rgb, alpha=1.0, beta=brightness)