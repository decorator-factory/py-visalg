from PIL import Image, ImageDraw, ImageFont
import os.path as path
from dataclasses import dataclass


class AlgImage:
    def __init__(self, width, height,
                 bgcolor=(255, 255, 255)):
        """A host object for the visualisation

        'alg_image << thing' will first call thing.on_connect(alg_image),
        then connect thing to alg_image. The same goes for >> and
        on_disconnect."""
        self.width = width
        self.height = height
        self.bgcolor = bgcolor
        self.image = Image.new('RGB', (width, height), self.bgcolor)
        self.draw = ImageDraw.Draw(self.image)

        self.children = []
        self.frame = 0
        self.frames = []


    def __lshift__(self, other):
        # add an element
        # img << elm1 << elm2 << ...
        if not isinstance(other, AlgElement):
            raise TypeError(other)

        other.on_connect(self)
        self.children.append(other)

        return self


    def __rshift__(self, other):
        # remove an element
        # img >> elm1 >> elm2 >> ...
        if not isinstance(other, AlgElement):
            raise TypeError(other)

        other.on_disconnect(self)
        if other in self.children:
            self.children.remove(other)

        return self

    connect = __lshift__
    disconnect = __rshift__


    def capture(self):
        self.draw.rectangle((0, 0, self.width, self.height),
                            fill=self.bgcolor)

        for child in self.children:
            child.render(self.image, self.draw)

        self.frame += 1
        self.frames.append(self.image.copy())

    def save_png(self, folder="img/", prefix="frame_"):
        for n, frame in enumerate(self.frames):
            filename = path.join(folder,
                                 prefix + str(n) + ".png")
            frame.save(filename)

    def save_gif(self, filename, duration=200):
        self.frames[0].save(filename, format="GIF",
                            append_images=self.frames[1:],
                            save_all=True,
                            duration=duration,
                            loop=0)


class AlgElement:
    def render(self, image, draw):
        pass

    def on_connect(self, parent):
        pass

    def on_disconnect(self, parent):
        pass


@dataclass
class Rectangle(AlgElement):
    x: int
    y: int
    width: int
    height: int
    fill: tuple = (255, 255, 255)
    outline: tuple = (0, 0, 0)

    def render(self, image, draw):
        draw.rectangle([self.x, self.y,
                        self.x + self.width, self.y + self.height],
                       fill=self.fill, outline=self.outline)

    @property
    def center(self):
        return (self.x + self.width // 2,
                self.y + self.height // 2)

@dataclass
class Cell(AlgElement):
    x: int
    y: int
    width: int
    height: int
    font: ImageFont

    margin: int = 8
    fill: tuple = (255, 255, 255)
    outline: tuple = (0, 0, 0)
    textcolor: tuple = (0, 0, 0)
    contents: str = ""


    def __post_init__(self):
        m = self.margin
        """
        ++++++++
        ++++++++<-- rect_outer (+)
        ++####++
        ++####<-- rect_inner (#) 
        ++####++
        ++++++++
        ++++++++
        """
        self.rect_outer = Rectangle(self.x, self.y,
                                    self.width, self.height,
                                    fill=self.outline, outline=self.outline)

        self.rect_inner = Rectangle(self.x + m, self.y + m,
                                    self.width - m*2, self.height - m*2,
                                    fill=self.fill, outline=self.fill)


    def render(self, image, draw):
        outer = self.rect_outer
        inner = self.rect_inner
        outer.outline = outer.fill = self.outline
        inner.outline = inner.fill = self.fill

        outer.render(image, draw)
        inner.render(image, draw)

        #print(f"render {self.contents} at {self.center}")
        w, h = draw.textsize(self.contents, self.font)
        draw.text((self.center[0]-w//2, self.center[1]-h//2),
                  self.contents,
                  fill=self.textcolor,
                  font=self.font)

    @property
    def center(self):
        return (self.x + self.width//2,
                self.y + self.height//2)



@dataclass()
class Array(AlgElement):
    x: int
    y: int
    length: int
    font: ImageFont
    cell_size: int = 96
    intercell_space: int = 8
    vertical: bool = False
    pointer: int = None
    pointer_size: int = 8
    pointer_color: tuple = (0, 0, 0)
    fill: object = (255, 255, 255)
    outline: object = (0, 0, 0)

    def __post_init__(self):
        self.highlight = {}
        self.cells = []

        px = self.x
        py = self.y
        step = self.cell_size + self.intercell_space

        for n in range(self.length):
            cell = Cell(px, py,
                        self.cell_size, self.cell_size,
                        font=self.font)
            self.cells.append(cell)

            if self.vertical:
                py += step
            else:
                px += step

        self.array = [0]*self.length


    def render(self, image, draw):
        cells_to_highlight = {}

        # a -- just a
        # [a, b] -- from a to b

        for color, region in self.highlight.items():
            _cells = cells_to_highlight[color] = set()
            for thing in region:
                if isinstance(thing, int):
                    _cells.add(thing)

                elif isinstance(thing, (list, tuple)):
                    for x in range(thing[0], thing[1]+1):
                        _cells.add(x)

                else:
                    raise ValueError(thing)


        for n, cell in enumerate(self.cells):
            value = self.array[n]

            if value is None:
                cell.contents = ""
            else:
                cell.contents = str(value)

            cell.outline = self.outline
            cell.textcolor = self.outline
            cell.fill = self.fill

            for color, cells_set in cells_to_highlight.items():
                if n in cells_set:
                    cell.outline = cell.textcolor    = color

            cell.render(image, draw)

        if self.pointer is not None:
            px = self.x
            py = self.y
            ps = self.pointer_size
            step = self.cell_size + self.intercell_space

            if self.vertical:
                px -= self.intercell_space
                py += self.cell_size//2
                py += self.pointer * step
                point_a = (px, py)
                point_b = (px - ps, py + ps)
                point_c = (px - ps, py - ps)
            else:
                py -= self.intercell_space
                px += self.cell_size // 2
                px += self.pointer * step
                point_a = (px, py)
                point_b = (px - ps, py - ps)
                point_c = (px + ps, py - ps)

            draw.polygon([point_a, point_b, point_c],
                         fill=self.pointer_color)


@dataclass()
class Grid(AlgElement):
    x: int
    y: int
    font: ImageFont
    width: int
    height: int
    cell_size: int = 96
    intercell_space: int = 8

    def __post_init__(self):
        self.rows = []
        px = self.x
        py = self.y
        step = self.cell_size + self.intercell_space

        for i in range(self.height):
            row = Array(px, py, self.width,
                        cell_size=self.cell_size,
                        intercell_space=self.intercell_space)
            self.rows.append(row)


    def __getitem__(self, index:(int, int)):
        x, y = index
        return self.rows[y].contents[x]