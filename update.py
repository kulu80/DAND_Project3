# The function takes a string with street name as an argument and 
# should return the fixed name This last function update_name is the 
# last step of the process, which take the old name and update them with a better name
def update_name(name, mapping, regex):
    m = regex.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            name = re.sub(regex, mapping[street_type], name)

    return name

for street_type, ways in streettypes_raleigh.iteritems():
    for name in ways:
        better_name = update_name(name, mapping, street_type_re)
        print name, "=>", better_name
if name == 'Blue Ridge Rd':
    assert better_name == 'Blue Ridge Road'
if name == 'Chapel Hill Rd':
    assert better_name == 'Chapel Hill Road'  
