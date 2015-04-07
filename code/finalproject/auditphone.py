'''
Created on Feb 26, 2015

@author: ml8523
'''
import xml.etree.ElementTree as ET
import pprint
import re
from collections import defaultdict
"""
Your task is to explore the data a bit more.
Before you process the data and add it into MongoDB, you should
check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data model
and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with problematic characters.
Please complete the function 'key_type'.
"""



phone_re = re.compile(r'^([+]1\s*[-\/\.]?)?(\((\d{3})\)|(\d{3}))\s*[-\/\.]?\s*(\d{3})\s*[-\/\.]?\s*(\d{4})\s*(([xX]|[eE][xX][tT])\.?\s*(\d+))*$')

expected_pattern = ['^[1-9]\d{2}-\d{3}-\d{4}',
                    '^\(\d{3}\)\s\d{3}-\d{4}',
                    '^[1-9]\d{2}\s\d{3}\s\d{4}',
                    '^[1-9]\d{2}\.\d{3}\.\d{4}'
                   ]
                  

non_decimal = re.compile(r'[^\d]+')


"""
Audit phone number format using regular expression. 
If phone is not in right format, report in invalid_phone list
"""
def audit_phone(invalid_phone,  unexpected_format,  phone):
    m = phone_re.match(phone)
    #print m
    print phone
    
    if not m:        
        print 'invalid phone: ' + phone       
        invalid_phone.append(phone)
    else: #phone is valid but format is different than expected, add it a list        
        for pattern in expected_pattern: 
            if not re.match(pattern, phone):
                unexpected_format.append(phone)
        
            
           


def is_phone(elem):
    return (elem.attrib['k'] == "phone")
"""
format phone number to XXX-XXX-XXXX like 504-234-7865
"""
def format_phone(phone):
    
    #strip all non-numeric characters
    ph = non_decimal.sub('', phone) 
    l = len(ph)
    
    if l == 10:  #if 10 digit number
        ph = ph[0 : 3] + '-' + ph[3 : 6] + '-' + ph[6:]
    elif l == 11: #if 10 digit number
        ph = ph[1 : 4] + '-' + ph[4 : 7] + '-' + ph[7:]
    elif l == 7: #if 10 digit number adding area code New Orleans only has 504 area code
        ph = '504' +  ph[0 : 3] + ph[3 :]
    elif l > 11: #number having extension
        if ph.startswith("1"):
            ph = ph[1:]
            
        ph = ph[0 : 3] + '-' + ph[3 : 6] + '-' + ph[6: 10] + 'x' + ph[10:]     
            
      
        
    phone = ph
    
    return phone


def process_map(filename):
   # keys = {"lower": {}, "lower_colon": {}, "problemchars": {}, "other": {}}
    invalid_phone = []
    unexpected_format = []    
    context = iter(ET.iterparse(filename, events=('start', 'end')))
    _, root = next(context)
    
    for event, element in context:
        
        if event == 'start':           
            if element.tag == "node" or element.tag == "way":
                for tag in element.iter("tag"):                   
                   if is_phone(tag):
                     audit_phone(invalid_phone, unexpected_format, tag.attrib['v'])
        elif event == 'end':
            root.clear()
            

    return  invalid_phone, unexpected_format



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertions will be incorrect then.
    #keys = process_map('C:\learning\DataAnalyst\SampleData\lesson2\example.osm')
    #keys = process_map('C:\learning\DataAnalyst\projects\Proj2\chengdu_china.osm')
    invalid_phone, unexpected_format = process_map('C:\\learning\\DataAnalyst\\projects\\Proj2\\new_orleans_louisiana.osm')
    print "invalid phone: "
    pprint.pprint(invalid_phone)
    print "different format: "
    pprint.pprint(unexpected_format)
    
   # assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()