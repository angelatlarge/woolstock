#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

def enum(**enums):
  return type('Enum', (), enums)

TextAttributes = enum(
  SUBSCRIPT=1, 
)
