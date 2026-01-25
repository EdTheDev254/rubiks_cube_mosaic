import numpy as np
from PIL import Image, ImageDraw

# colors(rubiks cube colors)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# grid line separator
GRAY = (128, 128, 128)


class RubiksMosaicGenerator:
    def __init__(self, image_path, cubes_wide=40):
        self.image_path = image_path
        self.cubes_wide = cubes_wide


        # we load the 6 colors into a numpy array grid(some sort of a computer matrix/ not the movie) for instant calculations
        self.palette = np.array([WHITE, RED, GREEN, BLUE, ORANGE, YELLOW])

        #print(self.palette.shape) shape is (6,3)

    # perform a euclidean difference to find the single closest color to the pixel
    def get_closet_color(self, pixel):
        
        # square to remove negative numbers and sum them horizontally = results in,
        # 6 numbers rep the total error of each of the Rubiks cube color
        distances = np.sqrt(np.sum((self.palette - pixel) ** 2, axis=1)) 

        # Find the index (0-5) of the smallest distance and return that color
        return self.palette[np.argmin(distances)] 




rubiks = RubiksMosaicGenerator('image.jpg')

#print(rubiks.get_closet_color((0, 0, 0))) return the closest color to the pixel



