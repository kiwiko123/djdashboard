import pathlib
import xml.etree.ElementTree


class PropertyManager:
    
    @staticmethod
    def _parse_entities(root: xml.etree.ElementTree.Element) -> {str: str}:
        mapping = {}
        for child in root:
            entity_key = child.get('name')
            if entity_key is None:
                raise ValueError('expected <entity .../> tag to have a "name" attribute; none found')
            mapping[entity_key] = {sub.tag: sub.text for sub in child}
        return mapping
    
    def __init__(self, properties_file_path: pathlib.Path):
        if not properties_file_path.is_file():
            raise ValueError('"{0}" is not a valid file'.format(properties_file_path))
        self._tree = xml.etree.ElementTree.parse(str(properties_file_path))
        self._properties = self._parse_entities(self._root)
        
    def __getitem__(self, entity_name: str) -> {str: str}:
        return self.get_entity(entity_name)
    
    @property
    def _root(self) -> xml.etree.ElementTree.Element:
        """ Returns the root tag in properties_file_path as an Element object """
        return self._tree.getroot()
        
    def get_entity(self, name: str) -> {str: str}:
        """ Returns a dictionary of {param: value} pairs as defined in
            the property file's <entity ...> tags.
        """
        if name in self._properties:
            return self._properties[name]
        else:
            raise KeyError('entity "{0}" does not exist; check properties.xml')


if __name__ == '__main__':
    pass