#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

def enum(**enums):
  return type('Enum', (), enums)

ComponentType = enum(DIODE=1, LED=2, SEVENSEGMENT=3)

componentTypeNames = {
  ComponentType.DIODE: "diode", 
  ComponentType.LED: "LED", 
  ComponentType.SEVENSEGMENT: "7segment", 
} 

def getComponentType(componentName, pluralAllowed=True):
  componentName = componentName.lower().strip()
  for cType, cName in componentTypeNames.iteritems():
      cName = cName.lower().strip()
      if componentName==cName or (pluralAllowed and componentName==cName+"s"):
        return cType
  return None
