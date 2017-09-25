import argparse
import os.path
import pathlib
import sys
import xml.etree.ElementTree

try:
    from commutity import helper
except ImportError:
    pass


class PropertyManager:
    def __init__(self, properties_file_path: pathlib.Path):
        """ properties_file is a pathlib.Path object pointing to a .xml file with the appropriate format """
        if not properties_file_path.is_file():
            raise ValueError('"{0}" is not a valid file'.format(properties_file_path))
        self._tree = xml.etree.ElementTree.parse(str(properties_file_path))
        self._properties = self._parse_entries(self._root)
        
    def __getitem__(self, entity_name: str) -> {str: str}:
        return self.get_entry(entity_name)
    
    def __contains__(self, entity_or_value_name: str) -> bool:
        return entity_or_value_name in self._properties
    
    @property
    def _root(self) -> xml.etree.ElementTree.Element:
        """ Returns the root tag in properties_file_path as an Element object """
        return self._tree.getroot()
        
    def get_entry(self, name: str) -> {str: str}:
        """ Returns a dictionary of {param: value} pairs as defined in
            the property file's <entity ...> tags.
        """
        if name in self:
            return self._properties[name]
        else:
            raise KeyError('entity "{0}" does not exist; check properties.xml')
        
    @staticmethod
    def _parse_entries(root: xml.etree.ElementTree.Element) -> {str: str}:
        mapping = {}
        for child in root:
            entity_key = child.get('name')
            if entity_key is None:
                raise ValueError('expected <entity .../> tag to have a "name" attribute; none found')
            mapping[entity_key] = {sub.tag: sub.text for sub in child}
        return mapping


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Commutity property manager')
    parser.add_argument('-n', '--entity', action='store', help='get values by entity name')
    args = parser.parse_args()
    
    print(os.path.abspath(__file__))
    
    if args.entity:
        if args.entity in manager:
            values = manager[args.entity]
            for key, value in values.items():
                print('{0}={1}'.format(key, value))
