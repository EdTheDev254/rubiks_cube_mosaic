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
    

    def generate_mosaic(self):
        try:
            original_image = Image.open(self.image_path)
        except FileNotFoundError:
            print(f"File not found: {self.image_path}")
            return None
        
        # 1 cube wide = 3 stickers // WIDTH
        target_width = self.cubes_wide * 3


        #height to match the aspect ratio
        aspect_ratio = original_image.width / original_image.height
        target_height = int(target_width / aspect_ratio)

        # We need the height to be perfectly divisible by 3
        # Because we cannot have a row of partial cubes at the end
        # We strip off the remainder to ensure we have full 3x3 blocks

        remainder = target_height % 3
        target_height = target_height - remainder

        print(f"Grid Size: {target_width}x{target_height} stickers.")
        print(f"Total Physical Cubes: {self.cubes_wide} x {target_height // 3}")

        # downscale the Image(pixelated)
        # shrink the photo so that 1 pixel = 1 sticker.
        # example - If we want a 1x1 Cube mosaic, this creates a 3x3 pixel image.
        image_small = original_image.resize((target_width, target_height), resample=Image.BILINEAR)

        image_array = np.array(image_small)

        

rubiks = RubiksMosaicGenerator('image.png')

#print(rubiks.get_closet_color((0, 0, 0))) return the closest color to the pixel

print(rubiks.generate_mosaic())


