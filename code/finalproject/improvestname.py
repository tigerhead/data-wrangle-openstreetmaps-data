'''
Created on Feb 13, 2015

@author: Min Lai
'''
"""
This module audit street type names to find different street name type than expected list the audit tag module. 
And it provide function to update street type name to uniform name based on auditing result
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "C:\learning\DataAnalyst\projects\Proj2\\new_orleans_louisiana.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# Street abbreviation and name mapping
mapping = { "St": "Street",
            "St.": "Street",
            "Rd" : "Road",
            "Rd." : "Road",
            "RD" : "Road",
            "RD." : "Road",
            "Blvd" : "Boulevard",
            "Ave" : "Avenue",
            "Ave." : "Avenue",
            "Dr" : "Drive",
            "Dr." : "Drive",
            "dr" : "Drive",
            "Ct" : "Court",
            "Pl" : "Place",
            "PL" : "Place",
            "Pl." : "Place",
            "Cut-Of": "Cut-off",
            "Hwy": "Highway",
            "Pky": "Parkway",
            "Steeet": "Street",
            "Rerre": "Terre",
            "Circe" : "Circle",
            "LOOP"  : "Loop"
            }

"""
find unexpected strret types
"""
def audit_street_type(unexpected_street_types, street_name):
    m = street_type_re.search(street_name)
   
    if m:
        street_type = m.group()
        print street_type
        if street_type not in expected:
            unexpected_street_types[street_type].add(street_name)
           


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def process_map(osmfile):
    osm_file = open(osmfile, "r")
    unexpected_street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(unexpected_street_types, tag.attrib['v'])

    return unexpected_street_types

"""
Update street type name to uniform name based mapping

"""
def update_name(name):

   
    m = street_type_re.search(name)
    
    if m:
        street_type = m.group()
        for key in mapping.keys():
           if key == street_type:
             name = name.replace(key, mapping[key])
             break

    return name


def test():
    unexpected_street_types = process_map(OSMFILE)
    
    pprint.pprint(dict(unexpected_street_types))

    


if __name__ == '__main__':
    test()