#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

class LabelBlock:
  def __init__(self, *args):
    print "LabelBlock.__init()__", args
    self.labelLines = args

  def measure(self, sheet):
    width = 0
    height = 0
    for labelLine in self.labelLines:
      w, h = labelLine.measure(sheet)
      width = max(width, w)
      height += h
    return (width, height)

  def draw(self, sheet, centerX, startAtY):
    blockWidth = 0
    blockHeight = 0
    for labelLine in self.labelLines:
      (w, h) = labelLine.draw(sheet, centerX, startAtY + blockHeight)
      blockWidth = max(blockWidth, w)
      blockHeight += h
    return (blockWidth, blockHeight)

