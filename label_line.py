#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

class LabelLine(object):
  def __init__(self, *args):
    self.labelTexts = args

class SingleLabelLine(LabelLine):

  def draw(self, sheet, centerX, startAtY):
    w, h = self.measure(sheet)
    x = centerX - w / 2.0
    y = startAtY + h
    lastSpaceW = None
    lastText = None
    for labelText in self.labelTexts:
      if labelText:
        w, h, _ = labelText.measure(sheet)
        _, _, spaceW = labelText.measureSpace(sheet)
        if lastText and not labelText.leadingSpace and not lastText.trailingSpace:
          x += (lastSpaceW + spaceW) / 2
        labelText.draw(sheet, x, y)
        x += w
        lastText = labelText
        lastSpaceW = spaceW
    return (w, h)

  def measure(self, sheet):
    width = 0
    height = 0
    lastSpaceW = None
    lastText = None
    for labelText in self.labelTexts:
      if labelText:
        textW, textH, _= labelText.measure(sheet)
        _, _, spaceW = labelText.measureSpace(sheet)
        height = max(height, textH)
        width += textW
        if lastText and not labelText.leadingSpace and not lastText.trailingSpace:
          width += (lastSpaceW + spaceW) / 2
        lastText = labelText
        lastSpaceW = spaceW
    return (width, height)

class WrappingLabelLine(LabelLine):
  def draw(self, sheet, centerX, startAtY):
    pass

  def measure(self, sheet):
    pass
