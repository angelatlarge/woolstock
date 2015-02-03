#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_sheet import FontType, LabelSheet
from label_block import LabelBlock
from label_line import LabelLine, SingleLabelLine, WrappingLabelLine
from label_text import LabelText
from led_component import LedComponent
from component import Component

class TransistorComponent(Component):

  def makeLabel(self):
    labelLines = []
    specs = []

    source = self.getSource()
    if source: labelLines.append(source)

    transistorType = self.getPrintableType()
    if transistorType in ["BJT", "DARLINGTON"]:
      category = [self.getProp("Subtype"), transistorType]

      # hFE
      specs.append(self.getMinMaxValue("hFE min", "hFE max", self.identityExtractor, "hFE"))
      # I max
      specs.append(self.getMinMaxValue("IC, A", None, self.ampsAsMilliampsExtractor, "mA"))
      # Vmax
      specs.append(self.getMinMaxValue("VCB/VCE max", None, self.identityExtractor, "V"))

    elif transistorType in ["MOSFET", "FET"]:
      category = [self.getProp("Subtype"), transistorType]

      # Vdss max
      specs.append(self.getMinMaxValue("VDSS max", None, self.identityExtractor, "VDSS"))
      # Vdss max
      specs.append(self.getMinMaxValue("ID cont, A", None, self.identityExtractor, "A"))
      # Vds(on)
      specs.append(self.getMinMaxValue("VDS(On) min", "VDS(On) max", self.identityExtractor, "VDS(on)"))
      # Rds(on)
      specs.append(self.getMinMaxValue("RDS(on) max", None, self.identityExtractor, "Ω"))
    else:
      return None


    summary = [self.getProp("Name")]

    labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, " ".join(category))]))
    labelLines.append(WrappingLabelLine(map(lambda t: LabelText(FontType.MAJOR, t), summary), True))

    # if self.getProp("Common"): 
      # labelLines.append(SingleLabelLine([LabelText(FontType.BASIC, LedComponent.commonTextDict[self.getProp("Common")])]))

    # specs.append(self.getMaxCurrentAsMa())
    # specs.append(self.getVoltageDropText())
    # specs.append(self.getBrightnessText())
    # specs.append(self.getWavelengthText())
    filteredSpecs = filter(lambda x: x, specs)
    if filteredSpecs:
      labelLines.append(WrappingLabelLine(map(lambda t: LabelText(FontType.BASIC, t), filteredSpecs), True))

    if self.getNotes(): labelLines.append(self.getNotes())

    self.checkAllPropsUsed()

    return LabelBlock(*labelLines) if labelLines else None

  def getPrintableType(self):
    typeMap = {"DARLINGTON": "Darlington"}
    transistorType = self.getProp("Type")
    if transistorType:
      if transistorType in typeMap:
        return typeMap[transistorType]
      else:
        return transistorType
    else:
      return None
