#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import argparse
import math
import cairocffi as cairo
from diode_component import DiodeComponent
from label_sheet import LabelSheet
from component_type import ComponentType
from csv_glob_provider import CsvGlobProvider
from osv_provider import OsvProvider

def main():

  labelSheet = LabelSheet("labels.pdf")
  componentClasses = {ComponentType.DIODE: DiodeComponent}
  # with CsvGlobProvider('diodes.csv') as provider:
  with OsvProvider("../components.ods") as provider:
    for (componentType, componentClass) in componentClasses.iteritems():
      if componentType in provider:
        componentDefinitions = provider[componentType]
        for componentProperties in componentDefinitions:
          component = componentClass(componentProperties)
          labelSheet.draw(component.makeLabel())
        
  #     componentProperties = csvComponents.next()
  #     try:
  #       while componentProperties:
  #         component = DiodeComponent(componentProperties)
  #         labelSheet.draw(component.makeLabel())
  #         componentProperties = csvComponents.next()

  #     except StopIteration:
  #       pass

  #     provider

  # with open('diodes.csv', 'r') as csvfile:
  #   csvComponents = csv.DictReader(csvfile)

  #   labelSheet = LabelSheet("labels.pdf")
  #   componentProperties = csvComponents.next()
  #   try:
  #     while componentProperties:
  #       component = DiodeComponent(componentProperties)
  #       labelSheet.draw(component.makeLabel())
  #       componentProperties = csvComponents.next()

  #   except StopIteration:
  #     pass
  


if __name__ == "__main__":
    main()