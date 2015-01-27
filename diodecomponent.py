#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import cairocffi as cairo

class DiodeComponent:
  def __init__(self, propertiesDict):
    self.propertiesDict = propertiesDict

  def draw(self, ctx, x, y, width):
    return self._process(ctx, x, y, width, True)

  def measure(self, ctx, x, y, width):
    return self._process(ctx, x, y, width, False)

  def _process(self, ctx, x, y, width, draw):
    typeMap = {"GENERAL": "diode", "SCHOTTKY": "schottky diode"}


    ctx.select_font_face(family='Asana Math', slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_NORMAL)
    # ctx.select_font_face('Asana Math')
    ctx.set_font_size(0.125) 
    ctx.set_source_rgb(0, 0, 0) 
    (e_x, e_y, e_width, e_height, e_dx, e_dy) = ctx.text_extents(typeMap[self.propertiesDict["Type"]])
    (fe_ascent, fe_descent, fe_height, fe_max_x_advance, fe_max_y_advance) = ctx.font_extents()
    y += (fe_ascent) * 1.00
    ctx.move_to(x+(width - e_width)/2.0, y) 
    if draw: ctx.show_text(typeMap[self.propertiesDict["Type"]])
    # y += (fe_descent) * 1.00

    ctx.select_font_face(family='Asana Math', slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_BOLD)
    (e_x, e_y, e_width, e_height, e_dx, e_dy) = ctx.text_extents(self.propertiesDict["ID"])
    (fe_ascent, fe_descent, fe_height, fe_max_x_advance, fe_max_y_advance) = ctx.font_extents()
    y += (fe_ascent) * 1.5
    ctx.move_to(x+(width - e_width)/2.0, y) 
    if draw: ctx.show_text(self.propertiesDict["ID"])
    # y += (fe_descent) * 1.00

    ctx.select_font_face(family='Asana Math', slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_NORMAL)
    specs = []

    specs.append(self.propertiesDict["Vmax, V"] + "V")

    iMax = float(self.propertiesDict["Imax, A"])
    iMaxText = str(iMax) + "A" if iMax >= 1 else str(int(iMax * 1000)) + "mA"
    specs.append(iMaxText)
    
    if (self.propertiesDict["Recovery time, ns"]):
      time = long(self.propertiesDict["Recovery time, ns"])
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
