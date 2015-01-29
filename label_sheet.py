#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import cairocffi as cairo

def enum(**enums):
  return type('Enum', (), enums)

FontType = enum(BASIC=1, MAJOR=2)

class LabelText:
  def __init__(self, textType, textString):
    self.textType = textType
    self.textString = textString

class LabelLine:
  def __init__(self, *args):
    self.texts = args
    # if hasattr(args, '__len__'):
    #   self.texts = args
    # else:
    #   # args is a singleton. Assume just a LabelText
    #   self.texts = [args]

class LabelSheet:
  def __init__(self, filename, startCoords = None):
    self.surface = cairo.PDFSurface(filename, self.sheetWidth*72, self.sheetHeight*72)
    # surface = cairo.cairo_ps_surface_create  ("test.ps", WIDTH, HEIGHT)
    # surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    self.ctx = cairo.Context(self.surface)
    self.ctx.scale (72, 72) # Normalizing the canvas

    # self.draw_background_labels()

    self.xCoord, self.yCoord = (0, 0) if not startCoords else startCoords
    self.moveToLabel(self.xCoord, self.yCoord)

  @property
  def sheetWidth(self): return 11.0
  @property
  def sheetHeight(self): return 8.5
  @property
  def labelWidth(self): return 1.0
  @property
  def labelHeight(self): return 2.625
  @property 
  def sheetMarginX(self): return 0.5
  @property 
  def sheetMarginY(self): return 0.125
  @property 
  def labelSpacingX(self): return 0.0
  @property 
  def labelSpacingY(self): return 0.15625
  @property 
  def labelMarginX(self): return 0.125
  @property 
  def labelMarginY(self): return 0.125
  @property 
  def interSublabelGapY(self): return 0.125
  @property
  def fontAscentHeightMult(self): return 1.25

  @property
  def currentLabelX(self):
    return self.sheetMarginX + self.xCoord * (self.labelWidth + self.labelSpacingX)
  @property
  def currentLabelY(self):
    return self.sheetMarginY + self.yCoord * (self.labelHeight + self.labelSpacingY)
  @property
  def maxCoordX(self):
    return (self.sheetWidth - self.sheetMarginX * 2 + self.labelSpacingX) / (self.labelWidth + self.labelSpacingX)
  @property
  def maxCoordY(self):
    return (self.sheetHeight - self.sheetMarginY * 2+ self.labelSpacingY) / (self.labelHeight + self.labelSpacingY)
  @property
  def labelCenterX(self):
    return self.currentLabelX + self.labelWidth / 2.0


  def draw(self, labelLines):
    w, h = self.measureLabelLines(labelLines)
    print("Label measured at %f by %f..." % (w, h)),
    if self.nextY+h > self.currentLabelY+self.labelHeight-self.labelMarginY:
      print "moving to the next label", 
      self.moveToNextLabel()
    self.drawLabelLines(labelLines)
    print "label drawn"

  def moveToLabel(self, newCoordX, newCoordY):
    self.xCoord, self.yCoord = (newCoordX, newCoordY)
    self.nextY = self.currentLabelY + self.sheetMarginY

  def moveToNextLabel(self):
    if (self.xCoord+1 >= self.maxCoordX):
      if (self.yCoord+1 >= self.maxCoordY):
        raise Exception("Can't move the the next label")
      else:
        self.moveToLabel(0, self.yCoord+1)
    else:
      self.moveToLabel(self.xCoord+1, self.yCoord)

  def drawLabelLines(self, labelLines):
    for labelLine in labelLines:
      (w, h) = self.drawLabelLine(labelLine)
      # self.nextY += h
    self.nextY += self.interSublabelGapY

  def measureLabelLines(self, labelLines):
    width = 0
    height = 0
    for labelLine in labelLines:
      w, h = self.measureLabelLine(labelLine)
      width = max(width, w)
      height += h
    return (width, height)

  def drawLabelLine(self, labelLine):
    w, h = self.measureLabelLine(labelLine)
    x = self.labelCenterX - w / 2.0
    self.nextY += h
    for labelText in labelLine.texts:
      w, h = self.measureLabelText(labelText)
      self.drawLabelText(labelText, x, self.nextY)
      x += w
    return (w, h)

  def measureLabelLine(self, labelLine):
    width = 0
    height = 0
    for labelText in labelLine.texts:
      w, h = self.measureLabelText(labelText)
      height = max(height, h)
      width += w
    return (width, height)


  def drawLabelText(self, labelText, x, y):
    self.applyFont(labelText.textType)
    self.ctx.move_to(x, y) 
    self.ctx.show_text(labelText.textString)

  def measureLabelText(self, labelText):
    self.applyFont(labelText.textType)
    (te_x, te_y, te_width, te_height, te_dx, te_dy) = self.ctx.text_extents(labelText.textString)
    (fe_ascent, fe_descent, fe_height, fe_max_x_advance, fe_max_y_advance) = self.ctx.font_extents()
    return (te_width, fe_ascent * self.fontAscentHeightMult)

  def draw_background_labels(self):
    self.ctx.set_source_rgb (0.75,0.75,0.75)
    self.ctx.set_line_width (1.0/72.0/4.0)
    y = 0.125
    h = 2.625
    w = 1
    while y+h<8.5:
      x = 0.5
      for i in range(10):
        # roundedrecA(ctx, x, y, w, h, 0.125/2.0)
        self.ctx.move_to(x,y)
        self.ctx.line_to(x+w,y)
        self.ctx.line_to(x+w,y+h)
        self.ctx.line_to(x,y+h)
        self.ctx.line_to(x,y)
        x+=w
      y+=h+0.125/4.0*5.0

    self.ctx.stroke()



  def applyFont(self, textType):
    if textType == FontType.BASIC:
      self.ctx.select_font_face(family='Asana Math', slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_NORMAL)
      # self.ctx.set_font_size(0.125) 
    elif textType == FontType.MAJOR:
      self.ctx.select_font_face(family='Asana Math', slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_BOLD)
      # self.ctx.set_font_size(0.25) 
    else:
      raise Exception("Unknown font type" + textType)
    self.ctx.set_font_size(0.125) 
    self.ctx.set_source_rgb(0, 0, 0) 

