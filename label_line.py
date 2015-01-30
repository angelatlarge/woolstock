#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

class LabelLine:
  def __init__(self, *args):
    self.labelTexts = args
    # if hasattr(args, '__len__'):
    #   self.texts = args
    # else:
    #   # args is a singleton. Assume just a LabelText
    #   self.texts = [args]

  def draw(self, sheet, centerX, startAtY):
    w, h = self.measure(sheet)
    x = centerX - w / 2.0
    y = startAtY + h
    for labelText in self.labelTexts:
      w, h = labelText.measure(sheet)
      labelText.draw(sheet, x, y)
      x += w
    return (w, h)

  def measure(self, sheet):
    width = 0
    height = 0
    for labelText in self.labelTexts:
      w, h = labelText.measure(sheet)
      height = max(height, h)
      width += w
    return (width, height)
