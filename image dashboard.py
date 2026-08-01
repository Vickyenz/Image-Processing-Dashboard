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


def adjust_saturation(image_rgb: np.ndarray, saturation_scale: float) -> np.ndarray:
    """
    Adjust saturation by scaling the S channel in HSV space.
    saturation_scale range: 0.0 (grayscale) to 3.0 (very saturated), 1.0 = unchanged
    """
    hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_scale, 0, 255)
    hsv = hsv.astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)