# rubiks_cube_mosaic
Mapping an image using a Rubiks cube standard colors.

# Sample
For the following original_image I used 100 cubes wide as the var input to atleast see some details from it.

## Original
![](image.png)

<<<<<<< HEAD
## mosaic - 10K cubes used
=======
## mosaic - 100 cubes wide used
>>>>>>> 6a410a3161d2634dbbf6d054ce33df05bbd0195b
![](output.png)

## Additional Info
PS: This code is a little fast because of downscaling the image first, reducing the dataset from millions of pixels to just the target grid size (e.g., 120x90). 

it uses NumPy vectorization to calculate the Euclidean distance for all 6 palette colors and 3 RGB channels simultaneously using (low-level C optimization) - the numpy lib, completely avoiding slow Python loops for the math operations.....

## Using Dithering
Implementing dithering gives the image much more color, but the Floyd-Steinberg will scatter random colored stickers everywhere to try to create subtle color tones. And the low the number of cubes used the worse the image looks compared to the (NN) method. 

PS: Still Learning..

### 900 Cubes(Default)
![](default-900-cubes.png)

### 900 Cubes(Dithered)
![](dithered-900-cubes.png)
