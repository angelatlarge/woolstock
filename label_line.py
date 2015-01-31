#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

class LabelLine(object):
  def __init__(self, labelTexts):
    self.labelTexts = labelTexts

class SingleLabelLine(LabelLine):

  def __init__(self, labelTexts, smallify = False):
    super(SingleLabelLine, self).__init__(labelTexts)
    self.smallify = smallify
    self.brokenLine = None

  def measure(self, sheet):
    return self.safeGetBrokenLine(sheet).measure(sheet)

  def draw(self, sheet, centerX, startAtY):
    return self.safeGetBrokenLine(sheet).draw(sheet, centerX, startAtY)

  def safeGetBrokenLine(self, sheet):
    if not self.brokenLine:
      maxWidth = sheet.printableLabelWidth if self.smallify else None
      self.brokenLine = _BrokenLine(self.labelTexts, None, maxWidth)
    return self.brokenLine


class _BrokenLine(object):
  def __init__(self, labelTexts, extents = None, maxWidth = None):
    self.labelTexts = labelTexts
    self.scaleFactor = 1.0
    self.extents = None
    self.maxWidth = maxWidth

  @property
  def width(self): return self.extents[0] if self.extents else None

  @property
  def height(self): return self.extents[1] if self.extents else None

  def measure(self, sheet):
    self.scaleFactor = 1.0
    (width, height) = self._measure(sheet)
    if not self.maxWidth or width <= self.maxWidth: 
      return (width, height)
    scaleFactorDelta = self.maxWidth / width
    self.scaleFactor = self.scaleFactor * scaleFactorDelta
    (width, height) = self._measure(sheet)
    return (width, height)

  def _measure(self, sheet):
    width = 0
    height = 0
    lastSpaceW = None
    lastText = None
    for labelText in self.labelTexts:
      if labelText:
        textW, textH, _= labelText.measure(sheet, self.scaleFactor)
        _, _, spaceW = labelText.measureSpace(sheet, self.scaleFactor)
        height = max(height, textH)
        width += textW
        if lastText and not labelText.leadingSpace and not lastText.trailingSpace:
          width += (lastSpaceW + spaceW) / 2
        lastText = labelText
        lastSpaceW = spaceW
    self.extents = (width, height)
    return self.extents

  def draw(self, sheet, centerX, startAtY):
    if not self.extents: self.measure(sheet)
    x = centerX - self.width / 2.0
    y = startAtY + self.height
    lastSpaceW = None
    lastText = None
    for labelText in self.labelTexts:
      if labelText:
        w, h, _ = labelText.measure(sheet, self.scaleFactor)
        _, _, spaceW = labelText.measureSpace(sheet, self.scaleFactor)
        if lastText and not labelText.leadingSpace and not lastText.trailingSpace:
          x += (lastSpaceW + spaceW) / 2
        # print "Drawing at %s,%s" % (str(x), str(y))
        labelText.draw(sheet, x, y, self.scaleFactor)
        x += w
        lastText = labelText
        lastSpaceW = spaceW
    return self.extents

class WrappingLabelLine(LabelLine):

  def __init__(self, labelTexts, smallify = False):
    super(WrappingLabelLine, self).__init__(labelTexts)
    self.smallify = smallify

  def measure(self, sheet):
    w = 0
    h = 0
    for bl in self.breakLines(sheet):
      blWidth, blHeight = bl.measure(sheet)
      w = max(w, blWidth)
      h += blHeight
    return (w, h)

  def draw(self, sheet, centerX, startAtY):
    y = startAtY
    width = 0
    height = 0
    for bl in self.breakLines(sheet):
      blWidth, blHeight = bl.measure(sheet)
      bl.draw(sheet, centerX, y)

      y += blHeight
      width = max(width, blWidth)
      height += blHeight
    return (width, height)

  def breakLines(self, sheet):
    width = 0
    height = 0
    lastSpaceW = None
    lastText = None
    wrapLines = []
    labelTexts = []
    maxWidth = sheet.printableLabelWidth if self.smallify else None
    for labelText in self.labelTexts:
      if labelText:

        textW, textH, _= labelText.measure(sheet)
        _, _, spaceW = labelText.measureSpace(sheet)
        widthContribution = textW
        if lastText and not labelText.leadingSpace and not lastText.trailingSpace:
          widthContribution += (lastSpaceW + spaceW) / 2
        if width + widthContribution > sheet.printableLabelWidth and labelTexts:
          # Exceeded the max width. Wrap
          wrapLines.append(_BrokenLine(labelTexts, (width, height), maxWidth))
          width = 0
          height = 0
          lastSpaceW = None
          lastText = None
          labelTexts = []

        width += widthContribution
        height = max(height, textH)
        lastText = labelText
        lastSpaceW = spaceW
        labelTexts.append(labelText)


    if labelTexts: 
      wrapLines.append(_BrokenLine(labelTexts, (width, height), maxWidth))
    return wrapLines
