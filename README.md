# Assignment 3

This repository contains the source code and images for Assignment 3.

## Structure

- `noisy/` — The folder provided by the instructor. Make sure it is in the same directory as the scripts.
- `utils.py` — Contains the filter and image processing functions.
- `task1-plot-outputs/` and `task2-plot-outputs/` — Contain the images for the report.
- Other scripts (`a1.py`, `a2.py`, `a3.py`) correspond to the assignment parts.

## Assignments

- [Part 1](#part-1)
- [Part 2](#part-2)
- [Part 3](#part-3)
- [How to Run](#how-to-run)

## Part 1

Based on a seed, I have chosen 3 random images. For each filtering function (kernel), the program randomly picks one of those 3 images.

Aside from techniques learned in class, I present my own approach which significantly outperforms other filters due to the nature of these images.

To simplify program structure, I’ve created a method map that links method names to their corresponding functions. You can save method results separately.

### 📚 Filtering Method Mapping and Analysis

1. **Mean Filter**

   _Text: Write your analysis and observations here._

   ![Mean Filter Result](plot_outputs/plot_image1_mean.png)

2. **Median Filter**

   _Text: Write your analysis and observations here._

   ![Median Filter Result](plot_outputs/plot_image1_median.png)

3. **Gaussian Filter**

   _Text: Write your analysis and observations here._

   ![Gaussian Filter Result](plot_outputs/plot_image1_gaussian.png)

4. **Conservative Smoothing**

   _Text: Write your analysis and observations here._

   ![Conservative Smoothing Result](plot_outputs/plot_image1_conservative.png)

5. **Crimmins Speckle Removal**

   _Text: Write your analysis and observations here._

   ![Crimmins Filter Result](plot_outputs/plot_image1_crimmins.png)

6. **Frequency Low-Pass Filter**

   _Text: Write your analysis and observations here._

   ![Frequency Filter Result](plot_outputs/plot_image1_frequency.png)

7. **Laplacian Filter**

   _Text: Write your analysis and observations here._

   ![Laplacian Filter Result](plot_outputs/plot_image1_laplacian.png)

8. **Unsharp Filter**

   _Text: Write your analysis and observations here._

   ![Unsharp Filter Result](plot_outputs/plot_image1_unsharp.png)

9. **Morphological Opening**

   _Text: Write your analysis and observations here._

   ![Opening Result](plot_outputs/plot_image1_opening.png)

10. **Morphological Closing**

   _Text: Write your analysis and observations here._

   ![Closing Result](plot_outputs/plot_image1_closing.png)

11. **Aghax Kernel Method**

   _Text: Write your analysis and observations here._

   ![Aghax Filter Result](plot_outputs/plot_image1_aghax.png)

---

## Part 2

In this part, I provide only the best results based on qualitative analysis. You can run `a2.py` and experiment with different filters on the speckle images.

## Part 3

Run `a3.py`, which provides an interactive tool to view images in a loop (forward and backward). You can also use a slider to navigate through different image frames.

You can save filtered images by setting `save` to `True`. It will save the result under `outputs/output{assignment_number}/` using the `save_image` function.

You can also save the comparison plot by setting `save_plot` to `True`.

## How to Run

```bash
git clone https://github.com/ADA-GWU/a3-digital-image-pre-processing-aghayevagha.git
cd a3-digital-image-pre-processing-aghayevagha
