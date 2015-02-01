#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_text import LabelText
from label_line import LabelLine, SingleLabelLine, WrappingLabelLine
from label_sheet import FontType, LabelSheet

class Component(object):
  def __init__(self, propertiesDict):
    self.propertiesDict = propertiesDict

  @property
  def id(self): return int(self.propertiesDict["ID"])

  def getNotes(self):
    if not "Notes" in self.propertiesDict: return None
    notes = self.propertiesDict["Notes"]
    if notes:
      noteTexts = [LabelText(FontType.MINORHEADING, "Notes:")]
      noteTexts.extend(map(lambda t: LabelText(FontType.MINOR, t), notes.split()))
      return WrappingLabelLine(noteTexts, True)
    else:
      return None

  def getSource(self):
    source = None
    manufaturer = self.propertiesDict["Manufacturer"] if "Manufacturer" in self.propertiesDict else None
    model = self.propertiesDict["Model"] if "Model" in self.propertiesDict else None
    if manufaturer and model:
      source = "%s %s" % (manufaturer, model)
    elif manufaturer:
      source = manufaturer
    elif model:
      source = model
    elif self.propertiesDict["Source"] and self.propertiesDict["Subsource"]:
      source = "%s (%s)" % (self.propertiesDict["Source"], self.propertiesDict["Subsource"])
    elif self.propertiesDict["Source"]:
      source = self.propertiesDict["Source"]

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
    iMax = self.getProperty(propertyName)
    if iMax: 
      return str(int(float(iMax)*1000))
    else:
      return None

  def getProperty(self, propertyName):
    if propertyName in self.propertiesDict:
      return self.propertiesDict[propertyName]
