#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from __future__ import print_function
from label_text import LabelText
from label_line import LabelLine, SingleLabelLine, WrappingLabelLine
from label_sheet import FontType, LabelSheet
import sys

class Component(object):
  def __init__(self, propertiesDict):
    self.propertiesDict = propertiesDict
    self._checkedProps = set(["ID"])

  @property
  def id(self): return int(self.propertiesDict["ID"])

  def getNotes(self):
    notes = self.getProp("Notes")
    if notes:
      noteTexts = [LabelText(FontType.MINORHEADING, "Notes:")]
      noteTexts.extend(map(lambda t: LabelText(FontType.MINOR, t), notes.split()))
      return WrappingLabelLine(noteTexts, True)
    else:
      return None

  def getSource(self):
    source = None
    manufaturer = self.getProp("Manufacturer")
    model = self.getProp("Model")
    if manufaturer and model:
      source = "%s %s" % (manufaturer, model)
    elif manufaturer:
      source = manufaturer
    elif model:
      source = model
    elif self.getProp("Source") and self.getProp("Subsource"):
      source = "%s (%s)" % (self.getProp("Source"), self.getProp("Subsource"))
    elif self.getProp("Source"):
      source = self.getProp("Source")

    if source: 
      return SingleLabelLine([LabelText(FontType.MINOR, source)], True)
    else:
      return None

  def getMaxCurrentAsMa(self):
    maxCurrent = []
    maxCurrent.append(self.getMaxCurrentAmpsAsMa("Imax, A"))
    if not maxCurrent:
      maxCurrent.append(self.getMaxCurrentAmpsAsMa("Imax1, A"))
      maxCurrent.append(self.getMaxCurrentAmpsAsMa("Imax2, A"))
      maxCurrent.append(self.getMaxCurrentAmpsAsMa("Imax3, A"))
    filteredMaxCurrent = filter(lambda x: x, maxCurrent)
    if filteredMaxCurrent: 
      return "/".join(filteredMaxCurrent) + "mA"
    else:
      return None

  def getMaxCurrentAmpsAsMa(self, propertyName):
    iMax = self.getProp(propertyName)
    if iMax: 
      return str(int(float(iMax)*1000))
    else:
      return None

  def getProp(self, propertyName):
    self._checkedProps.add(propertyName)
    if propertyName in self.propertiesDict:
      return self.propertiesDict[propertyName]

  def checkAllPropsUsed(self):
    allProps = set(self.propertiesDict.iterkeys())
    unusedProps = allProps - self._checkedProps
    if len(unusedProps) > 0:
      print("WARNING: not all properties have been considered. Ignored prerties: %s" % (",".join(unusedProps)), file=sys.stderr)
