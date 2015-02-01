#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_sheet import FontType, LabelSheet
from label_block import LabelBlock
from label_line import LabelLine, SingleLabelLine, WrappingLabelLine
from label_text import LabelText
from led_component import LedComponent
from component import Component

class SevenSegmentComponent(Component):

  def makeLabel(self):

    if not self.propertiesDict["Color"]: return None

    labelLines = []

    source = self.getSource()
    if source: labelLines.append(source)


    summary = []
    category = ["7-segment display"]

    labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, " ".join(category))]))

    if self.propertiesDict["Size, in"]: summary.append(self.propertiesDict["Size, in"] + '"')
    if self.propertiesDict["Color"]: summary.append(self.propertiesDict["Color"])

    labelLines.append(WrappingLabelLine(map(lambda t: LabelText(FontType.MAJOR, t), summary), True))

    if self.propertiesDict["Common"]: 
      labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, LedComponent.commonTextDict[self.propertiesDict["Common"]])]))


    specs = []
    print self.getMaxCurrentAsMa()
    specs.append(self.getMaxCurrentAsMa())
    # specs.append(self.getVoltageDropSpec())
    # specs.append(self.getMaxCurrentSpec())
    # specs.append(self.getAngleSpec())
    # specs.append(self.getBrightnessSpec())
    # specs.append(self.getPowerSpec())
    filteredSpecs = filter(lambda x: x, specs)



    if filteredSpecs:
      labelLines.append(WrappingLabelLine(map(lambda t: LabelText(FontType.BASIC, t), filteredSpecs), True))

    if self.getNotes(): labelLines.append(self.getNotes())

    return LabelBlock(*labelLines) if labelLines else None

