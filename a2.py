import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from utils import *

# Select image index and method key
index = 6
method_key = 12  # Just change this to switch method

# Resize settings
resize = True
max_size = 300

# Save settings
save_filtered_image = False
save_plot_figure = True

# Unified method dictionary (key → method_name, function)
method_functions = {
    1: ("mean", lambda img: mean_filter(img)),
    2: ("median", lambda img: median_filter(img)),
    3: ("gaussian", lambda img: gaussian_filter(img)),
    4: ("conservative", lambda img: conservative_smoothing(img, 5)),
    5: ("crimmins", lambda img: crimmins_filter(img, 2)),
    6: ("frequency", lambda img: frequency_lowpass(img)),
    7: ("laplacian", lambda img: laplacian_filter(img)),
    8: ("unsharp", lambda img: unsharp_filter(img, kernel_size=7, sigma=3)),
    9: ("opening", lambda img: opening(img, 3, 4, 3, 4)),
    10: ("closing", lambda img: closing(img, 20, 5, 4, 2)),
    11: ("aghax", lambda img: aghax_kernel(img, 3, 5)),
    12: ("bilateral", lambda img: bilateral_filter(img,d=5))
}

# Get method name and function
method_name, method_function = method_functions[method_key]

# Paths
base_image_path = f'noisy/noisy/speckle/{index}'
image_output_name = f'speckle{index}_{method_name}.jpeg'
plot_output_name = f'speckle{index}_{method_name}.jpeg'

def load_image_with_flexible_extension(base_path, extensions=(".jpeg", ".jpg", ".png")):
    for ext in extensions:
        full_path = f"{base_path}{ext}"
        if os.path.exists(full_path):
            return cv2.imread(full_path), full_path
    raise FileNotFoundError(f"No image found at {base_path} with extensions {extensions}")

# Load image
script_dir = os.path.dirname(os.path.realpath(__file__))
full_base_path = os.path.join(script_dir, base_image_path)
image, actual_path = load_image_with_flexible_extension(full_base_path)

# Resize and convert color
if resize:
    image = resize_image(image, max_size)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Apply selected filter
result = method_function(image)

# Plot Original vs Filtered
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
titles = ["Original Image", f"{method_name} Filtered"]
images = [image, result]

for ax, img, title in zip(axes, images, titles):
    ax.imshow(img)
    ax.set_title(title)
    ax.axis("off")

plt.tight_layout()

# Save plot if needed
if save_plot_figure:
    plot_output_dir = os.path.join(script_dir, "task2_plot_outputs")
    os.makedirs(plot_output_dir, exist_ok=True)
    plot_output_path = os.path.join(plot_output_dir, plot_output_name)
    plt.savefig(plot_output_path, bbox_inches='tight', dpi=300)
    print(f"Plot saved to: {plot_output_path}")

plt.show()

# Save filtered image if required
if save_filtered_image:
    save_image(result, script_dir, image_output_name, 2)
