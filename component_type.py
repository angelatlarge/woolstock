#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

def enum(**enums):
  return type('Enum', (), enums)

ComponentType = enum(DIODE=1, LED=2)

componentTypeNames = {ComponentType.DIODE: "diode", ComponentType.LED: "LED"}

def getComponentType(componentName, pluralAllowed=True):
  componentName = componentName.lower().strip()
  for cType, cName in componentTypeNames.iteritems():
      cName = cName.lower().strip()
      print componentName, cName
      if componentName==cName or (pluralAllowed and componentName==cName+"s"):
        return cType
  return None
