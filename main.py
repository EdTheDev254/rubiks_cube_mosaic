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
CUBE_BORDER = (128, 128, 128)
STICKER_BORDER = (0, 0, 0)


class RubiksMosaicGenerator:
    def __init__(self, image_path, cubes_wide=40):
        self.image_path = image_path
        self.cubes_wide = cubes_wide


        # we load the 6 colors into a numpy array grid(some sort of a computer matrix/ not the movie) for instant calculations
        self.palette = np.array([WHITE, RED, GREEN, BLUE, ORANGE, YELLOW])

        #print(self.palette.shape) shape is (6,3)

    # perform a euclidean difference to find the single closest color to the pixel
    def get_closest_color(self, pixel): #typo haha
        
        # square to remove negative numbers and sum them horizontally = results in,
        # 6 numbers rep the total error of each of the Rubiks cube color
        distances = np.sqrt(np.sum((self.palette - pixel) ** 2, axis=1)) 

        # Find the index (0-5) of the smallest distance and return that color
        return self.palette[np.argmin(distances)] 
    

    def generate_mosaic(self, output_scale=10):
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

        # create a blank canvas (matrix) of zeros with the exact same shape as our image....
        mosaic_array = np.zeros_like(image_array)


        for row in range(target_height):# row 
            for col in range(target_width): # column
                
                pixel = image_array[row, col] # get pixel color
                
                closest = self.get_closest_color(pixel) # find closest color
                
                # We write the closest color into the specific slot on the blank canvas.
                mosaic_array[row, col] = closest 

        # .astype('uint8') ensures the numbers are standard (0-255) image colors.
        mosaic_img = Image.fromarray(mosaic_array.astype('uint8'))

        # upscale
        final_width = target_width * output_scale
        final_height = target_height * output_scale
        
        # nearest for pixelated/hard edges
        final_img = mosaic_img.resize((final_width, final_height), resample=Image.NEAREST)

        # We prepare the image for drawing.

        draw = ImageDraw.Draw(final_img)
        
        # Added these for aesthetics purposes :D
        # These lines separate every single individual color patch.
        for x in range(0, final_width + 1, output_scale):
            draw.line([(x, 0), (x, final_height)], fill=STICKER_BORDER, width=1)
            
        for y in range(0, final_height + 1, output_scale):
            draw.line([(0, y), (final_width, y)], fill=STICKER_BORDER, width=1)

        # separte the cubes
        # These lines separate the physical 3x3 cubes.
        cube_pixel_size = 3 * output_scale
        
        # Draw the internal lines only (skipping the edges)
        for x in range(cube_pixel_size, final_width, cube_pixel_size):
            draw.line([(x, 0), (x, final_height)], fill=CUBE_BORDER, width=3)
            
        for y in range(cube_pixel_size, final_height, cube_pixel_size):
            draw.line([(0, y), (final_width, y)], fill=CUBE_BORDER, width=3)

        # Draw the outer border using a rectangle so the width falls inside the image
        draw.rectangle([(0, 0), (final_width - 1, final_height - 1)], outline=CUBE_BORDER, width=3)

        return final_img
    

if __name__ == "__main__":
    input_file = 'image.png'
    
    print(f"Processing {input_file}........")

    generator = RubiksMosaicGenerator(input_file, cubes_wide=100) # cubes_wide is the number of cubes
    
    result = generator.generate_mosaic(output_scale=10) # output_scale is the pixel size
    
    if result:
        result.save('output.png')
        print("Success! ...Saved as 'rubiks_mosaic_output.png'")
        result.show()

#print(rubiks.get_closet_color((0, 0, 0))) return the closest color to the pixel

#print(rubiks.generate_mosaic())




