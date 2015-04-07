'''
Created on Feb 26, 2015

@author: ml8523
'''
import xml.etree.ElementTree as ET
import pprint
import re
from collections import defaultdict
from test.test_typechecks import Integer
"""
This module audit zip code in OSM dataset finding invalid zip code format
and zip code out New Orleans zip code range. 
"""


#regular expression for US zip code
zip_code_re = re.compile(r'^\d{5}(-\d{4})?$')
non_decimal = re.compile(r'[^\d]+')


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#zip code list for New Orleans metropolitan  
zip_range = [70112,
70113,
70114,
70115,
70116,
70117,
70118,
70119,
70121,
70122,
70123,
70124,
70125,
70126,
70127,
70128,
70129,
70130,
70131,
70139,
70140,
70141,
70142,
70143,
70145,
70146,
70148,
70149,
70150,
70151,
70152,
70153,
70154,
70156,
70157,
70158,
70159,
70160,
70161,
70162,
70163,
70164,
70165,
70166,
70167,
70170,
70172,
70174,
70175,
70176,
70177,
70178,
70179,
70181,
70182,
70183,
70184,
70185,
70186,
70187,
70189,
70190,
70195]



#find zip code out of rang or in wrong format
def audit_zip_code(wrong_zip_codes, out_of_range,zip_code ):
    m = zip_code_re.match(zip_code)
   
    print zip_code
    if not m:        
        print 'Wrong zip: ' + zip_code       
        wrong_zip_codes.append(zip_code)
        
    else:
        if int(zip_code) not in zip_range and zip_code not in out_of_range:
            out_of_range.append(zip_code)
        

            
           


def is_zip_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

#correct zip code in wrong format
def update_zip(zip):
    
    if zip.startswith("LA") :
       zip = non_decimal.sub('', zip)  
    
    return zip


def process_map(filename):
   
    wrong_zip_codes = []
    out_of_range = []
    
    context = iter(ET.iterparse(filename, events=('start', 'end')))
    _, root = next(context)
    for event, element in context:
        
        if event == 'start':  
           
            if element.tag == "node" or element.tag == "way":
                for tag in element.iter("tag"):
                   if is_zip_code(tag):
                     audit_zip_code(wrong_zip_codes, out_of_range, tag.attrib['v'])
        elif event == 'end':
            root.clear()
            

    return  wrong_zip_codes, out_of_range



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertions will be incorrect then.
    #keys = process_map('C:\learning\DataAnalyst\SampleData\lesson2\example.osm')
    #keys = process_map('C:\learning\DataAnalyst\projects\Proj2\chengdu_china.osm')
    #wrong_zip_codes, out_of_range = process_map('C:\\learning\\DataAnalyst\\projects\\Proj2\\new_orleans_louisiana.osm')
    #pprint.pprint(wrong_zip_codes)
    #pprint.pprint(out_of_range)
    zip = update_zip('LA 70116')
    print zip
   # assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()