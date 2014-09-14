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
loggerData = logging.getLogger('membershipReview')
loggerData.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh2 = logging.FileHandler('bitacora-file2.log')
fh2.setLevel(logging.DEBUG)
fhData = logging.FileHandler('membershipsReview.log')
fhData.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch2 = logging.StreamHandler()
ch2.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(name)s %(levelname)s: %(message)s')
fh2.setFormatter(formatter)
fhData.setFormatter(formatter)
ch2.setFormatter(formatter)
# add the handlers to the logger
logger2.addHandler(fh2)
loggerData.addHandler(fhData)
loggerData.addHandler(ch2)
logger2.addHandler(ch2)

#################
## Global vars ##
#################

###########################
## second file: SocisCIC ##
###########################
# things to check in the database:
# - if the COOP number exists add the fee record
# - if the COOP doesn't exists: it's an ERROR
# - check the status of the membership

def file2_addFee(row, membership):
    # TODO
    return None

def SecondFile(filename):
    logger2.info("Hello file2")
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
                        if row[1] == 'Actiu CIC':
                            # add membership fee
                            file2_addFee(row, membership)
                        elif row[1] == 'Baixa CIC':
                            loggerData.warning("%s: Soci donat de baixa",row[0])
                        elif row[1] == 'Sense Info':
                            loggerData.info("%s: Soci 'Sense Info'", membership.ic_cesnum)

                    except DoesNotExist:
                        loggerData.info("%s: Membership not found", row[0])
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

