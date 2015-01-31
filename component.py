#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_text import LabelText
from label_line import LabelLine, SingleLabelLine, WrappingLabelLine
from label_sheet import FontType, LabelSheet

class Component(object):
  def __init__(self, propertiesDict):
    self.propertiesDict = propertiesDict

  def getNotes(self):
    notes = self.propertiesDict["Notes"]
    if notes:
      noteTexts = [LabelText(FontType.MINORHEADING, "Notes:")]
      noteTexts.extend(map(lambda t: LabelText(FontType.MINOR, t), notes.split()))
      return WrappingLabelLine(noteTexts, True)
    else:
      return None
