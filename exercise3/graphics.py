import threading
from typing import Callable, Any
import math
from math import floor, ceil
from PIL import Image, ImageDraw, ImageFont

from .solution import HexMazeState

sixty = math.radians(60)
thirty = math.radians(30)

def hexagon_points(x: float, y: float, edge_length: float) -> None:
    for angle in range(0, 360, 60):
        yield x + math.cos(math.radians(angle + 30))*edge_length
        yield y + math.sin(math.radians(angle + 30))*edge_length

def draw_hexagon(im: Image, x: float, y: float, edge_length: float, fill: Any = None) -> None:

    draw = ImageDraw.Draw(im)

    draw.polygon(list(hexagon_points(x,y, edge_length)), fill=fill, outline="#000", width=2)

def draw_hexgrid_state(grid: HexMazeState, edge_length: float = 50, decide_fill: Callable[[int, int], Any] = lambda _1, _2: '#fff') -> Image:
    hex_grid = grid.maze

    # Half the length of a hexagon itselff
    half_length = edge_length*math.cos(thirty)

    rows, cols = len(hex_grid), len(hex_grid[0])

    border = 10
    offset_x = 2*half_length + border
    offset_y = edge_length + border

    # Calculating w:
    w = offset_x + (2*(cols-1) + 1)*half_length + border
    # Calculating h:
    # We will have floor(rows/2) even honeycombs and ceil(rows/2) odd ones
    # For each odd one we add 2*edge_length, and for each even one we add 1*edge_length.
    # If even number of rows (thus row+1%2==0), we also add sin(30)*edge_length = 0.5*edge_length in the end
    h = (floor(rows/2)*1 + ceil(rows/2)*2 + ((rows+1)%2)*0.5) * edge_length + 2*border

    im = Image.new("RGB", (int(w), int(h)), color=(255, 255, 255))

    for row in range(rows):
        for col in range(cols):
            x = col * 2 * half_length - row%2*half_length
            y = row * edge_length * 3/2

            x += offset_x
            y += offset_y 

            draw_hexagon(im, x, y, edge_length=edge_length, fill=decide_fill(row, col))
    
    return im