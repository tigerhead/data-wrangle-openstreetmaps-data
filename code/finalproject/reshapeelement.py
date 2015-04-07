#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
from auditzip import  update_zip
from improvestname import  update_name
from auditphone import  format_phone
"""
Wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 


 only 2 types of top level tags: "node" and "way"
all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]


 ```python as the line before the code and ```
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]



def shape_element(element):
    node = {}
    
    #process node and way tags only
    if element.tag == "node" or element.tag == "way" :
        node["id"] = element.attrib["id"]        
        node["type"] =  element.tag        
        node[ "visible"] = element.get("visible")
        created = {}
        created["version"] = element.attrib["version"]
        created["changeset"] = element.attrib["changeset"]
        created["timestamp"] = element.attrib["timestamp"]
        created["user"] = element.attrib["user"]
        created["uid"] = element.attrib["uid"]
        node["created"] = created
        #position latitude and longtitude
        if "lat" in element.keys() and "lon" in element.keys():
           pos = [float(element.attrib["lat"]), float(element.attrib["lon"])]        
           node["pos"] = pos
        else:
           node["pos"] = None
        addr = {}
        
        for tag in element.iter("tag"):
            tag_name = tag.attrib["k"]
            value = tag.attrib["v"]
            
            # process address related tags   
            if "addr" in tag_name and len(tag_name.split(":")) == 2:               
               add_key = tag_name.split(":")[1]              
               if add_key == "street":
                   value = update_name(value)
               elif add_key == "postcode":
                   value = update_zip(value)   
               addr[add_key] = value
               
            elif tag_name == "amenity":
                node["amenity"] = value
            elif  tag_name == "cuisine": 
                 node["cuisine"] = value 
            elif  tag_name == "name": 
                 node["name"] = value
            elif  tag_name == "phone": 
                 value = format_phone(value)
                 node["phone"] = value 
        
        #If address exists
        if len(addr) > 0:
            node["address"] = addr
        
        #for way node process reference nodes
        if element.tag == "way":
            nd_refs = []
            for nd in element.iter("nd"):
                if "ref" in nd.keys():
                   nd_refs.append(nd.get("ref"))
            if len(nd_refs) > 0:
                        node["node_refs"] = nd_refs
                
            
        
        return node
    else:
        return None

def check_null(value):    
    
    if value.strip() == 'null' or value.strip() == 'NULL' or value.strip() == 'Null':
        value = None
        
    
    
    
    return value

def process_map(file_in, pretty = False):
   
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        context = iter(ET.iterparse(file_in, events=('start', 'end')))
        _, root = next(context)
        for event, element in context:
            
            if event == 'start':                 
                el = shape_element(element)
                
                if el:
                    #only get first 50 documents for view how JSON document looks liek                    
                    if len(data) <= 50:
                        data.append(el)
                        
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")
            elif event == 'end':
                root.clear()            
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('C:\learning\DataAnalyst\projects\Proj2\\new_orleans_louisiana.osm', True)    
    pprint.pprint( data)
   

if __name__ == "__main__":
    test()