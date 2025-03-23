import pydicom
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import os
# Load the DICOM file
dicom_path = "E1154S7I.dcm"

#if you wanna see specific tags, mention here
show_selected_tags = False
selected_tags = [
    'PatientName', 'PatientID', 'StudyDescription', 'SliceLocation', 
    'Modality', 'StudyDate', 'Manufacturer', 'BodyPartExamined', 
    'PixelSpacing', 'Rows', 'Columns', 'BitsAllocated'
]


script_dir = os.path.dirname(os.path.realpath(__file__))
file_name = os.path.join(script_dir, dicom_path)
ds = pydicom.dcmread(file_name)



# Get the pixel data (assuming the DICOM file contains multiple slices)
ims = ds.pixel_array  # Shape: (num_slices, H, W)
num_slices = ims.shape[0]

# Normalize the pixel data for display (scaling it between 0 and 255)
ims = ((ims - ims.min()) / (ims.max() - ims.min()) * 255).astype(np.uint8)

# Define the DICOM tags you are interested in
if show_selected_tags==False:
    keywords = [elem.keyword for elem in ds if elem.keyword]
    keywords.remove("PixelData")  # Remove PixelData as it's not needed for display
    selected_tags = keywords

# Extract and print the selected DICOM data, keeping only non-null values
dicom_data = {}
for tag in selected_tags:
    try:
        value = getattr(ds, tag)
        # Keep only non-null, non-empty, and non-"Not Available" values
        if value not in [None, '', "Not available"]:
            dicom_data[tag] = value
    except AttributeError:
        dicom_data[tag] = "Not available"

# --- Create the Matplotlib figure (split into two sections: left for image, right for metadata)
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns
plt.subplots_adjust(left=0.05, right=0.95, bottom=0.25, top=0.9)  # Adjust space for the slider and button

# --- Plot the first image on the left side
im_disp = ax.imshow(ims[0], cmap='gray')
ax.set_title(f"Slice 1 / {num_slices}")
ax.axis('off')

# --- Add a line separating the image and the metadata section
ax.axvline(x=ims.shape[2] + 5, color='black', linewidth=20)  # Vertical line at the boundary between image and data

# --- Plot the DICOM metadata (static, once loaded) on the right side
dicom_info_text = ax2.text(0.1, 0.95, "DICOM Data", transform=ax2.transAxes, fontsize=12, verticalalignment='top')
ax2.axis('off')

# Format the DICOM data to be displayed
dicom_info = "\n".join([f"{key}: {value}" for key, value in dicom_data.items()])
dicom_info_text.set_text(dicom_info)

# --- Adjust the slider to be the same length as the number of images and fit the left side
slider_ax = plt.axes([0.1, 0.18, 0.3, 0.03])  # slider position (adjusted to fit the left side)
slider = Slider(slider_ax, 'Slice', 1, num_slices, valinit=1, valstep=1)

# --- Add a play button
play_ax = plt.axes([0.15, 0.09, 0.1, 0.05])
play_button = Button(play_ax, 'Forward', hovercolor='0.975')

# --- Add a backward button (next to play)
backward_ax = plt.axes([0.26, 0.09, 0.1, 0.05])  # Positioning next to the play button
backward_button = Button(backward_ax, 'Backward', hovercolor='0.975')

# --- Function to update the image when slider moves
def update(val):
    idx = int(slider.val) - 1
    im_disp.set_array(ims[idx])
    ax.set_title(f"Slice {idx + 1} / {num_slices}")
    fig.canvas.draw_idle()

slider.on_changed(update)

# --- Play function (Move forward)
playing = [False]  # mutable flag for stopping in the future if needed

def play(event):
    if playing[0]:
        return  # prevent multiple presses
    playing[0] = True
    for i in range(num_slices):
        slider.set_val(i + 1)
        plt.pause(0.05)  # adjust speed here
    playing[0] = False

play_button.on_clicked(play)

# --- Function to move backward (start from the last slice and go back to the first)
def move_backward(event):
    # Start at the last slice
    for i in range(num_slices - 1, -1, -1):  # Loop from the last image to the first
        slider.set_val(i + 1)
        update(slider.val)  # Update image accordingly
        plt.pause(0.05)  # Adjust speed here

backward_button.on_clicked(move_backward)

# --- Show the plot
plt.show()
