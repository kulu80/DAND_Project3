mporting necessary python modules
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import collections
import pymongo
# parsing through the dataset iteratvely to find unique elements in the dataset
def count_tags(filename):
        tags = {}
        for event, elem in ET.iterparse(filename):
            if elem.tag in tags: 
                tags[elem.tag] += 1
            else:
                tags[elem.tag] = 1
        return tags
# Call the function count-tags on the Chicago dataset
tags_raleigh = count_tags('raleigh_north-carolina.osm')
pprint.pprint(tags_raleigh)
