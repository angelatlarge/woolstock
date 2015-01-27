#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import csv
import argparse
import math
import cairocffi as cairo
# import pandas as pd

def main():
  # csvComponents = pd.read_csv('diodes.csv')
  # for csvComponent in csvComponents:
  #   print csvComponent

  with open('diodes.csv', 'r') as csvfile:
    csvComponents = csv.DictReader(csvfile)
    # csvComponents = csv.reader(csvfile, delimiter=',', quotechar='"')
    labelWidth = 1
    labelHeight = 2.625
    labelsStartY = 0.125
    labelsStartX = 0.5

    xMargin = 0.125/2
    yMargin = 0.125/2

    labelStartY = labelsStartY
    labelStartX = labelsStartX
    labelEndY = labelsStartY + labelHeight
    labelEndX = labelsStartX + labelWidth
    x = labelsStartX + xMargin
    y = labelStartY + yMargin
    availableWidth = labelWidth - xMargin*2
    height = 1.0 - xMargin*2
    interComponentMargin = .125

    ctx = cairoInitialize()
    # csvComponents.next()
    csvComponent = csvComponents.next()
    try:
      while csvComponent:
        newY = processDiode(ctx, x, y, availableWidth, csvComponent, False)
        if newY < labelEndY - yMargin:
          processDiode(ctx, x, y, availableWidth, csvComponent, True)
          y = newY + interComponentMargin
          csvComponent = csvComponents.next()
        else:
          y = labelStartY + yMargin
          labelsStartX += labelWidth
          x = labelsStartX + xMargin
    except StopIteration:
      pass
  
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

def processDiode(ctx, x, y, width, csvComponent, draw):
  typeMap = {"GENERAL": "diode", "SCHOTTKY": "schottky diode"}


  ctx.select_font_face(family='Asana Math', slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_NORMAL)
  # ctx.select_font_face('Asana Math')
  ctx.set_font_size(0.125) 
  ctx.set_source_rgb(0, 0, 0) 
  (e_x, e_y, e_width, e_height, e_dx, e_dy) = ctx.text_extents(typeMap[csvComponent["Type"]])
  (fe_ascent, fe_descent, fe_height, fe_max_x_advance, fe_max_y_advance) = ctx.font_extents()
  y += (fe_ascent) * 1.00
  ctx.move_to(x+(width - e_width)/2.0, y) 
  # glyphs.append(ctx.text_to_glyphs(xStart, y, typeMap[csvComponent["Type"]]))
  if draw: ctx.show_text(typeMap[csvComponent["Type"]])
  # y += (fe_descent) * 1.00

  ctx.select_font_face(family='Asana Math', slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_BOLD)
  (e_x, e_y, e_width, e_height, e_dx, e_dy) = ctx.text_extents(csvComponent["ID"])
  (fe_ascent, fe_descent, fe_height, fe_max_x_advance, fe_max_y_advance) = ctx.font_extents()
  y += (fe_ascent) * 1.5
  ctx.move_to(x+(width - e_width)/2.0, y) 
  # glyphs.append(ctx.text_to_glyphs(xStart, y, csvComponent["ID"]))
  if draw: ctx.show_text(csvComponent["ID"])
  # y += (fe_descent) * 1.00

  ctx.select_font_face(family='Asana Math', slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_NORMAL)
  specs = []

  specs.append(csvComponent["Vmax, V"] + "V")

  iMax = float(csvComponent["Imax, A"])
  iMaxText = str(iMax) + "A" if iMax >= 1 else str(int(iMax * 1000)) + "mA"
  specs.append(iMaxText)
  
  if (csvComponent["Recovery time, ns"]):
    time = long(csvComponent["Recovery time, ns"])
    timeText = str(time) + "ns" if time < 1000 else str(time/1000) + "μs"
    specs.append(timeText)

  specsText = " ".join(specs)
  (e_x, e_y, e_width, e_height, e_dx, e_dy) = ctx.text_extents(specsText)
  (fe_ascent, fe_descent, fe_height, fe_max_x_advance, fe_max_y_advance) = ctx.font_extents()
  y += (fe_ascent) * 1.5
  xStart = x+(width - e_width)/2.0
  ctx.move_to(xStart, y) 
  
  # glyphs.append(ctx.text_to_glyphs(xStart, y, specsText))
  if draw: ctx.show_text(specsText)

  # ctx.move_to(xStart, y-fe_ascent) 
  # ctx.line_to(xStart+e_width, y-fe_ascent) 
  # ctx.line_to(xStart+e_width, y-fe_ascent+fe_height) 
  # ctx.line_to(xStart, y+fe_descent) 
  # ctx.line_to(xStart, y-fe_ascent) 
  # ctx.stroke()
  # ctx.move_to(xStart, y) 
  # ctx.line_to(xStart+e_width, y) 
  # ctx.stroke()

  # y += (fe_descent) * 1.00

  # ctx.move_to(x+(width - e_width)/2.0, y) 
  # ctx.line_to(x+e_width, y) 
  # ctx.line_to(x+e_width, y+e_height) 
  # ctx.line_to(x, y+e_height) 
  # ctx.line_to(x, y) 
  # ctx.stroke()

  # ctx.move_to(x+(width - e_width)/2.0, y) 
  # ctx.line_to(x+e_width, y) 
  # ctx.line_to(x+e_width, y+e_y) 
  # ctx.line_to(x, y+e_y) 
  # ctx.line_to(x, y) 
  # ctx.stroke()

  return y

if __name__ == "__main__":
    main()