#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from label_sheet import FontType, LabelSheet
from label_text import TextEntity, TextWord, SingleTextLine, WrappingTextLine
from component import Component

class GenericComponent(Component):

  def makeLabel(self):

    textLines = []

    source = self.getSource()
    if source: textLines.append(source)

    category = self.getProp("Category")
    if category:
      textLines.extend(map(lambda cline: SingleTextLine([TextWord(FontType.BASIC, cline)]), category.split("\n")))

    heading = self.getProp("Heading")
    if heading:
      textLines.extend(map(lambda hline: SingleTextLine([TextWord(FontType.MAJOR, hline)]), heading.split("\n")))

    description = self.getProp("Description")
    if description:
      textLines.append(WrappingTextLine(map(lambda word: TextWord(FontType.BASIC, word), description.split())))

    if self.getNotes(): textLines.append(self.getNotes())

    self.checkAllPropsUsed()

    return TextEntity(*textLines) if textLines else None

