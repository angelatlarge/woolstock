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

    if not self.getProp("Color"): return None

    labelLines = []

    source = self.getSource()
    if source: labelLines.append(source)


    summary = []
    category = ["7-segment display"]

    labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, " ".join(category))]))

    if self.getProp("Size, in"): summary.append(self.getProp("Size, in") + '"')
    if self.getProp("Color"): summary.append(self.getProp("Color"))

    labelLines.append(WrappingLabelLine(map(lambda t: LabelText(FontType.MAJOR, t), summary), True))

    if self.getProp("Common"): 
      labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, LedComponent.commonTextDict[self.getProp("Common")])]))


    specs = []
    specs.append(self.getMaxCurrentAsMa())
    specs.append(self.getVoltageDropText())
    # specs.append(self.getMaxCurrentSpec())
    # specs.append(self.getAngleSpec())
    specs.append(self.getBrightnessText())
    specs.append(self.getWavelengthText())
    print self.getWavelengthText()
    # specs.append(self.getPowerSpec())
    filteredSpecs = filter(lambda x: x, specs)



    if filteredSpecs:
      labelLines.append(WrappingLabelLine(map(lambda t: LabelText(FontType.BASIC, t), filteredSpecs), True))

    if self.getNotes(): labelLines.append(self.getNotes())

    self.checkAllPropsUsed()

    return LabelBlock(*labelLines) if labelLines else None

