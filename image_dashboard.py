import io
import cv2
import numpy as np
import streamlit as st
from PIL import  Image

st.set_page_config(page_title="Image Processing Dashboard", layout="wide")
st.title("🖼️ Image Processing Dashboard")
st.caption("Upload an image, convert color spaces, tweak brightness/saturation, and download the result.")

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


def convert_color_space(image_rgb: np.ndarray, target_space: str) -> np.ndarray:
    """
    Convert an RGB image to the chosen color space for DISPLAY purposes.
    Note: HSV/BGR arrays displayed directly will look 'wrong' to the eye on purpose —
    that's the actual pixel data in that color space, which is the point of showing it.
    """
    if target_space == "RGB":
        return image_rgb
    elif target_space == "BGR":
        return cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    elif target_space == "HSV":
        return cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
    else:
        raise ValueError(f"Unknown color space: {target_space}")


def numpy_to_downloadable_bytes(image_array: np.ndarray, file_format: str = "PNG") -> bytes:
        """
        Convert a NumPy RGB array into downloadable image bytes.
        """
        pil_image = Image.fromarray(image_array)
        buffer = io.BytesIO()
        pil_image.save(buffer, format=file_format)
        return buffer.getvalue()
 

st.sidebar.header("Controls")
 
uploaded_file = st.sidebar.file_uploader(
    "Upload an image", type=["png", "jpg", "jpeg", "bmp", "webp"]
)
 
color_space = st.sidebar.selectbox("Color space (for preview)", ["RGB", "BGR", "HSV"])
 
brightness = st.sidebar.slider("Brightness", min_value=-100, max_value=100, value=0, step=1)
 
saturation = st.sidebar.slider(
    "Saturation", min_value=0.0, max_value=3.0, value=1.0, step=0.05
)
 
output_format = st.sidebar.selectbox("Download format", ["PNG", "JPEG"])
 
# ----------------------------
# Main processing pipeline
# ----------------------------
if uploaded_file is not None:
    # Load image and force RGB (Pillow handles most formats/orientations cleanly)
    pil_original = Image.open(uploaded_file).convert("RGB")
    original_rgb = np.array(pil_original)
 
    # Apply brightness + saturation adjustments (always done in RGB/HSV space,
    # regardless of which color space the user wants to PREVIEW)
    adjusted = adjust_brightness(original_rgb, brightness)
    adjusted = adjust_saturation(adjusted, saturation)
 
    # Convert the adjusted image into the selected color space for display
    display_image = convert_color_space(adjusted, color_space)
 
    col1, col2 = st.columns(2)
 
    with col1:
        st.subheader("Original")
        st.image(original_rgb, use_container_width=True)
 
    with col2:
        st.subheader(f"Processed ({color_space} preview)")
        st.image(display_image, use_container_width=True, clamp=True)
 
    # ----------------------------
    # Download button
    # ----------------------------
    # Always save the RGB-adjusted version (not the HSV/BGR display array),
    # since HSV/BGR arrays aren't valid "natural" images to save and open elsewhere.
    downloadable_bytes = numpy_to_downloadable_bytes(adjusted, file_format=output_format)
 
    st.sidebar.download_button(
        label=f"⬇️ Download processed image ({output_format})",
        data=downloadable_bytes,
        file_name=f"processed_image.{output_format.lower()}",
        mime=f"image/{output_format.lower()}",
    )
 
else:
    st.info("👆 Upload an image from the sidebar to get started.")