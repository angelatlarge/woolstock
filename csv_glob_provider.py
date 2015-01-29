#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import csv
import glob
from os.path import basename, splitext
from component_type import ComponentType, componentTypeNames

class CsvGlobProvider:
  def __init__(self, globExpression):

    self.components = {}
    for (k, v) in componentTypeNames.iteritems():
      print v
      for filename in glob.glob(globExpression):
        bareFilename = splitext(basename(filename))[0].lower().strip()
        bareName = v.lower().strip()
        if bareFilename == bareName or bareFilename == bareName+"s":
          self.components[k] = csv.DictReader(open(filename, 'r'))

    print self.components

  def __getitem__(self, itemName):
    return self.components[itemName]

  def __contains__(self, itemName):
    return itemName in self.components

  def __enter__(self):
    return self
    
  def __exit__(self, type, value, traceback):
    pass