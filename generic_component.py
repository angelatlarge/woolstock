#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_sheet import FontType, LabelSheet
from label_block import LabelBlock
from label_line import LabelLine, SingleLabelLine, WrappingLabelLine
from label_text import LabelText
from component import Component

class GenericComponent(Component):

  def makeLabel(self):

    labelLines = []

    source = self.getSource()
    if source: labelLines.append(source)

    category = self.getProp("Category")
    if category:
      labelLines.extend(map(lambda cline: SingleLabelLine([LabelText(FontType.BASIC, cline)]), category.split("\n")))

    heading = self.getProp("Heading")
    if heading:
      labelLines.extend(map(lambda hline: SingleLabelLine([LabelText(FontType.MAJOR, hline)]), heading.split("\n")))

    description = self.getProp("Description")
    if description:
      labelLines.append(WrappingLabelLine(map(lambda word: LabelText(FontType.BASIC, word), description.split())))

    if self.getNotes(): labelLines.append(self.getNotes())

    self.checkAllPropsUsed()

    return LabelBlock(*labelLines) if labelLines else None

