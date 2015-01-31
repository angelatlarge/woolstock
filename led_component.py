#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_sheet import FontType, LabelSheet
from label_block import LabelBlock
from label_line import LabelLine, SingleLabelLine, WrappingLabelLine
from label_text import LabelText
from component import Component

class LedComponent(Component):
  lensTextDict = {"DIFFUSED": "diffused", "CLEAR": "clear"}
  commonTextDict = {"C": "cmn cathode", "A": "cmn anode"}

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

    source = ""
    if self.propertiesDict["Manufacturer"]:
      source = self.propertiesDict["Manufacturer"]
    elif self.propertiesDict["Source"] and self.propertiesDict["Subsource"]:
      source = "%s (%s)" % (self.propertiesDict["Source"], self.propertiesDict["Subsource"])
    elif self.propertiesDict["Source"]:
      source = self.propertiesDict["Source"]



    specs = []
    specs.append(self.getVoltageDropSpec())
    specs.append(self.getMaxCurrentSpec())
    specs.append(self.getAngleSpec())
    specs.append(self.getBrightnessSpec())
    filteredSpecs = filter(lambda x: x, specs)


    if source: 
      labelLines.append(SingleLabelLine([LabelText(FontType.MINOR, source)], True))
    labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, " ".join(category))]))


    if summary: 
      labelLines.append(SingleLabelLine([LabelText(FontType.MAJOR, " ".join(summary))]))
    labelLines.append(SingleLabelLine([LabelText(FontType.MAJOR, self.propertiesDict["Color"])]))
    if self.propertiesDict["Common"]: 
      labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, LedComponent.commonTextDict[self.propertiesDict["Common"]])]))
    if filteredSpecs:
      # labelLines.append(SingleLabelLine(LabelText(FontType.BASIC, " ".join(filteredSpecs))))
      labelLines.append(WrappingLabelLine(map(lambda t: LabelText(FontType.BASIC, t), filteredSpecs), True))

    #   if mountingType == "TH":
    #     summary.append(self.propertiesDict["Size"])
    #     # summary.append(self.propertiesDict["Shape"])
    #     # summary.append(self.propertiesDict["Color"])
    #     # summary.append(self.propertiesDict["Lens"])
    #     # self.propertiesDict["Mounting Type"]

    # elif mountingType == "SMD":
    #   summary.append(self.propertiesDict["Size"])
    #   summary.append("SMD")

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

  def getMaxCurrentSpec(self):
    maxCurrent = []
    maxCurrent.append(self.getMaxCUrrent(self.propertiesDict["Imax1, A"]))
    maxCurrent.append(self.getMaxCUrrent(self.propertiesDict["Imax2, A"]))
    maxCurrent.append(self.getMaxCUrrent(self.propertiesDict["Imax3, A"]))
    filteredMaxCurrent = filter(lambda x: x, maxCurrent)
    if filteredMaxCurrent: 
      return "/".join(filteredMaxCurrent) + "mA"
    else:
      return None

  def getMaxCUrrent(self, iMax):
    if not iMax: return None
    return str(int(float(iMax)*1000))

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
