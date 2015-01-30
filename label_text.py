#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

class LabelText:
  def __init__(self, textType, textString):
    self.textType = textType
    self.textString = textString

  def measure(self, sheet):
    return sheet.measureText(self.textType, self.textString)

  def draw(self, sheet, x, y):
    return sheet.drawText(self.textType, self.textString, x, y)
