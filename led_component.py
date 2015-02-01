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
    mountingType = self.getProp("Mounting Type")
    if mountingType == "TH":
      category = ["th LED"]

      if self.getProp("Shape") == "ROUND":
        summary.append(self.getProp("Size"))
        summary.append(LedComponent.lensTextDict[self.getProp("Lens")])
      elif self.getProp("Shape") == "RECT":
        summary.append("Rectangular")
      else:
        return None
    elif mountingType == "SMD":
      category = ["SMD LED"]
      summary.append(self.getProp("Size"))
    elif mountingType == "EMIT":
      category = ["EMITTER LED"]
    else:
      return None

    specs = []
    specs.append(self.getVoltageDropText())
    specs.append(self.getMaxCurrentAsMa())
    specs.append(self.getAngleSpec())
    specs.append(self.getBrightnessText())
    specs.append(self.getPowerSpec())
    filteredSpecs = filter(lambda x: x, specs)


    source = self.getSource()
    if source: labelLines.append(source)

    labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, " ".join(category))]))

    if summary: 
      labelLines.append(SingleLabelLine([LabelText(FontType.MAJOR, " ".join(summary))]))
    labelLines.append(SingleLabelLine([LabelText(FontType.MAJOR, self.getProp("Color"))]))
    if self.getProp("Common"): 
      labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, LedComponent.commonTextDict[self.getProp("Common")])]))
    if self.getProp("Configuration"): 
      labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, "config: " + self.getProp("Configuration"))]))
    if filteredSpecs:
      # labelLines.append(SingleLabelLine(LabelText(FontType.BASIC, " ".join(filteredSpecs))))
      labelLines.append(WrappingLabelLine(map(lambda t: LabelText(FontType.BASIC, t), filteredSpecs), True))

    if self.getNotes(): labelLines.append(self.getNotes())

    self.checkAllPropsUsed()

    return LabelBlock(*labelLines) if labelLines else None


  def getAngleSpec(self):
    angleMin = self.getProp("Angle min")
    angleMax = self.getProp("Angle max")
    if angleMin and angleMax:
      return "%s-%s°" % (angleMin, angleMax)
    elif angleMin:
      return "%s°" % (angleMin)
    else:
      return None

  def getPowerSpec(self):
    power = self.getProp("Max Power, W")
    if power:
      return power + "W"
    else:
      return None
