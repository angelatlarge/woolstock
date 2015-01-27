#!/usr/bin/env python

import math
# import cairo
import cairocffi as cairo

WIDTH, HEIGHT = 72*5, 72*5

surface = cairo.PDFSurface("test.pdf", WIDTH, HEIGHT)
# surface = cairo.cairo_ps_surface_create  ("test.ps", WIDTH, HEIGHT)
# surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context (surface)

ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas

pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
pat.add_color_stop_rgba (1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
pat.add_color_stop_rgba (0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity

ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
ctx.set_source (pat)
ctx.fill ()

ctx.translate (0.1, 0.1) # Changing the current transformation matrix

ctx.move_to (0, 0)
ctx.arc (0.2, 0.1, 0.1, -math.pi/2, 0) # Arc(cx, cy, radius, start_angle, stop_angle)
ctx.line_to (0.5, 0.1) # Line to (x,y)
ctx.curve_to (0.5, 0.2, 0.5, 0.4, 0.2, 0.8) # Curve(x1, y1, x2, y2, x3, y3)
ctx.close_path ()

ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
ctx.set_line_width (0.02)
ctx.stroke ()

# font = cairo.ToyFontFace(family='Asana Math', slant=FONT_SLANT_NORMAL, weight=FONT_WEIGHT_NORMAL)
ctx.select_font_face('Asana Math')
ctx.set_font_size(0.25) # em-square height is 90 pixels
ctx.move_to(0.1, 0.1) # move to point (x, y) = (10, 90)
ctx.set_source_rgb(0, 0, 0) # yellow
ctx.show_text('Hello World')

# surface.write_to_png ("example.png") # Output to PNG
