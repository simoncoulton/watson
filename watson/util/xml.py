# -*- coding: utf-8 -*-
from xml.etree.ElementTree import Element, SubElement, tostring


def to_string(xml, encoding='utf-8', xml_declaration=False):
    """Outputs an xml.etree.ElementTree.Element object to a string.

    Usage:
        xml = from_dict(data)
        xml_to_string(xml, xml_declaration=True)  # <?xml version ....

    Args:
        string encoding: the encoding used for the xml.
        boolean xml_declaration: whether or not to include the xml declaration.
    """
    declaration = '<?xml version="1.0" encoding="{encoding}" ?>'.format(
        encoding=encoding)
    string = tostring(xml).decode(encoding)
    return '{0}{1}'.format(declaration if xml_declaration else '', string)


def from_dict(obj, node_name='root'):
    """Converts a simple dictionary into an XML document.

    Usage:
        data = {
            'test': {
                'nodes': {
                    'node': [
                        'Testing',
                        'Another node'
                    ]
                },
            }
        }
        xml = from_dict(data)  # <test><nodes><node>Testing</node><node>Another node</node></nodes></test>

    Args:
        string node_name: the initial node name in case there are multiple
                          top level elements.
    """
    def __dict_to_xml(obj, node_name=None, parent_element=None):
        # internal processing for from_dict
        if not isinstance(parent_element, Element):
            if isinstance(obj, dict) and len(obj) == 1:
                node_name, obj = obj.popitem()
            parent_element = Element(node_name)
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (list, tuple)):
                    __dict_to_xml(value, key, parent_element)
                else:
                    __dict_to_xml(value, key, SubElement(parent_element, key))
        elif isinstance(obj, (list, tuple)):
            for value in obj:
                sub_element = SubElement(parent_element, node_name)
                __dict_to_xml(value, node_name, sub_element)
        else:
            parent_element.text = obj
        return parent_element

    return __dict_to_xml(obj, node_name)
