#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import csv
from ssconverter import SSConverter
from component_type import ComponentType, componentTypeNames
import os
from os.path import basename, splitext

class OsvProvider:
  def __init__(self, sourceFilename):
    self.components = {}
    ssconverter = SSConverter()
    self.outputFilenames = ssconverter.convert(sourceFilename, "%s")
    for (k, v) in componentTypeNames.iteritems():
      for filename in self.outputFilenames:
        bareFilename = splitext(basename(filename))[0].lower().strip()
        bareName = v.lower().strip()
        if bareFilename == bareName or bareFilename == bareName+"s":
          self.components[k] = csv.DictReader(open(filename, 'r'))
          # self.components[k] = csv.DictReader(filename)

  def __getitem__(self, itemName):
    return self.components[itemName]

  def __contains__(self, itemName):
    return itemName in self.components

  def __enter__(self):
    return self
    
  def __exit__(self, type, value, traceback):
    for filename in self.outputFilenames:
      os.remove(filename)
