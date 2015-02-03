#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_sheet import FontType, LabelSheet
from label_text import TextEntity, TextWord, SingleTextLine, WrappingTextLine
from component import Component

class LedComponent(Component):
  lensTextDict = {"DIFFUSED": "diffused", "CLEAR": "clear"}
  # commonTextDict = {"C": "cmn cathode", "A": "cmn anode"}
  commonTextDict = {"C": "cmn CATHODE", "A": "cmn ANODE"}

  def makeLabel(self):
    textLines = []


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
    specs.append(self.getPowerSpec())
    specs.append(self.getAngleSpec())
    specs.append(self.getBrightnessText())
    specs.append(self.getWavelengthText())
    filteredSpecs = filter(lambda x: x, specs)


    source = self.getSource()
    if source: textLines.append(source)

    textLines.append(SingleTextLine([TextWord(FontType.BASIC, " ".join(category))]))

    if summary: 
      textLines.append(SingleTextLine([TextWord(FontType.MAJOR, " ".join(summary))]))
    textLines.append(SingleTextLine([TextWord(FontType.MAJOR, self.getProp("Color"))]))
    if self.getProp("Common"): 
      textLines.append(SingleTextLine([TextWord(FontType.BASIC, LedComponent.commonTextDict[self.getProp("Common")])]))
    if self.getProp("Configuration"): 
      textLines.append(SingleTextLine([TextWord(FontType.BASIC, "config: " + self.getProp("Configuration"))]))
    if filteredSpecs:
      # textLines.append(SingleTextLine(TextWord(FontType.BASIC, " ".join(filteredSpecs))))
      textLines.append(WrappingTextLine(map(lambda t: TextWord(FontType.BASIC, t), filteredSpecs), True))

    if self.getNotes(): textLines.append(self.getNotes())

    self.checkAllPropsUsed()

    return TextEntity(*textLines) if textLines else None


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
