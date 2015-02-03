#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

class TextEntity:
  """
    Class representing the largest textual grouping, an entire label
  """
  def __init__(self, *args):
    self.textLines = args

  def measure(self, sheet):
    width = 0
    height = 0
    for textLine in self.textLines:
      w, h = textLine.measure(sheet)
      width = max(width, w)
      height += h
    return (width, height)

  def draw(self, sheet, centerX, startAtY):
    blockWidth = 0
    blockHeight = 0
    for textLine in self.textLines:
      (w, h) = textLine.draw(sheet, centerX, startAtY + blockHeight)
      blockWidth = max(blockWidth, w)
      blockHeight += h
    return (blockWidth, blockHeight)

class TextLine(object):
  """
    Abstract class representing a line of text: 
    this line might or might not wrap, depending on the implementation
  """
  def __init__(self, textWords):
    self.textWords = textWords

class SingleTextLine(TextLine):
  """
    Non-wrapping line of text
  """

  def __init__(self, textWords, smallify = False):
    super(SingleTextLine, self).__init__(textWords)
    self.smallify = smallify
    self.brokenLine = None

  def measure(self, sheet):
    return self.safeGetBrokenLine(sheet).measure(sheet)

  def draw(self, sheet, centerX, startAtY):
    return self.safeGetBrokenLine(sheet).draw(sheet, centerX, startAtY)

  def safeGetBrokenLine(self, sheet):
    if not self.brokenLine:
      maxWidth = sheet.printableLabelWidth if self.smallify else None
      self.brokenLine = _BrokenLine(self.textWords, None, maxWidth)
    return self.brokenLine


class _BrokenLine(object):
  """
    Internal representation of a broken lines
  """
  def __init__(self, textWords, extents = None, maxWidth = None):
    self.textWords = textWords
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
    for textWord in self.textWords:
      if textWord:
        textW, textH, _= textWord.measure(sheet, self.scaleFactor)
        _, _, spaceW = textWord.measureSpace(sheet, self.scaleFactor)
        height = max(height, textH)
        width += textW
        if lastText and not textWord.leadingSpace and not lastText.trailingSpace:
          width += (lastSpaceW + spaceW) / 2
        lastText = textWord
        lastSpaceW = spaceW
    self.extents = (width, height)
    return self.extents

  def draw(self, sheet, centerX, startAtY):
    if not self.extents: self.measure(sheet)
    x = centerX - self.width / 2.0
    y = startAtY + self.height
    lastSpaceW = None
    lastText = None
    for textWord in self.textWords:
      if textWord:
        w, h, _ = textWord.measure(sheet, self.scaleFactor)
        _, _, spaceW = textWord.measureSpace(sheet, self.scaleFactor)
        if lastText and not textWord.leadingSpace and not lastText.trailingSpace:
          x += (lastSpaceW + spaceW) / 2
        # print "Drawing at %s,%s" % (str(x), str(y))
        textWord.draw(sheet, x, y, self.scaleFactor)
        x += w
        lastText = textWord
        lastSpaceW = spaceW
    return self.extents

class WrappingTextLine(TextLine):
  """
    Wrapping line of text
  """

  def __init__(self, textWords, smallify = False):
    super(WrappingTextLine, self).__init__(textWords)
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
    textWords = []
    maxWidth = sheet.printableLabelWidth if self.smallify else None
    for textWord in self.textWords:
      if textWord:

        textW, textH, _= textWord.measure(sheet)
        _, _, spaceW = textWord.measureSpace(sheet)
        widthContribution = textW
        if lastText and not textWord.leadingSpace and not lastText.trailingSpace:
          widthContribution += (lastSpaceW + spaceW) / 2
        if width + widthContribution > sheet.printableLabelWidth and textWords:
          # Exceeded the max width. Wrap
          wrapLines.append(_BrokenLine(textWords, (width, height), maxWidth))
          width = 0
          height = 0
          lastSpaceW = None
          lastText = None
          textWords = []

        width += widthContribution
        height = max(height, textH)
        lastText = textWord
        lastSpaceW = spaceW
        textWords.append(textWord)


    if textWords: 
      wrapLines.append(_BrokenLine(textWords, (width, height), maxWidth))
    return wrapLines

class TextWord:
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
    return "TextWord(%s, %s)" % (self.textType, self.textString)

  def __repr__(self):
    return self.__str__()
