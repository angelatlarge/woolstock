#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

class LabelText:
  def __init__(self, textType, textString):
    self.textType = textType
    self.textString = textString

  @property
  def leadingSpace(self): return self.textString and len(self.textString) > 0 and self.textString[0] == " "

  @property
  def trailingSpace(self): return self.textString and len(self.textString) > 0 and self.textString[-1] == " "

  @property
  def empty(self): return self.textString

  def measure(self, sheet, scaleFactor = 1.0):
    return sheet.measureText(self.textType, self.textString, scaleFactor)

  def measureSpace(self, sheet, scaleFactor = 1.0):
    return sheet.measureText(self.textType, " ", scaleFactor)

  def draw(self, sheet, x, y, scaleFactor = 1.0):
    return sheet.drawText(self.textType, self.textString, x, y, scaleFactor)

  def __str__(self):
    return "LabelText(%s, %s)" % (self.textType, self.textString)

  def __repr__(self):
    return self.__str__()
