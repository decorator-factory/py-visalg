from visalg import AlgImage, ImageFont, Array

img = AlgImage(740, 96)
font = ImageFont.truetype("consola.ttf", size=48)

array = Array(x=16, y=16,
              length=10, font=font,
              cell_size=64)
img << array

A = array.array = [9, 5, 3, 4, 8, 6, 1, 2, 7, 0]

for i in range(9):
    array.highlight["red"] = [i]
    img.capture()

    for j in range(i+1, 10):
        array.highlight["green"] = [j]
        img.capture()

        if A[j] < A[i]:
            A[i], A[j] = A[j], A[i]

            array.highlight["fuchsia"] = [i, j]

            img.capture()

            array.highlight["fuchsia"] = []
            array.highlight["red"] = [i]


    img.capture()
    img.capture()

[img.capture() for i in range(4)]

img.save_gif("examples/bubblesort.gif", duration=350)

