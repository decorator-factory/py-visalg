# py-visalg
Algorithm visualization library for Python.

## Documentation

### The `AlgImage` object

This is a host object or a 'canvas' for all the visual elements.

####Attributes
* `width`, `height` — width and height of the image (in pixels)
* `bgcolor` — the background color (in PIL format)
* `frames` — a list with all the captured frames

####Methods
* `capture()` — save a frame to `frames`

* `save_png(folder, prefix)` — save the frames as individual PNG 
files:`folder/prefix0.png`, `folder/prefix1.png` and so on.

* `save_gif(filename)` — save the frames as a GIF animation

* `connect(obj)` and `disconnect(obj)` — connect a visual element to the canvas.
`<<` and `>>` are aliases for `connect` and `disconnect`, so you can do something
like:  
  `image << array_top << grid << array_cache`

####Explanation
When you call `AlgImage.capture()`, the `AlgImage` object iterates over all the
visual elements and renders them by providing them with handlers to the image.

---

### The `AlgElement` object
`AlgElement` is a parent object for all the visual elements like cells, arrays,
grids and so on. 

####Methods

* `render(image, draw)` — render the element to an image. `image` is a `PIL.Image`
object, and `draw` is a `PIL.ImageDraw` object for that image.

* `on_connect(parent)`, `on_disconnect(parent)` — these methods are called when
(just before) the element gets connected to or disconnected from an `AlgImage`.

---

### The `Cell` object

####Attributes

* `x`, `y` — position of the top left corner of the cell (in pixels)
* `width`, `height` — width and height of the cell (in pixels)
* `font` — a `PIL.ImageFont` object that will be used to draw the text   


* `margin` — border thickness of the cell
* `fill`, `outline` — colors (in PIL format) for the inner and outer rectangles of the cell
* `textcolor` is the color of the cell
* `contents` — an object that supports `str` or a `ColorFill` object. This is what's shown inside the cell

## Examples

### Bubble sort
See `example_bubblesort.py`

![Bubble sort](https://github.com/decorator-factory/py-visalg/blob/master/visalg/examples/bubblesort.gif?raw=true)

### Finding top N numbers in an array
See `example_max_n.py`

![Top N numbers](https://github.com/decorator-factory/py-visalg/blob/master/visalg/examples/max_n.gif?raw=true)

### Solving a maze
See `example_maze.py`

![Maze solving](https://github.com/decorator-factory/py-visalg/blob/master/visalg/examples/maze.gif?raw=true)

