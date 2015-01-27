#!/usr/bin/env python

import csv
import argparse
import math
import cairocffi as cairo
# import pandas as pd

def main():
  with open('diodes.csv', 'r') as csvfile:
    csvComponents = csv.reader(csvfile, delimiter=',', quotechar='"')
    xMargin = 0.125/2
    yMargin = 0.125/2
    x = 0.5 + xMargin
    y = 0.125 + yMargin
    width = 1.0 - xMargin*2
    height = 1.0 - xMargin*2

    ctx = cairoInitialize()
    csvComponents.next()
    for csvComponent in csvComponents:
      processDiode(ctx, x, y, width, csvComponent)
      break
  
def cairoInitialize():
  surface = cairo.PDFSurface("diodes.pdf", 11*72, 8.5*72)
  # surface = cairo.cairo_ps_surface_create  ("test.ps", WIDTH, HEIGHT)
  # surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
  ctx = cairo.Context (surface)

  ctx.scale (72, 72) # Normalizing the canvas
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

  return ctx

def processDiode(ctx, x, y, width, csvComponent):
  typeMap = {"GENERAL": "diode", "SCHOTTKY": "schottky diode"}
  ctx.select_font_face(family='Asana Math', slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_NORMAL)
  # ctx.select_font_face('Asana Math')
  ctx.set_font_size(0.125) 
  ctx.set_source_rgb(0, 0, 0) 
  (e_x, e_y, e_width, e_height, e_dx, e_dy) = ctx.text_extents(typeMap[csvComponent[1]])
  y += (e_height) * 1.25
  ctx.move_to(x+(width - e_width)/2.0, y) 
  ctx.show_text(typeMap[csvComponent[1]])

  ctx.select_font_face(family='Asana Math', slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_BOLD)
  (e_x, e_y, e_width, e_height, e_dx, e_dy) = ctx.text_extents(csvComponent[0])
  y += (e_height) * 1.25
  ctx.move_to(x+(width - e_width)/2.0, y) 
  ctx.show_text(csvComponent[0])


if __name__ == "__main__":
    main()