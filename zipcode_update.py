# Using part of the above codes let check zipcodes for uniformity 
# or consitency. We can see from the result that the zipcode formatting 
# is inconsistent. There are zipcodes which are not in the area that start 
# with '26', some zipcodes have only 4 digits, the other zipcodes have formats
# like '27513-3507' and '275198404' which show inconsistency in the zipcode formatting
# Let check zipcode for inconsistency 
from collections import defaultdict

def audit_zipcode(invalid_zipcodes, zipcode):
    twoDigits = zipcode[0:2]
    
    if not twoDigits.isdigit():
        invalid_zipcodes[twoDigits].add(zipcode)
    
    elif twoDigits != 27:
        invalid_zipcodes[twoDigits].add(zipcode)
        
def is_zipcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_zip(osmfile):
    osm_file = open(osmfile, "r")
    invalid_zipcodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zipcode(tag):
                    audit_zipcode(invalid_zipcodes,tag.attrib['v'])

    return invalid_zipcodes

zipcode_raleigh = audit_zip('raleigh_north-carolina.osm')
pprint.pprint(dict(zipcode_raleigh))
# updating zipcode 

def update_name(zipcode):
    testNum = re.findall('[a-zA-Z]*', zipcode)
    if testNum:
        testNum = testNum[0]
    testNum.strip()
    if testNum == "CA":
        updatedzcode = (re.findall(r'\d+', zipcode))
        if updatedzcode:
            if updatedzcode.__len__() == 2:
                return (re.findall(r'\d+', zipcode))[0] + "-" +(re.findall(r'\d+', zipcode))[1]
            else:
                return (re.findall(r'\d+', zipcode))[0]

for street_type, ways in zipcode_raleigh.iteritems():
    for name in ways:
        better_name = update_name(name)
        print name, "=>", better_name
