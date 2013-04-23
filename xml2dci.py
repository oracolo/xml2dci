#!/usr/bin/python

import sys
from xml.dom.minidom import parse
from optparse import OptionParser

parser = OptionParser(usage = "%prog source.xml <destination.csv>")
parser.add_option("-j", "--judges", dest="judges", action="store_true", default=False,
                  help="includes judges in the csv")
parser.add_option("-s", "--scorekeepers", dest="scorekeepers", action="store_true", default=False,
                  help="includes scorekeepers in the csv")
parser.add_option("-n", "--no-players", dest="noplayers", action="store_true", default=False,
                  help="skips players in the csv")

(options, args) = parser.parse_args()

count = 0
roles = []

if options.judges:
    roles.append("JG")
if options.scorekeepers:
    roles.append("SK")
if not options.noplayers:
    roles.append("PL")

if (len(args) > 0):
    xmlFile = args[0]
    if (len(args) == 2):
        csvFile = args[1]
    else:
        if xmlFile[-3:] == "xml":
            csvFile = xmlFile[:-3] + "csv"
        else:
            csvFile = xmlFile + "csv"
    try:
        torneo = parse(xmlFile)
        csvFile = open(csvFile, 'w')
    except IOError:
        print "Source file not found or unable to write to destination file."
    else:
        for role in torneo.getElementsByTagName('role'):
            if role.attributes['cd'].value in roles:
                for person in role.getElementsByTagName('ref'):
                    csvFile.write(person.getAttribute('person') + '\n')
                    count += 1

        #for person in torneo.getElementsByTagName('person'):
        #    csvFile.write(person.getAttribute('id') + '\n')
            
        csvFile.close()
        print("%d record(s) exported" % count)
else:
    parser.print_help()



