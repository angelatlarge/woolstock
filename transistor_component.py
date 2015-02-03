#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_sheet import FontType, LabelSheet
from label_text import TextEntity, TextWord, SingleTextLine, WrappingTextLine
from led_component import LedComponent
from component import Component

class TransistorComponent(Component):

  def makeLabel(self):
    textLines = []
    specs = []

    source = self.getSource()
    if source: textLines.append(source)

    transistorType = self.getPrintableType()
    if transistorType in ["BJT", "DARLINGTON"]:
      category = [self.getProp("Subtype"), transistorType]

      # hFE
      specs.append(self.getMinMaxValue("hFE min", "hFE max", self.identityExtractor, "h<sub>FE<sub>"))
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

    textLines.append(SingleTextLine([TextWord(FontType.BASIC, " ".join(category))]))
    textLines.append(WrappingTextLine(map(lambda t: TextWord(FontType.MAJOR, t), summary), True))

    # if self.getProp("Common"): 
      # textLines.append(SingleTextLine([TextWord(FontType.BASIC, LedComponent.commonTextDict[self.getProp("Common")])]))

    # specs.append(self.getMaxCurrentAsMa())
    # specs.append(self.getVoltageDropText())
    # specs.append(self.getBrightnessText())
    # specs.append(self.getWavelengthText())
    filteredSpecs = filter(lambda x: x, specs)
    if filteredSpecs:
      textLines.append(WrappingTextLine(map(lambda t: TextWord(FontType.BASIC, t), filteredSpecs), True))

    if self.getNotes(): textLines.append(self.getNotes())

    self.checkAllPropsUsed()

    return TextEntity(*textLines) if textLines else None

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
