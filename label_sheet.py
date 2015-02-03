#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import cairocffi as cairo

def enum(**enums):
  return type('Enum', (), enums)

FontType = enum(BASIC=1, MAJOR=2, MINOR=3, MINORHEADING=4)

class LabelSheet:
  def __init__(self, filename, startCoords = None, exclusions=[]):
    self.surface = cairo.PDFSurface(filename, self.sheetWidth*72, self.sheetHeight*72)
    # surface = cairo.cairo_ps_surface_create  ("test.ps", WIDTH, HEIGHT)
    # surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    self.ctx = cairo.Context(self.surface)
    self.ctx.scale (72, 72) # Normalizing the canvas

    self.xCoord, self.yCoord = (0, 0) if not startCoords else startCoords
    self.moveToLabel(self.xCoord, self.yCoord)

    self.exclusions = exclusions

  @property
  def baseFontFace(self): return "Bitstream Charter"
  @property
  def baseFontSize(self): return 0.1
  # def baseFontSize(self): return 0.18
  @property
  def minorFontSize(self): return 0.08
  # def minorFontSize(self): return 0.18
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
  @property
  def printableLabelWidth(self): return self.labelWidth - (self.labelMarginX * 2)


  def draw(self, labelBlock):
    if labelBlock:
      w, h = labelBlock.measure(self)
      # print("Label measured at %f by %f..." % (w, h)),
      if self.nextY+h > self.currentLabelY+self.labelHeight-self.labelMarginY:
        # print "moving to the next label", 
        self.moveToNextLabel()
      (w, h) = labelBlock.draw(self, self.labelCenterX, self.nextY)
      self.nextY += h
      self.nextY += self.interSublabelGapY
      # print "label drawn"
    # else:
      # print "no label"

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

    if (self.xCoord, self.yCoord) in self.exclusions: 
      self.moveToNextLabel()

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

  def measureText(self, textType, textString, scaleFactor = 1.0):
    self.applyFont(textType, scaleFactor)
    (te_x, te_y, te_width, te_height, te_dx, te_dy) = self.ctx.text_extents(textString)
    (fe_ascent, fe_descent, fe_height, fe_max_x_advance, fe_max_y_advance) = self.ctx.font_extents()
    return (te_width, fe_ascent * self.fontAscentHeightMult, te_dx)

  def drawText(self, textType, textString, x, y, scaleFactor = 1.0):
    self.applyFont(textType, scaleFactor)
    self.ctx.move_to(x, y) 
    self.ctx.show_text(textString)

  def applyFont(self, textType, scaleFactor = 1.0):
    if textType == FontType.BASIC:
      self.ctx.select_font_face(family=self.baseFontFace, slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_NORMAL)
      self.ctx.set_font_size(self.baseFontSize * scaleFactor) 
    elif textType == FontType.MAJOR:
      self.ctx.select_font_face(family=self.baseFontFace, slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_BOLD)
      self.ctx.set_font_size(self.baseFontSize * scaleFactor) 
    elif textType == FontType.MINOR:
      self.ctx.select_font_face(family=self.baseFontFace, slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_NORMAL)
      self.ctx.set_font_size(self.minorFontSize * scaleFactor) 
    elif textType == FontType.MINORHEADING:
      self.ctx.select_font_face(family=self.baseFontFace, slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_BOLD)
      self.ctx.set_font_size(self.minorFontSize * scaleFactor) 
    else:
      raise Exception("Unknown font type" + textType)
    self.ctx.set_source_rgb(0, 0, 0) 

