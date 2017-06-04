# Before processing the data and add it into a database
# we should check the "k" value for each "" (there are 886,324 tag 
# elements in the dataset as showen in the above result) and see if 
# there are any potential problems.

import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        for tag in element.iter('tag'):
            k = tag.get('k')
            if lower.search(k):
                keys['lower'] += 1
            elif lower_colon.search(k):
                keys['lower_colon'] += 1
            elif problemchars.search(k):
                keys['problemchars'] += 1
            else:
                keys['other'] += 1
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys
raleigh_keys = process_map('raleigh_north-carolina.osm')
pprint.pprint(raleigh_keys)

#people invovlved in the map editing.
def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        for ele in element:
            if 'uid' in ele.attrib:
                users.add(ele.attrib['uid'])
    return users
users = process_map('raleigh_north-carolina.osm')
len(users)
from collections import defaultdict

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Avenue", "Boulevard", "Commons", "Court", "Drive", "Lane", "Parkway", 
                         "Place", "Road", "Square", "Street", "Trail"]

mapping = {'Ave'  : 'Avenue',
           'Blvd' : 'Boulevard',
           'Dr'   : 'Drive',
           'Dr.'  : 'Drive',
           'Blvd.': 'Boulevard',
           'Ln'   : 'Lane',
           'Pkwy' : 'Parkway',
           'Pky'  : 'Parkway',
           'Rd'   : 'Road',
           'Rd.'   : 'Road',
           'St'   : 'Street',
           'St,'  : 'Street',
           'street' :"Street",
           'Ct'   : "Court",
           'Cir'  : "Circle",
           'Cr'   : "Court",
           'ave'  : 'Avenue',
           'Hwg'  : 'Highway',
           'Hwy'  : 'Highway',
           'Sq'   : "Square"}

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types
streettypes_raleigh = audit('raleigh_north-carolina.osm')
pprint.pprint(dict(streettypes_raleigh))

