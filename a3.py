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
ims = ds.pixel_array  
num_slices = ims.shape[0]

ims = ((ims - ims.min()) / (ims.max() - ims.min()) * 255).astype(np.uint8)

# Define the DICOM tags you are interested in
if show_selected_tags==False:
    keywords = [elem.keyword for elem in ds if elem.keyword]
    keywords.remove("PixelData") 
    selected_tags = keywords


dicom_data = {}
for tag in selected_tags:
    try:
        value = getattr(ds, tag)
        # Keep only non-null, non-empty, and non-"Not Available" values
        if value not in [None, '', "Not available"]:
            dicom_data[tag] = value
    except AttributeError:
        dicom_data[tag] = "Not available"


fig, (ax, ax2) = plt.subplots(1, 2, figsize=(14, 6)) 
plt.subplots_adjust(left=0.05, right=0.95, bottom=0.25, top=0.9)  


im_disp = ax.imshow(ims[0], cmap='gray')
ax.set_title(f"Slice 1 / {num_slices}")
ax.axis('off')

ax.axvline(x=ims.shape[2] + 5, color='black', linewidth=20)  

dicom_info_text = ax2.text(0.1, 0.95, "DICOM Data", transform=ax2.transAxes, fontsize=12, verticalalignment='top')
ax2.axis('off')

dicom_info = "\n".join([f"{key}: {value}" for key, value in dicom_data.items()])
dicom_info_text.set_text(dicom_info)

slider_ax = plt.axes([0.1, 0.18, 0.3, 0.03]) 
slider = Slider(slider_ax, 'Slice', 1, num_slices, valinit=1, valstep=1)

play_ax = plt.axes([0.15, 0.09, 0.1, 0.05])
play_button = Button(play_ax, 'Forward', hovercolor='0.975')

backward_ax = plt.axes([0.26, 0.09, 0.1, 0.05])  
backward_button = Button(backward_ax, 'Backward', hovercolor='0.975')

# --- Function to update the image when slider moves
def update(val):
    idx = int(slider.val) - 1
    im_disp.set_array(ims[idx])
    ax.set_title(f"Slice {idx + 1} / {num_slices}")
    fig.canvas.draw_idle()

slider.on_changed(update)

playing = [False]  

def play(event):
    if playing[0]:
        return  
    playing[0] = True
    for i in range(num_slices):
        slider.set_val(i + 1)
        plt.pause(0.05) 
    playing[0] = False

play_button.on_clicked(play)

def move_backward(event):
    for i in range(num_slices - 1, -1, -1):  
        slider.set_val(i + 1)
        update(slider.val)  
        plt.pause(0.05) 

backward_button.on_clicked(move_backward)

# --- Show the plot
plt.show()
