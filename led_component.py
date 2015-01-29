#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_sheet import LabelText, LabelLine, FontType
from component import Component

class LedComponent(Component):

  def makeLabel(self):
    labelLines = []

    summary = []
    mountingType = self.propertiesDict["Mounting Type"]
    if mountingType == "TH":
      summary.append(self.propertiesDict["Size"])
      # summary.append(self.propertiesDict["Shape"])
      # summary.append(self.propertiesDict["Color"])
      # summary.append(self.propertiesDict["Lens"])
      # self.propertiesDict["Mounting Type"]

    elif mountingType == "SMD":
      summary.append(self.propertiesDict["Size"])
      summary.append("SMD")
    else:
      return None

    summary.append("LED")
    labelLines.append(LabelLine(LabelText(FontType.MAJOR, " ".join(summary))))
    return labelLines
