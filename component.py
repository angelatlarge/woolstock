#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from __future__ import print_function
from label_text import LabelText
from label_line import LabelLine, SingleLabelLine, WrappingLabelLine
from label_sheet import FontType, LabelSheet
import sys

class Component(object):

  @staticmethod
  def ampsAsMilliampsExtractor(iMax): return str(int(float(iMax)*1000))
  @staticmethod
  def identityExtractor(x): return x

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
    return self.getMinMaxValue("Imax%s, A", None, ampsAsMilliampsExtractor, "mA")

  def getBrightnessText(self):
    brightnessText = self.getMinMaxValue("Brightness%s min", "Brightness%s max", Compoent.identityExtractor, self.getProp("Brightness units", ""))
    if self.getProp("Brightness units"): 
      return brightnessText
    else:
      return None

  def getWavelengthText(self):
    extractor = lambda x: x
    return self.getMinMaxValue("Wave%s, min, nm", "Wave%s, max, nm", extractor, "nm")

  def getVoltageDropText(self):
    extractor = lambda x: "%1.1f" % float(x)
    return self.getMinMaxValue("Drop%s min, V", "Drop%s max, V", extractor, "V")

  def getMinMaxValue(self, minPropNameT, maxPropNameT, extractor, unitString=None):
    """
      Given at least one name template (minPropNameT) an field value to string converter
      and a unit string, get up to three min/max or precise property and format them for the label
    """

    def getMinMaxString(minPropName, maxPropName):
      min = self.getProp(minPropName)
      max = self.getProp(maxPropName) if maxPropNameT else None
      if not min: return None
      if not max or max == min:
        return extractor(min)
      else:
        return "%s-%s" % (extractor(min), extractor(max))

    allValues = []
    for idx in range(4):
      idxSubst = "" if idx == 0 else str(idx)
      try:
        minPropName = minPropNameT % (idxSubst)
        maxPropName = maxPropNameT % (idxSubst) if maxPropNameT else None
      except TypeError:
        minPropName = minPropNameT
        maxPropName = maxPropNameT if maxPropNameT else None
      minMaxString = getMinMaxString(minPropName, maxPropName)
      if minMaxString: allValues.append(minMaxString)
      if idx == 0 and allValues: break
    if allValues: 
      return "/".join(allValues) + unitString
    else:
      return None



  def getProp(self, propertyName, defaultValue = None):
    self._checkedProps.add(propertyName)
    if propertyName in self.propertiesDict:
      return self.propertiesDict[propertyName]
    else:
      return defaultValue

  def checkAllPropsUsed(self):
    allProps = set(self.propertiesDict.iterkeys())
    unusedProps = allProps - self._checkedProps
    if len(unusedProps) > 0:
      print("WARNING: not all properties have been considered in %s ID %d. Ignored prerties: %s" % (self.__class__.__name__, self.id, ",".join(unusedProps)), file=sys.stderr)



