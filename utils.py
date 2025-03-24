import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.fft import fft2, ifft2, fftshift, ifftshift
import random


def read_image(path):
    image_bgr = cv2.imread(path)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    return image_rgb

def resize_image(image, max_size=800):
    if image is None:
        print("Error: Could not read the image!")
        return None
    height, width = image.shape[:2]

    # If either dimension exceeds max_size
    if width > max_size or height > max_size:
        scale = min(max_size / width, max_size / height)  # pick largest dimension
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    return image



# Function to save the image
def save_image(image, script_dir, output_name, task_index):
    # Create the "outputs" directory inside script_dir if it doesn't exist
    outputs_folder = os.path.join(script_dir, 'outputs')
    if not os.path.exists(outputs_folder):
        os.makedirs(outputs_folder)
    
    # Create the folder "output{task_index}" inside the "outputs" folder
    output_folder = os.path.join(outputs_folder, f'output{task_index}')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Define the output file path with the given output_name
    output_path = os.path.join(output_folder, output_name)

    # Save the image
    cv2.imwrite(output_path, image)
    print(f"Image saved at {output_path}")



# =======================================
                                # Part 1
# =======================================

#my method

def aghax_kernel(image, radius=1, threshold=5):
    """
    Removes isolated 0-pixels (structure) in chemical structure images.
    Converts 0 pixels with fewer than `threshold` zeros in their neighborhood to 255.

    Parameters:
        image (np.ndarray): Shape (H, W, 3), values 0 or 255.
        radius (int): Radius of the square neighborhood (r → window size = 2r+1).
        threshold (int): Minimum number of 0s in the neighborhood to keep a pixel as 0.

    Returns:
        np.ndarray: Denoised version of the first channel (0 and 255 values).
    """
    # Work only on the first channel
    gray = image[:, :, 0]
    output = gray.copy()  # Copy to make changes
    
    # Define the padded array for neighborhood checking
    padded = np.pad(gray, pad_width=radius, mode='constant', constant_values=255)
    
    # Iterate through the image
    for i in range(gray.shape[0]):
        for j in range(gray.shape[1]):
            if gray[i, j] == 255:
                continue  # Skip white pixels (background)

            # Get the neighborhood of the current pixel
            neighborhood = padded[i:i + 2*radius + 1, j:j + 2*radius + 1]
            zero_count = np.sum(neighborhood == 0)  # Count the 0s in the neighborhood

            # If fewer than the threshold number of 0s, turn it to 255 (background)
            if zero_count < threshold:
                output[i, j] = 255

    return np.array([output,output,output]).transpose(1,2,0)


def opening(image, kernel_erode=2, iteration_erode=1, kernel_dilate =2,  iteration_dilate=1):
    result = image.copy()

    kernel_erodes = (kernel_erode, kernel_erode)
    for _ in range(iteration_erode):
        result = cv2.erode(result, kernel_erodes)
    kernel_dilates = (kernel_dilate,kernel_dilate)
    for _ in range(iteration_dilate):
        result = cv2.dilate(result, kernel_dilates)
    return result

def closing(image, kernel_erode=2, iteration_erode=1, kernel_dilate =2,  iteration_dilate=1):
    result = image.copy()

    kernel_dilates = (kernel_dilate,kernel_dilate)
    for _ in range(iteration_dilate):
        result = cv2.dilate(result, kernel_dilates)

    kernel_erodes = (kernel_erode, kernel_erode)
    for _ in range(iteration_erode):
        result = cv2.erode(result, kernel_erodes)
    return result


def mean_filter(image, kernel_size=3):
    return cv2.blur(image, (kernel_size, kernel_size))

def median_filter(image, kernel_size=3):
    return cv2.medianBlur(image, kernel_size)

def gaussian_filter(image, kernel_size=5, sigma=0):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

