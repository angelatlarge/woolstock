#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

def enum(**enums):
  return type('Enum', (), enums)

ComponentType = enum(DIODE=1, LED=2)

