#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from labelsheet import LabelText, LabelLine, FontType

class DiodeComponent:
  def __init__(self, propertiesDict):
    self.propertiesDict = propertiesDict

  def makeLabel(self):
    typeMap = {"GENERAL": "diode", "SCHOTTKY": "schottky diode"}

    labelLines = []

    # TYPE
    labelLines.append(LabelLine(LabelText(FontType.BASIC, typeMap[self.propertiesDict["Type"]])))

    # ID/NAME
    labelLines.append(LabelLine(LabelText(FontType.MAJOR, self.propertiesDict["ID"])))

    # SPECS (all on one line)
    specs = []

    # Forward voltage drop
    specs.append(self.propertiesDict["Vmax, V"] + "V")

    # Max current
    iMax = float(self.propertiesDict["Imax, A"])
    iMaxText = str(iMax) + "A" if iMax >= 1 else str(int(iMax * 1000)) + "mA"
    specs.append(iMaxText)
    
    # Recovery time
    if (self.propertiesDict["Recovery time, ns"]):
      time = long(self.propertiesDict["Recovery time, ns"])
      timeText = str(time) + "ns" if time < 1000 else str(time/1000) + "μs"
      specs.append(timeText)

    specsText = " ".join(specs)

    labelLines.append(LabelLine(LabelText(FontType.BASIC, specsText)))

    return labelLines