def conservative_smoothing(img, kernel_size=3):
    """
    Apply conservative smoothing on an RGB image.
    - Converts image to grayscale internally.
    - Applies conservative smoothing on grayscale channel.
    - Replicates the smoothed grayscale image across all RGB channels.
    Returns the smoothed RGB image.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    pad = kernel_size // 2
    padded = np.pad(gray, pad_width=pad, mode='edge')
    output = gray.copy()
    rows, cols = gray.shape

    for i in range(rows):
        for j in range(cols):
            window = padded[i:i+kernel_size, j:j+kernel_size].flatten()
            center = gray[i, j]
            neighbors = np.delete(window, kernel_size * kernel_size // 2)
            local_min = np.min(neighbors)
            local_max = np.max(neighbors)
            if center < local_min:
                output[i, j] = local_min
            elif center > local_max:
                output[i, j] = local_max

    # Replicate smoothed grayscale back to RGB
    smoothed_rgb = cv2.merge([output]*3)
    return smoothed_rgb

def frequency_lowpass(image, cutoff=30):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    dft = fft2(gray)
    dft_shift = fftshift(dft)
    rows, cols = gray.shape
    crow, ccol = rows//2 , cols//2
    mask = np.zeros_like(gray, dtype=np.float32)
    mask[crow - cutoff:crow + cutoff, ccol - cutoff:ccol + cutoff] = 1
    fshift = dft_shift * mask
    img_back = np.abs(ifft2(ifftshift(fshift)))
    output = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return np.array([output,output,output]).transpose(1,2,0)

def laplacian_filter(image):
    return 255-cv2.Laplacian(image, cv2.CV_64F).astype(np.uint8)

def unsharp_filter(image, kernel_size=5, sigma=1.0, amount=1.5):
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    sharpened = cv2.addWeighted(image, 1 + amount, blurred, -amount, 0)
    return sharpened



def dark_pixel_adjustment(img):
    """Apply dark pixel adjustment in 4 directions."""
    for direction in [(0, 1), (1, 0), (1, 1), (1, -1)]:  # Vertical, Horizontal, Diagonal
        dx, dy = direction
        
        a = np.roll(img, shift=-dy, axis=0)  # Up/Left
        c = np.roll(img, shift=dy, axis=0)   # Down/Right
        
        condition1 = a >= img + 2
        condition2 = (a > img) & (img <= c)
        condition3 = (c > img) & (img <= a)
        condition4 = c >= img + 2
        
        img[condition1 | condition2 | condition3 | condition4] += 1
    
    return img

def light_pixel_adjustment(img):
    """Apply light pixel adjustment in 4 directions."""
    for direction in [(0, 1), (1, 0), (1, 1), (1, -1)]:  # Vertical, Horizontal, Diagonal
        dx, dy = direction
        
        a = np.roll(img, shift=-dy, axis=0)  # Up/Left
        c = np.roll(img, shift=dy, axis=0)   # Down/Right
        
        condition1 = a <= img - 2
        condition2 = (a < img) & (img >= c)
        condition3 = (c < img) & (img >= a)
        condition4 = c <= img - 2
        
        img[condition1 | condition2 | condition3 | condition4] -= 1
    
    return img

def bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)

def crimmins_filter(image, iterations=1):
    """Apply Crimmins Speckle Removal Algorithm to a grayscale image."""
    img = image.copy().astype(np.int16)  # Use int16 to avoid overflow
    
    for _ in range(iterations):
        img = dark_pixel_adjustment(img)
        img = light_pixel_adjustment(img)
    
    return np.clip(img, 0, 255).astype(np.uint8)  # Convert back to uint8

def get_image_index(seed):
    # Step 1: Use a separate generator with fixed seed
    rng_fixed = random.Random(seed)
    picked_list = rng_fixed.sample(range(1, 8), 3)  # Always same list
    print("Picked list:", picked_list)

    # Step 2: Use global randomness for dynamic final pick
    final_choice = random.choice(picked_list)
    print("Final choice (changes each run):", final_choice)
    return final_choice

