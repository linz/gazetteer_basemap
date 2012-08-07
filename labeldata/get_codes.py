from lxml import etree
import sys
import csv

if len(sys.argv) != 3:
    print "Require tdd_file and output_file name parameters"
    sys.exit()

tdd=etree.parse(open(sys.argv[1]))
csvf=csv.writer(open(sys.argv[2],"wb"))
csvf.writerow(['code','value'])


root=tdd.getroot()
# Get the default namespace
tddns=root.nsmap[None]
# Create a namespace map using this
nsm={'tdd':tddns}

# Select all the codes for the point_description_code attribute

for v in root.findall('.//tdd:attribute[@name="point_description_code"]/tdd:values/tdd:value',nsm):
    csvf.writerow([v.attrib['text'],v.attrib['description']])
