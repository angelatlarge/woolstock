#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import argparse
import math
import cairocffi as cairo
from diode_component import DiodeComponent
from led_component import LedComponent
from label_sheet import LabelSheet
from component_type import ComponentType
from csv_glob_provider import CsvGlobProvider
from ods_provider import OdsProvider

def main():
  parser = argparse.ArgumentParser(description='Make electronics labels')
  parser.add_argument('output', help='Name of the output PDF file')
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('--ods', help='ODS source')
  group.add_argument('--csv', help='CSV source')
  args = parser.parse_args()



  labelSheet = LabelSheet(args.output)
  componentClasses = {ComponentType.DIODE: DiodeComponent, ComponentType.LED: LedComponent}
  # with OsvProvider("../components.ods") as provider:
  with makeProviderFromParsedArgs(args) as provider:
    for (componentType, componentClass) in componentClasses.iteritems():
      if componentType in provider:
        componentDefinitions = provider[componentType]
        for componentProperties in componentDefinitions:
          component = componentClass(componentProperties)
          labelSheet.draw(component.makeLabel())
        
def makeProviderFromParsedArgs(args):
  providerMap = {'ods': OdsProvider, 'csv': CsvGlobProvider}
  foundNames = 0
  for name in providerMap.iterkeys():
    if name in args and args.__dict__[name]:
      foundNames += 1
  if foundNames < 1: raise Exception("A source must be provided")
  if foundNames > 1: raise Exception("Only one source may be provided")
  for name, providerClass in providerMap.iteritems():
    if name in args:
      return providerClass(args.__dict__[name])

if __name__ == "__main__":
    main()