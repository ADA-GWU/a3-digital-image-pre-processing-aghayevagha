import cv2
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils import *

# Select method key (change this to switch method)
method_key = 1

# Pick image using seed
index = get_image_index(42)
image_path = f'noisy/noisy/chemical/inchi{index}.png'

# Save options
save_filtered_image = False
save_plot_figure = True

# Resize option
resize = False
max_size = 300

# Define method map (key → method_name, function)
method_functions = {
    1: ("mean", lambda img: mean_filter(img)),
    2: ("median", lambda img: median_filter(img)),
    3: ("gaussian", lambda img: gaussian_filter(img)),
    4: ("conservative", lambda img: conservative_smoothing(img)),
    5: ("crimmins", lambda img: crimmins_filter(img)),
    6: ("frequency", lambda img: frequency_lowpass(img)),
    7: ("laplacian", lambda img: laplacian_filter(img)),
    8: ("unsharp", lambda img: unsharp_filter(img, kernel_size=7, sigma=3)),
    9: ("opening", lambda img: opening(img, 2, 2, 2, 2)),
    10: ("closing", lambda img: closing(img, 20, 5, 4, 2)),
    11: ("aghax", lambda img: aghax_kernel(img, 3, 5)),
    12: ("bilateral", lambda img: bilateral_filter(img))
}

# Get method name and function
method_name, method_function = method_functions[method_key]

# Paths
script_dir = os.path.dirname(os.path.realpath(__file__))
file_name = os.path.join(script_dir, image_path)
image_output_name = f'result_image{index}_{method_name}.jpeg'
plot_output_name = f'plot_image{index}_{method_name}.jpeg'

# Load image
image = cv2.imread(file_name)
if resize:
    image = resize_image(image, max_size)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Apply filter
if method_key == 1:  # Special pipeline: mean → unsharp(mean)
    mean = mean_filter(image)
    result = unsharp_filter(mean)
else:
    result = method_function(image)

# Compute difference
difference = cv2.absdiff(image, result)

# Plot original, result, and difference
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
titles = ["Original Image", f"{method_name.capitalize()} Filtered", "Difference (Original - Filtered)"]
images = [image, result, difference]
plt.subplots_adjust(wspace=0.05)

for ax, img, title in zip(axes, images, titles):
    ax.imshow(img)
    ax.set_title(title)
    ax.axis("off")
    rect = patches.Rectangle((0, 0), img.shape[1], img.shape[0],
                             linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(rect)

plt.tight_layout()

# Save plot figure
if save_plot_figure:
    plot_output_dir = os.path.join(script_dir, "task1_plot_outputs")
    os.makedirs(plot_output_dir, exist_ok=True)
    plot_output_path = os.path.join(plot_output_dir, plot_output_name)
    plt.savefig(plot_output_path, bbox_inches='tight', dpi=300)
    print(f"Plot saved to: {plot_output_path}")

plt.show()

# Save filtered image
if save_filtered_image:
    save_image(result, script_dir, image_output_name, 1)
