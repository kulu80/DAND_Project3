#To store the data into a mongodb database, it could be 
# converted from XML to JSON format. We need to do the following to convert the data from XML format to JSON.

# you should process only 2 types of top level tags: "node" and "way"
# all attributes of "node" and "way" should be turned into regular key/value pairs, except:
 #   - attributes in the CREATED array should be added under a key "created"
 #   - attributes for latitude and longitude should be added to a "pos" array,
 #     for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
# if the second level tag "k" value contains problematic characters, it should be ignored
# if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
# if the second level tag "k" value does not start with "addr:", but contains ":", you can
#  process it in a way that you feel is best. For example, you might split it into a two-level
#  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
# if there is a second ":" that separates the type/direction of a street,
#  the tag should be ignored, for example:
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
address_regex = re.compile(r'^addr\:')
street_regex = re.compile(r'^street')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node['type'] = element.tag
        # let us assign an empty dict to address
        address = {}
        # parse through attributes of all elements
        for attr  in element.attrib:
            if attr in CREATED:
                if 'created' not in node:
                    node['created'] = {}
                node['created'][attr] = element.get(attr)
            elif attr in ['lat', 'lon']:
                continue
            else:
                node[attr] = element.get(attr)
        # finding lattitute and logitude positions
        if 'lat' in element.attrib and 'lon' in element.attrib:
            node['pos'] = [float(element.get('lat')), float(element.get('lon'))]

        # parse second-level tags for nodes
        for e in element:
            # parse second-level tags for ways and populate `node_refs`
            if e.tag == 'nd':
                if 'node_refs' not in node:
                    node['node_refs'] = []
                if 'ref' in e.attrib:
                    node['node_refs'].append(e.get('ref'))

            # throw out not-tag elements and elements without `k` or `v`
            if e.tag != 'tag' or 'k' not in e.attrib or 'v' not in e.attrib:
                continue
            key = e.get('k')
            val = e.get('v')

            # skip problematic characters
            if problemchars.search(key):
                continue

            # parse address k-v pairs
            elif address_regex.search(key):
                key = key.replace('addr:', '')
                address[key] = val

            # catch-all
            else:
                node[key] = val
        # compile address
        if len(address) > 0:
            node['address'] = {}
            street_full = None
            street_dict = {}
            street_format = ['prefix', 'name', 'type']
            # parse through address objects
            for key in address:
                val = address[key]
                if street_regex.search(key):
                    if key == 'street':
                        street_full = val
                    elif 'street:' in key:
                        street_dict[key.replace('street:', '')] = val
                else:
                    node['address'][key] = val
            # assign street_full or fallback to compile street dict
            if street_full:
                node['address']['street'] = street_full
            elif len(street_dict) > 0:
                node['address']['street'] = ' '.join([street_dict[key] for key in street_format])
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
# Print the JSON data type
process_map('raleigh_north-carolina.osm',False)

