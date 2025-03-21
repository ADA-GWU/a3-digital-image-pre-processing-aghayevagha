# Assignment 3

This repository contains the source code and images for Assignment 3.

## Structure
  - `nosiy`The folder that is been provided by the instructor, make sure it is in the same folder with other scripts

  - `utils.py` Contains the filter and image processing functions
  - `task1-plot-outputs` and `task2-plot-outputs` contain the images for the report of my work.
  - the other scripts are for assignments.

## Assignments 

- [Part 1](#part-1)
- [Part 2](#part-2)
- [Part 3](#part-3)
- [How to run](#how-to-run)

### Part 1
Based on a seed, I have chosen 3 random images, and on different kernels/functions, the program randomly picks from those 3 elements.
Aside from learned techniques in the class, I present my own approach for this task, which significantly outperforms other approaches due to the nature of these images.
To simplfy the management of program, I have generated a map that contains method names, which are used for both calling the corresponding functions and generating names for outputs. You can save the result of methods seperately.

### 📚 Filtering Method Mapping and Analysis

1. **Mean Filter**

   _Text: Write your analysis and observations here._

   ![Mean Filter Result](plot_outputs/plot_image1_mean.png)

---

2. **Median Filter**

   _Text: Write your analysis and observations here._

   ![Median Filter Result](plot_outputs/plot_image1_median.png)

---

3. **Gaussian Filter**

   _Text: Write your analysis and observations here._

   ![Gaussian Filter Result](plot_outputs/plot_image1_gaussian.png)

---

4. **Conservative Smoothing**

   _Text: Write your analysis and observations here._

   ![Conservative Smoothing Result](plot_outputs/plot_image1_conservative.png)

---

5. **Crimmins Speckle Removal**

   _Text: Write your analysis and observations here._

   ![Crimmins Filter Result](plot_outputs/plot_image1_crimmins.png)

---

6. **Frequency Low-Pass Filter**

   _Text: Write your analysis and observations here._

   ![Frequency Filter Result](plot_outputs/plot_image1_frequency.png)

---

7. **Laplacian Filter**

   _Text: Write your analysis and observations here._

   ![Laplacian Filter Result](plot_outputs/plot_image1_laplacian.png)

---

8. **Unsharp Filter**

   _Text: Write your analysis and observations here._

   ![Unsharp Filter Result](plot_outputs/plot_image1_unsharp.png)

---

9. **Morphological Opening**

   _Text: Write your analysis and observations here._

   ![Opening Result](plot_outputs/plot_image1_opening.png)

---

10. **Morphological Closing**

   _Text: Write your analysis and observations here._

   ![Closing Result](plot_outputs/plot_image1_closing.png)

---

11. **Aghax Kernel Method**

   _Text: Write your analysis and observations here._

   ![Aghax Filter Result](plot_outputs/plot_image1_aghax.png)

---


### Part 2
In this part, I will only put the best results based on my qualitative analysis, you can run `a2.py` and try for different functions on the speckle images.

### Part 3
Run `a3.py`, as it provides an interactive tool for playing the images as a loop forward and backwards, u can also use the slider for seeing the different images based on slider value.

You can save images after execution, to do so, set `save` variable to. It will save the result image in `outputs\output{assignment_number}\` with given file name using `save_image` function. Alternatively, you can save the output of the plots by setting `save_plot` to True.

## How to run

~~~
git clone https://github.com/ADA-GWU/a3-digital-image-pre-processing-aghayevagha.git
cd a3-digital-image-pre-processing-aghayevagha
~~~

Install the necessary libraries
~~~
pip install opencv-python numpy matplotlib scikit-image scikit-learn
~~~
  - run `a1.py`, `a2.py`, `a3.py` for corresponding parts of the assignments, example:
~~~
python a1.py
~~~
