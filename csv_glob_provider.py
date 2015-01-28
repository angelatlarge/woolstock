#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
import glob
from os.path import basename
from component_type import ComponentType



class CsvGlobProvider:
  def __init__(self, globExpression):
    componentTypeNames = {ComponentType.DIODE: "diode", ComponentType.LED: "LED"}

    self.components = {}
    for (k, v) in componentTypeNames.iteritems():
      for filename in glob.glob(globExpression):
        if basename(filename).lower().strip() == v:
          self.components[k] = csv.DictReader(open(filename, 'r'))

  def __getitem__(self, itemName):
    return self.components[itemName]

  def __contains__(self, itemName):
    return itemName in self.components


# now you can call it directly with basename
print basename("/a/b/c.txt")    