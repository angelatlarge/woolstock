#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import csv
from ssconverter import SSConverter
from component_type import ComponentType, getComponentType
import os
from os.path import basename, splitext

class OdsProvider:
  def __init__(self, sourceFilename):
    self.components = {}
    ssconverter = SSConverter()
    self.outputFilenames = ssconverter.convert(sourceFilename, "%s")

    for filename in self.outputFilenames:
      bareFilename = splitext(basename(filename))[0].lower().strip()
      componentType = getComponentType(bareFilename)
      if componentType:
          self.components[componentType] = csv.DictReader(open(filename, 'r'))

  def __getitem__(self, itemName):
    return self.components[itemName]

  def __contains__(self, itemName):
    return itemName in self.components

  def __enter__(self):
    return self
    
  def __exit__(self, type, value, traceback):
    for filename in self.outputFilenames:
      os.remove(filename)
