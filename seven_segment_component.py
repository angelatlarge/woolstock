#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_sheet import FontType, LabelSheet
from label_text import TextEntity, TextWord, SingleTextLine, WrappingTextLine
from led_component import LedComponent
from component import Component

class SevenSegmentComponent(Component):

  def makeLabel(self):

    if not self.getProp("Color"): return None

    textLines = []

    source = self.getSource()
    if source: textLines.append(source)


    summary = []
    category = ["7-segment display"]

    textLines.append(SingleTextLine([TextWord(FontType.BASIC, " ".join(category))]))

    if self.getProp("Size, in"): summary.append(self.getProp("Size, in") + '”')
    if self.getProp("Color"): summary.append(self.getProp("Color"))

    textLines.append(WrappingTextLine(map(lambda t: TextWord(FontType.MAJOR, t), summary), True))

    if self.getProp("Common"): 
      textLines.append(SingleTextLine([TextWord(FontType.BASIC, LedComponent.commonTextDict[self.getProp("Common")])]))


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
      textLines.append(WrappingTextLine(map(lambda t: TextWord(FontType.BASIC, t), filteredSpecs), True))

    if self.getNotes(): textLines.append(self.getNotes())

    self.checkAllPropsUsed()

    return TextEntity(*textLines) if textLines else None

