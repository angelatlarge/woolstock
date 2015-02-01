#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import argparse
import math
import cairocffi as cairo
from diode_component import DiodeComponent
from led_component import LedComponent
from seven_segment_component import SevenSegmentComponent
from label_sheet import LabelSheet
from component_type import ComponentType, getComponentType
from csv_glob_provider import CsvGlobProvider
from ods_provider import OdsProvider
from component_filter import ComponentFilter

def main():
  parser = argparse.ArgumentParser(description='Make electronics labels')
  parser.add_argument('output', help='Name of the output PDF file')
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('--ods', help='ODS source')
  group.add_argument('--csv', help='CSV source')
  parser.add_argument('-g', '--grid', help='Draw label grid', action='store_true')
  parser.add_argument('--start', help='Start position for the first label', nargs=2, type=int)
  parser.add_argument('-I', '--include_components', help='Names of components to draw', nargs='*', type=str)
  parser.add_argument('-E', '--exclude_components', help='Names of components to exclude', nargs='*', type=str)
  parser.add_argument('-i', '--include_ids', help='Names of components to draw', nargs='*', type=int)
  parser.add_argument('-e', '--exclude_ids', help='Names of components to exclude', nargs='*', type=int)
  parser.add_argument('--exclude_labels', help='Coordinates of labels to exclude', nargs=2, type=int, action='append')
  args = parser.parse_args()



  labelSheet = LabelSheet(args.output, None, getLabelExclusions(args))
  if args.grid:   labelSheet.draw_background_labels()
  if args.start: labelSheet.moveToLabel(args.start[0], args.start[1])
  componentClasses = {
    ComponentType.DIODE: DiodeComponent, 
    ComponentType.LED: LedComponent, 
    ComponentType.SEVENSEGMENT: SevenSegmentComponent, 
  }


  # with OsvProvider("../components.ods") as provider:
  componentFilter = ComponentFilter(args)
  with makeProviderFromParsedArgs(args) as provider:
    for (componentType, componentClass) in componentClasses.iteritems():
      if componentType in provider:
        componentDefinitions = provider[componentType]
        for componentProperties in componentDefinitions:
          component = componentClass(componentProperties)
          if componentFilter.isIncluded(componentType, component):
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

def getComponentClasses(args):
  if args.comps:
    filteredClasses = {}
    for comp in args.comps:
      componentType = getComponentType(comp)
      try:
        filteredClasses[componentType] = componentClasses[componentType]
      except KeyError:
        raise Exception('Invalid component name: "%s"' % (comp))
    return filteredClasses
  else:
    return componentClasses

def getLabelExclusions(args):
  labelExclusions = []
  if args.exclude_labels:
    for x, y in args.exclude_labels:
      labelExclusions.append((x, y))
  return labelExclusions


if __name__ == "__main__":
    main()