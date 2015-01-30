#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_sheet import FontType
from label_block import LabelBlock
from label_line import LabelLine, SingleLabelLine, WrappingLabelLine
from label_text import LabelText
from component import Component

class DiodeComponent(Component):

  def makeLabel(self):
    typeMap = {"GENERAL": "diode", "SCHOTTKY": "schottky diode"}

    labelLines = []

    # TYPE
    labelLines.append(SingleLabelLine(LabelText(FontType.BASIC, typeMap[self.propertiesDict["Type"]])))

    # ID/NAME
    labelLines.append(SingleLabelLine(LabelText(FontType.MAJOR, self.propertiesDict["ID"])))

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

    labelLines.append(SingleLabelLine(LabelText(FontType.BASIC, specsText)))

    return LabelBlock(*labelLines) if labelLines else None
