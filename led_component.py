#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_sheet import FontType
from label_block import LabelBlock
from label_line import LabelLine
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
      category = ["t.h. LED"]

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
    else:
      return None

    labelLines.append(LabelLine(LabelText(FontType.BASIC, " ".join(category))))
    if summary: 
      labelLines.append(LabelLine(LabelText(FontType.MAJOR, " ".join(summary))))
    labelLines.append(LabelLine(LabelText(FontType.MAJOR, self.propertiesDict["Color"])))
    if self.propertiesDict["Common"]: 
      labelLines.append(LabelLine(LabelText(FontType.BASIC, LedComponent.commonTextDict[self.propertiesDict["Common"]])))

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
