#!/usr/bin/env python
# This Python file uses the following encoding: utf-8

from component_type import ComponentType, getComponentType

class ComponentFilter(object):
  def __init__(self, args):

    self.include_ids = args.include_ids
    self.exclude_ids = args.exclude_ids

    self.includedComponentTypes = []
    if args.include_components:
      if args.exclude_components: raise Exception("Cannot have both include and exclude components")
      for componentTypeName in args.include_components:
        try:
          self.includedComponentTypes.append( getComponentType(componentTypeName))
        except KeyError:
          raise Exception('Invalid component name: "%s"' % (comp))
    elif args.exclude_components:
      excludeComponentTypes = map(lambda cn: getComponentType(cn), args.exclude_components)
      for ct, ctn in componentTypeNames:
        if not ct in excludeComponentTypes:
          self.includedComponentTypes.append(ct)
    elif not self.include_ids:
      for ct, ctn in componentTypeNames:
          self.includedComponentTypes.append(ct)



  def isIncluded(self, componentType, component):
    if self.include_ids and component.id in self.include_ids: return True
    if self.exclude_ids and component.id in self.exclude_ids: return False
    return componentType in self.includedComponentTypes
