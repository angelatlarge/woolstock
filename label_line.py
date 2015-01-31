#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

class LabelLine(object):
  def __init__(self, *args):
    print "LabelLine.__init()__", args
    # self.labelTexts = [item for sublist in args for item in sublist]
    self.labelTexts = args
    print self.labelTexts
    # self.labelTexts = list(args)
    # print args
    # print self.labelTexts

class SingleLabelLine(LabelLine):
  def __init__(self, *args):
    super(SingleLabelLine, self).__init__(*args)
    # print self.labelTexts
    self.brokenLine = _BrokenLine(self.labelTexts)

  def measure(self, sheet):
    return self.brokenLine.measure(sheet)

  def draw(self, sheet, centerX, startAtY):
    return self.brokenLine.draw(sheet, centerX, startAtY)

class _BrokenLine(object):
  def __init__(self, labelTexts, extents = None):
    self.labelTexts = labelTexts
    self.extents = extents

  @property
  def width(self): return self.extents[0] if self.extents else None

  @property
  def height(self): return self.extents[1] if self.extents else None

  def measure(self, sheet):
    width = 0
    height = 0
    lastSpaceW = None
    lastText = None
    for labelText in self.labelTexts:
      if labelText:
        print "labelText.measure()" + str(labelText)
        textW, textH, _= labelText.measure(sheet)
        _, _, spaceW = labelText.measureSpace(sheet)
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
        w, h, _ = labelText.measure(sheet)
        _, _, spaceW = labelText.measureSpace(sheet)
        if lastText and not labelText.leadingSpace and not lastText.trailingSpace:
          x += (lastSpaceW + spaceW) / 2
        print "Drawing at %s,%s" % (str(x), str(y))
        labelText.draw(sheet, x, y)
        x += w
        lastText = labelText
        lastSpaceW = spaceW
    return self.extents

class WrappingLabelLine(LabelLine):

  def measure(self, sheet):
    w = 0
    h = 0
    for bl in self.breakLines(sheet):
      w = max(w, bl.width)
      h += bl.height
    return (w, h)

  def draw(self, sheet, centerX, startAtY):
    y = startAtY
    width = 0
    height = 0
    for bl in self.breakLines(sheet):
      blWidth, blHeight = bl.extents
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
    for labelText in self.labelTexts:
      if labelText:

        textW, textH, _= labelText.measure(sheet)
        _, _, spaceW = labelText.measureSpace(sheet)
        widthContribution = textW
        if lastText and not labelText.leadingSpace and not lastText.trailingSpace:
          widthContribution += (lastSpaceW + spaceW) / 2
        if width + widthContribution > sheet.printableLabelWidth and labelTexts:
          # Exceeded the max width. Wrap
          wrapLines.append(_BrokenLine(labelTexts, (width, height)))
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
      wrapLines.append(_BrokenLine(labelTexts, (width, height)))
    return wrapLines
