'''
Created on Feb 26, 2015

@author: Min Lai
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
from collections import defaultdict
"""
This module audit address all tags in OSM dataset and try to find tag with problematic  characters
and also audit street type names to find different street name type than expected list.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

"""
Classify tag type and count number appearances of each tag types
"""
def key_type(element, keys):
    if element.tag == "tag":
       
       key = element.get("k") 
       #if tag is all lower case
       if re.match(lower, key) :
            if key in  keys["lower"].keys():
                keys["lower"][key] += 1
            else:
                keys["lower"][key] = 1    
                print key
       #if tag lower case and has colon         
       elif   re.match(lower_colon, key) : 
                if key in  keys["lower_colon"].keys():
                    keys["lower_colon"][key] += 1
                else:
                    keys["lower_colon"][key] = 1              
                    print key
       #if tag has problematic   char             
       elif  re.search(problemchars, key) : 
                if key in  keys["problemchars"].keys():
                    keys["problemchars"][key] += 1
                else:
                    keys["problemchars"][key] = 1       
                    print 'problematic key: ' + key
       else:
            if key in  keys["other"].keys():
                keys["other"][key] += 1
            else:
                keys["other"][key] = 1        
                
        
    return keys




def process_map(filename):
    keys = {"lower": {}, "lower_colon": {}, "problemchars": {}, "other": {}}
    unexpected_street_types = defaultdict(set)
    
    context = iter(ET.iterparse(filename, events=('start', 'end')))
    _, root = next(context)
    for event, element in context:
        
        if event == 'start':  
            keys = key_type(element, keys)
            
        elif event == 'end':
            root.clear()
            

    return keys, unexpected_street_types 



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertions will be incorrect then.
    #keys = process_map('C:\learning\DataAnalyst\SampleData\lesson2\example.osm')
    #keys = process_map('C:\learning\DataAnalyst\projects\Proj2\chengdu_china.osm')
    keys, unexpected_street_types = process_map('C:\\learning\\DataAnalyst\\projects\\Proj2\\new_orleans_louisiana.osm')
    pprint.pprint(keys)
    pprint.pprint(unexpected_street_types)
   # assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()