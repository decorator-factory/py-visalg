from visalg import AlgImage, ImageFont, Array

# AlgImage is the 'canvas' where everything will be drawn
img = AlgImage(740, 96)

# Load the font 'Consolas'
font = ImageFont.truetype("consola.ttf", size=48)

# Array is a container of cells
array = Array(x=16, y=16,
              length=10, font=font,
              cell_size=64)

# Connect the array to the canvas
img << array

# A and array.array will refer to the same newly created object
A = array.array = [9, 5, 3, 4, 8, 6, 1, 2, 7, 0]


# Here the algorithm begins:

for i in range(9):
    # Highlight a single cell:
    array.highlight["red"] = [i]

    # Capture a frame and save it:
    img.capture()

    for j in range(i+1, 10):
        array.highlight["green"] = [j]
        img.capture()

        if A[j] < A[i]:
            A[i], A[j] = A[j], A[i]

            # Reset the highlighting
            array.highlight["red"] = []
            array.highlight["green"] = []
            # Highlight two cells:
            array.highlight["fuchsia"] = [i, j]

            img.capture()

            # Highlight the first cell with red again
            array.highlight["fuchsia"] = []
            array.highlight["red"] = [i]

    # Make a small pause at the end of each outer iteration
    img.capture()
    img.capture()

# Make a 4-frame pause at the end of the animation
[img.capture() for i in range(4)]

# Save the frames as a gif animation
# Duration is the time each frame will appear for (in milliseconds)
img.save_gif("examples/bubblesort.gif", duration=350)

del img