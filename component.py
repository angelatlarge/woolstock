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

  def getBrightnessText(self):
    if not self.getProp("Brightness units"): return None
    brightness = []
    brightness.append(self.getBrightnessValue("Brightness min", "Brightness max"))
    if not brightness:
      brightness.append(self.getBrightnessValue("Brightness 1 min", "Brightness 1 max"))
      brightness.append(self.getBrightnessValue("Brightness 2 min", "Brightness 2 max"))
      brightness.append(self.getBrightnessValue("Brightness 3 min", "Brightness 3 max"))
    filteredBrightness = filter(lambda x: x, brightness)
    if filteredBrightness: 
      return "/".join(filteredBrightness) + self.getProp("Brightness units")
    else:
      return None

  def getBrightnessValue(self, minPropName, maxPropName):
    min = self.getProp(minPropName)
    max = self.getProp(maxPropName)
    if not min: return None
    if max:
      return "%s-%s" % (min, max)
    else:
      return "%s" % (min)

  def getWavelengthText(self):
    extractor = lambda x: x
    return self.getMinMaxValue("Wave%s, min, nm", "Wave%s, max, nm", extractor, "nm")

  def getMinMaxValue(self, minPropNameT, maxPropNameT, extractor, unitString):
    def getMinMaxString(minPropName, maxPropName):
      min = self.getProp(minPropName)
      max = self.getProp(maxPropName)
      if not min: return None
      if max:
        return "%s-%s" % (extractor(min), extractor(max))
      else:
        return extractor(min)

    allValues = []
    for idx in range(4):
      idxSubst = "" if idx == 0 else str(idx)
      allValues.append(getMinMaxString(minPropNameT % (idxSubst), maxPropNameT % (idxSubst)))
      if idx == 0 and allValues: break
    filteredValues = filter(lambda x: x, allValues)
    if filteredValues: 
      return "/".join(filteredValues) + unitString
    else:
      return None



  def getVoltageDropText(self):
    vDrop = []
    vDrop.append(self.getVoltageDropValue("Drop min, V", "Drop max, V"))
    if not vDrop:
      vDrop.append(self.getVoltageDropValue("Drop1 min, V", "Drop1 max, V"))
      vDrop.append(self.getVoltageDropValue("Drop2 min, V", "Drop2 max, V"))
      vDrop.append(self.getVoltageDropValue("Drop3 min, V", "Drop3 max, V"))
    filteredVoltageDrop = filter(lambda x: x, vDrop)
    if filteredVoltageDrop: 
      return "/".join(filteredVoltageDrop) + "V"
    else:
      return None

  def getVoltageDropValue(self, vMinPropName, vMaxPropName):
    vMin = self.getProp(vMinPropName)
    vMax = self.getProp(vMaxPropName)
    if not vMin: return None
    if vMax:
      return "%1.1f-%1.1f" % (float(vMin), float(vMax))
    else:
      return "%1.1f" % float(vMin)


  def getProp(self, propertyName):
    self._checkedProps.add(propertyName)
    if propertyName in self.propertiesDict:
      return self.propertiesDict[propertyName]

  def checkAllPropsUsed(self):
    allProps = set(self.propertiesDict.iterkeys())
    unusedProps = allProps - self._checkedProps
    if len(unusedProps) > 0:
      print("WARNING: not all properties have been considered in %s. Ignored prerties: %s" % (self.__class__.__name__, ",".join(unusedProps)), file=sys.stderr)



