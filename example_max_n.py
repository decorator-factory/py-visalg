from visalg import AlgImage, ImageFont, Array

["Defining the maximum function"]

def get_n_max(img: AlgImage, top: Array, bottom: Array):
    """Get n maximum elements from a non-empty list"""
    n = len(bottom.array)
    if len(top.array)<n:
        raise ValueError("list too small")

    # The smallest possible element is 0
    maximums = bottom.array = [0]*n

    for i, x in enumerate(top.array):
        array_top.highlight["red"] = [i]

        for j, old_max in enumerate(maximums):
            array_bottom.highlight["green"] = [j]
            array_bottom.highlight["green"] = [j]
            img.capture()
            if x > old_max:
                array_bottom.highlight["green"] = []
                array_bottom.highlight["#828749"] = [(j, n)]
                img.capture()
                img.capture()
                maximums.insert(j, x)
                maximums.pop()
                array_bottom.highlight["fuchsia"] = [j]
                array_bottom.highlight["#828749"] = [(j+1, n)]
                img.capture()

                array_bottom.highlight["fuchsia"] = []
                array_bottom.highlight["#828749"] = []
                break
        img.capture()

    return maximums


["Drawing"]

img = AlgImage(740, 192)
font = ImageFont.truetype("consola.ttf", size=48)

array_top = Array(x=16, y=16,
                 length=10, font=font,
                 cell_size=64)

array_bottom = Array(x=16, y=100,
                 length=4, font=font,
                 cell_size=64, outline="#383838")

img << array_top << array_bottom

array_top.array = [9, 5, 3, 4, 8, 6, 1, 2, 7, 0]

[img.capture() for i in range(4)]

get_n_max(img, array_top, array_bottom)

[img.capture() for i in range(4)]

img.save_gif("examples/max_n.gif", duration=400)

