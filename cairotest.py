#!/usr/bin/env python

import math
# import cairo
import cairocffi as cairo

def main():
  surface = cairo.PDFSurface("test.pdf", 11*72, 8.5*72)
  # surface = cairo.cairo_ps_surface_create  ("test.ps", WIDTH, HEIGHT)
  # surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
  ctx = cairo.Context (surface)

  ctx.scale (72, 72) # Normalizing the canvas

  # pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
  # pat.add_color_stop_rgba (1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
  # pat.add_color_stop_rgba (0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity

  # ctx.rectangle (0, 0, 11, 8.5) # Rectangle(x0, y0, x1, y1)
  # ctx.set_source (pat)
  # ctx.fill ()

  ctx.set_source_rgb (0.75,0.75,0.75)
  ctx.set_line_width (1.0/72.0/4.0)
  y = 0.125
  h = 2.625
  w = 1
  while y+h<8.5:
    x = 0.5
    for i in range(10):
      # roundedrecA(ctx, x, y, w, h, 0.125/2.0)
      ctx.move_to(x,y)
      ctx.line_to(x+w,y)
      ctx.line_to(x+w,y+h)
      ctx.line_to(x,y+h)
      ctx.line_to(x,y)
      x+=w
    y+=h+0.125/4.0*5.0

  ctx.stroke ()


  # ctx.set_line_width (1.0/72)
  # y = 0.125
  # while y<8.5:
  #   ctx.move_to(0, y)
  #   ctx.line_to(11, y)
  #   y += 1
  # ctx.stroke ()


  # ctx.set_line_width (0.125)
  # ctx.set_source_rgb (0,0,0)
  # roundedrecA(ctx, 0.125, 0.5, 2.125, 1, 0.125)
  # roundedrecA(ctx, 2, 2, 2.125, 1, 0.125)

  # ctx.move_to(
  # pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
  # pat.add_color_stop_rgba (1, 0.7, 0, 0, 0.5) # First stop, 50% opacity
  # pat.add_color_stop_rgba (0, 0.9, 0.7, 0.2, 1) # Last stop, 100% opacity

  # ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
  # ctx.set_source (pat)
  # ctx.fill ()

  # ctx.translate (0.1, 0.1) # Changing the current transformation matrix

  # ctx.move_to (0, 0)
  # ctx.arc (0.2, 0.1, 0.1, -math.pi/2, 0) # Arc(cx, cy, radius, start_angle, stop_angle)
  # ctx.line_to (0.5, 0.1) # Line to (x,y)
  # ctx.curve_to (0.5, 0.2, 0.5, 0.4, 0.2, 0.8) # Curve(x1, y1, x2, y2, x3, y3)
  # ctx.close_path ()

  # ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
  # ctx.set_line_width (0.02)
  # ctx.stroke ()

  # font = cairo.ToyFontFace(family='Asana Math', slant=FONT_SLANT_NORMAL, weight=FONT_WEIGHT_NORMAL)
  ctx.select_font_face('Asana Math')
  ctx.set_font_size(1) # em-square height is 90 pixels
  ctx.move_to(2, 2) # move to point (x, y) = (10, 90)
  ctx.set_source_rgb(0, 0, 0) # yellow
  ctx.show_text('Hello World')

  # surface.write_to_png ("example.png") # Output to PNG

def roundedrecA(cr,x,y,width,height,radius=5):
  #/* a custom shape, that could be wrapped in a function */
  #radius = 5  #/*< and an approximate curvature radius */        
  x0       = x+radius/2.0   #/*< parameters like cairo_rectangle */
  y0       = y+radius/2.0
  rect_width  = width - radius
  rect_height = height - radius

  cr.save()
  #cr.set_line_width (0.04)
  #self.snippet_normalize (cr, width, height)

  x1=x0+rect_width
  y1=y0+rect_height
  #if (!rect_width || !rect_height)
  #    return
  if rect_width/2<radius:
    if rect_height/2<radius:
      cr.move_to  (x0, (y0 + y1)/2)
      cr.curve_to (x0 ,y0, x0, y0, (x0 + x1)/2, y0)
      cr.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
      cr.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
      cr.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
    else:
      cr.move_to  (x0, y0 + radius)
      cr.curve_to (x0 ,y0, x0, y0, (x0 + x1)/2, y0)
      cr.curve_to (x1, y0, x1, y0, x1, y0 + radius)
      cr.line_to (x1 , y1 - radius)
      cr.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
      cr.curve_to (x0, y1, x0, y1, x0, y1- radius)

  else:
    if rect_height/2<radius:
      cr.move_to  (x0, (y0 + y1)/2)
      cr.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
      cr.line_to (x1 - radius, y0)
      cr.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
      cr.curve_to (x1, y1, x1, y1, x1 - radius, y1)
      cr.line_to (x0 + radius, y1)
      cr.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
    else:
      cr.move_to  (x0, y0 + radius)
      cr.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
      cr.line_to (x1 - radius, y0)
      cr.curve_to (x1, y0, x1, y0, x1, y0 + radius)
      cr.line_to (x1 , y1 - radius)
      cr.curve_to (x1, y1, x1, y1, x1 - radius, y1)
      cr.line_to (x0 + radius, y1)
      cr.curve_to (x0, y1, x0, y1, x0, y1- radius)

  cr.close_path ()

  cr.restore()

if __name__ == "__main__":
    main()  