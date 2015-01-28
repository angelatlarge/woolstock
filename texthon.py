#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

import csv
import argparse
import math
import cairocffi as cairo
from diodecomponent import DiodeComponent
from labelsheet import LabelSheet

def main():

  with open('diodes.csv', 'r') as csvfile:
    csvComponents = csv.DictReader(csvfile)

    labelSheet = LabelSheet("labels.pdf")
    componentProperties = csvComponents.next()
    try:
      while componentProperties:
        component = DiodeComponent(componentProperties)
        labelSheet.draw(component.makeLabel())
        componentProperties = csvComponents.next()

    except StopIteration:
      pass
  


if __name__ == "__main__":
    main()