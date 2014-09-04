#  coding: utf8
import csv
import sys
import re
import logging

from peewee import DoesNotExist

from models import WelcomeIcMembership, WelcomeIcRecord
from models import WelcomeIcPersonMembership, WelcomeIcProjectMembership
from models import GeneralHuman, GeneralPerson, GeneralRelHumanAddresses
from models import GeneralAddress, GeneralProject

###################
## logger config ##
###################

# create loggers
logger2 = logging.getLogger('File2')
logger2.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh2 = logging.FileHandler('bitacora-file2.log')
fh2.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch2 = logging.StreamHandler()
ch2.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(name)s %(levelname)s: %(message)s')
fh2.setFormatter(formatter)
ch2.setFormatter(formatter)
# add the handlers to the logger
logger2.addHandler(fh2)
logger2.addHandler(ch2)

#################
## Global vars ##
#################

# project related constants
cicProject_parent = 3
generalProject_type = 13  # general project
collectiveProject_type = 27
larderProject_type = 66
commonProject_type = 26
nalProject_type = 21
exProject_type = 22
cicProject_type = 24

# membership related constants
SociCoopInd = 7
SociCoopCol = 8
ProjPublic = 9
SociAfi = 10
Firaire = 11
QuotaAltaInd = 35
QuotaAltaCol = 36


###########################
## second file: SocisCIC ##
###########################
# things to check in the database:
# - if the COOP number exists add the fee record
# - if the COOP doesn't exists: it's an ERROR
# - check the status of the membership


def SecondFile(filename):
    with open(filename, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        reader = csv.reader(f, dialect)
        try:
            for row in reader:
                if row[1] == 'Sense Info':
                    membership = None
                    try:
                        membership = WelcomeIcMembership.get(
                            WelcomeIcMembership.ic_cesnum == row[0])
                        logger2.info("Membership found: %s",
                            membership.ic_cesnum)
                    except DoesNotExist:
                        logger2.info("Membership not found %s", row[0])
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

