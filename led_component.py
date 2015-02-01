#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_sheet import FontType, LabelSheet
from label_block import LabelBlock
from label_line import LabelLine, SingleLabelLine, WrappingLabelLine
from label_text import LabelText
from component import Component

class LedComponent(Component):
  lensTextDict = {"DIFFUSED": "diffused", "CLEAR": "clear"}
  # commonTextDict = {"C": "cmn cathode", "A": "cmn anode"}
  commonTextDict = {"C": "cmn CATHODE", "A": "cmn ANODE"}

  def makeLabel(self):
    labelLines = []


    summary = []
    category = []
    mountingType = self.propertiesDict["Mounting Type"]
    if mountingType == "TH":
      category = ["th LED"]

      if self.propertiesDict["Shape"] == "ROUND":
        summary.append(self.propertiesDict["Size"])
        summary.append(LedComponent.lensTextDict[self.propertiesDict["Lens"]])
      elif self.propertiesDict["Shape"] == "RECT":
        summary.append("Rectangular")
      else:
        return None
    elif mountingType == "SMD":
      category = ["SMD LED"]
      summary.append(self.propertiesDict["Size"])
    elif mountingType == "EMIT":
      category = ["EMITTER LED"]
    else:
      return None

    specs = []
    specs.append(self.getVoltageDropSpec())
    specs.append(self.getMaxCurrentAsMa())
    specs.append(self.getAngleSpec())
    specs.append(self.getBrightnessSpec())
    specs.append(self.getPowerSpec())
    filteredSpecs = filter(lambda x: x, specs)


    source = self.getSource()
    if source: labelLines.append(source)

    labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, " ".join(category))]))

    if summary: 
      labelLines.append(SingleLabelLine([LabelText(FontType.MAJOR, " ".join(summary))]))
    labelLines.append(SingleLabelLine([LabelText(FontType.MAJOR, self.propertiesDict["Color"])]))
    if self.propertiesDict["Common"]: 
      labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, LedComponent.commonTextDict[self.propertiesDict["Common"]])]))
    if self.propertiesDict["Configuration"]: 
      labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, "config: " + self.propertiesDict["Configuration"])]))
    if filteredSpecs:
      # labelLines.append(SingleLabelLine(LabelText(FontType.BASIC, " ".join(filteredSpecs))))
      labelLines.append(WrappingLabelLine(map(lambda t: LabelText(FontType.BASIC, t), filteredSpecs), True))

    if self.getNotes(): labelLines.append(self.getNotes())


    return LabelBlock(*labelLines) if labelLines else None

  def getVoltageDropSpec(self):
    vDrop = []
    vDrop.append(self.getVoltageDrop(self.propertiesDict["Drop1 min, V"], self.propertiesDict["Drop1 max, V"]))
    vDrop.append(self.getVoltageDrop(self.propertiesDict["Drop2 min, V"], self.propertiesDict["Drop2 max, V"]))
    vDrop.append(self.getVoltageDrop(self.propertiesDict["Drop3 min, V"], self.propertiesDict["Drop3 max, V"]))
    filteredVoltageDrop = filter(lambda x: x, vDrop)
    if filteredVoltageDrop: 
      return "/".join(filteredVoltageDrop) + "V"
    else:
      return None

  def getVoltageDrop(self, vMin, vMax):
    if not vMin: return None
    if vMax:
      return "%1.1f-%1.1f" % (float(vMin), float(vMax))
    else:
      return "%1.1f" % float(vMin)

  def getAngleSpec(self):
    angleMin = self.propertiesDict["Angle min"]
    angleMax = self.propertiesDict["Angle max"]
    if angleMin and angleMax:
      return "%s-%s°" % (angleMin, angleMax)
    elif angleMin:
      return "%s°" % (angleMin)
    else:
      return None

  def getBrightnessSpec(self):
    if not self.propertiesDict["Brightness units"]: return None
    brightness = []
    brightness.append(self.getBrightness(self.propertiesDict["Brightness 1 min"], self.propertiesDict["Brightness 1 max"]))
    brightness.append(self.getBrightness(self.propertiesDict["Brightness 2 min"], self.propertiesDict["Brightness 2 max"]))
    brightness.append(self.getBrightness(self.propertiesDict["Brightness 3 min"], self.propertiesDict["Brightness 3 max"]))
    filteredBrightness = filter(lambda x: x, brightness)
    if filteredBrightness: 
      return "/".join(filteredBrightness) + self.propertiesDict["Brightness units"]
    else:
      return None

  def getBrightness(self, min, max):
    if not min: return None
    if max:
      return "%s-%s" % (min, max)
    else:
      return "%s" % (min)

  def getPowerSpec(self):
    power = self.propertiesDict["Max Power, W"]
    if power:
      return power + "W"
    else:
      return None
