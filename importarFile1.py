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

# we have the old database and it has to be converted to the new structure.
# first will be imported de UsersCES file
# second the Socis CIC file
# and finally Transversal file to complet the database.

###################
## logger config ##
###################

# create loggers
logger = logging.getLogger('File1')
logger.setLevel(logging.DEBUG)
loggerLocked = logging.getLogger('File1.Review')
loggerLocked.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('bitacora-file1.log')
fh.setLevel(logging.DEBUG)
fhLocked = logging.FileHandler('bitacora-report.log')
fhLocked.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(name)s %(levelname)s: %(message)s')
formatterLocked = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
fhLocked.setFormatter(formatterLocked)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
loggerLocked.addHandler(fhLocked)
#loggerLocked.addHandler(ch)

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

##########################
## first file: UsersCES ##
##########################


def file1_cleanRowProcess(row):
    "Clean the data from the CSV"

    # saving telephone numbers enhanced
    # row[10] = PhoneHome
    # row[11] = PhoneWork
    # row[12] = PhoneFax
    # row[13] = PhoneMobile
    phone = row[10]
    cellphone = row[13]
    if re.match(r"6", phone) and cellphone == '':
        cellphone = phone
        phone = ''
    if phone == '':
        if row[11] != '':
            phone = row[11]
        elif row[12] != '':
            phone = row[12]
    phone = phone.replace(' ', '')
    phone = phone.replace('.', '')
    phone = phone.replace('-', '')
    phone = phone.replace('+34', '')
    if re.match(r"0034", phone):
        phone = phone[4:]
    phone = phone[0:9]
    cellphone = cellphone.replace(' ', '')
    cellphone = cellphone.replace('.', '')
    cellphone = cellphone.replace('-', '')
    cellphone = cellphone[0:9]
    cellphone = cellphone.replace('+34', '')
    if re.match(r"0034", cellphone):
        cellphone = cellphone[4:]
    if not re.match(r"[0-9]{9}", phone) and len(phone) > 9:
        phone = ''
    if not re.match(r"[0-9]{9}", cellphone) and len(cellphone) > 9:
        cellphone = ''
    row[10] = phone
    row[13] = cellphone
    # enhanced getting website url
    # row[15] = IM
     # (if beggins with 'http' or 'www' copy to website if empty)
    # row[16] = WebSite
    if row[16] == '':
        if row[15].startswith('www') or row[15].startswith('http'):
            row[16] = row[15]
    # fix postalcode format
    if re.search(r"^[0-9]{4}", row[8]) and len(row[8]) == 4:
        row[8] = '0' + row[8]
    if (not re.search(r"^[0-9]{5}", row[8])) or len(row[8]) != 5:
        row[8] = ''
    # fix data format
    if row[17] != '':
        row[17] = row[17].split(' ')  # get yyyy/mm/dd
        row[17] = row[17][0].replace('/', '-')
    else:
        row[17] = "1984-06-08"
        logger.error("Empty creation data!")


def file1_CreateHuman(row):
    "Process the CSV data related to Human class and saves to the database"

    # save to the db
    hum = GeneralHuman.create(name=row[2], email=row[14],
        telephone_cell=row[13], telephone_land=row[10], website=row[16])
    logger.debug("From:%s creating human:%s", row[0], hum.id)
    return hum


def file1_UpdateHuman(row, humanID):
    "Process the CSV data related to Human class and saves to the database"

    # update to the db
    hum = GeneralHuman.get(GeneralHuman.id == humanID)
    if hum.name == '':
        hum.name = row[2]
    # email keep the database value
    if hum.telephone_cell == '':
        hum.telephone_cell = row[13]
    if hum.telephone_land == '':
        hum.telephone_land = row[10]
    if hum.website == '':
        hum.website = row[16]
    hum.save()
    logger.debug("Updated human:%s", hum.id)


def file1_CreateAddress(row, humanID):
    "Process the CSV data related to Address class and saves to the database"

    # create address
    address = GeneralAddress.create(name='CES address', p_address=row[5],
        ic_larder=0, postalcode=row[8], town=row[6])
    logger.debug("create address: %s", address.id)
    # create relation between person and address
    GeneralRelHumanAddresses.create(
        address=address.id, human=humanID, main_address=1)


def file1_UpdateAddress(row, humanID):
    "Update or create the Address in the database"

    #check if has an address
    try:
        relhumaddr = GeneralRelHumanAddresses.get(
            GeneralRelHumanAddresses.human == humanID)
        addr = GeneralAddress.get(GeneralAddress.id == relhumaddr.address.id)
        if addr.name == '':
            addr.name = "CES address"
        if addr.p_address == '':
            addr.p_address = row[5]
        if addr.postalcode == '':
            addr.postalcode = row[8]
        if addr.town == '':
            addr.town = row[6]
        addr.save()
        logger.debug("Address from %s updated", humanID)
    except DoesNotExist:
        file1_CreateAddress(row, humanID)


def file1_CreatePerson(row):
    "Process the data related to Person Membership and saves to the database"
    # create human
    human = file1_CreateHuman(row)
    #create address
    file1_CreateAddress(row, human.id)
    # create person
    GeneralPerson.create(human=human.id, surnames=row[3])
    # create record of the membership
    record = WelcomeIcRecord.create(name="Alta Soci Individual:" + row[0],
        record_type=SociCoopInd)
    # create membership
    WelcomeIcMembership.create(human=human.id, ic_project=cicProject_parent,
        ic_record=record.id, join_date=row[17], ic_cesnum=row[0])
    # link person to membership
    WelcomeIcPersonMembership.create(ic_membership=record.id, person=human.id)


def file1_UpdatePerson(row, humanID):
    "Gets Person Membership and updates its data to the database"
    # update human
    file1_UpdateHuman(row, humanID)
    # update the person
    person = GeneralPerson.get(GeneralPerson.human == humanID)
    if person.surnames == '':
        person.surnames = row[3]
    person.save()
    # update the address
    file1_UpdateAddress(row, humanID)


def file1_CreateProject(row):
    "Process the data related to Project Membership and saves to the database"
    # TODO: create reference person
    # create human
    human = file1_CreateHuman(row)
    # create address
    file1_CreateAddress(row, human.id)

    # define membership type
    record_type = SociCoopCol
    record_name = "Alta Soci Col·lectiu:" + row[0]
    # select project type
    if row[1] == 'org':
        projType = collectiveProject_type
    elif row[1] == 'cic':
        projType = cicProject_type
    elif row[1] == 'ex':
        projType = exProject_type
    elif row[1] == 'nal':
        projType = nalProject_type
    elif row[1] == 'reb':
        projType = larderProject_type
    elif row[1] == 'pub':
        projType = commonProject_type
        record_type = ProjPublic
        record_name = "Alta Projecte Públic:" + row[0]
    # create project
    GeneralProject.create(human=human.id, project_type=projType,
        parent=cicProject_parent)
    # create membership record
    record = WelcomeIcRecord.create(name=record_name,
        record_type=record_type)
    # create membership
    membership = WelcomeIcMembership.create(human=human.id,
            ic_project=cicProject_parent, ic_record=record.id,
            join_date=row[17], ic_cesnum=row[0])

    # link project to membership
    WelcomeIcProjectMembership.create(ic_membership=membership.ic_record.id,
                                     project=human.id)


def file1_UpdateProject(row, projectID):
    "Update project process"

    # update human
    logger.debug("Updating human:%s", projectID)
    file1_UpdateHuman(row, projectID)
    # update the address
    file1_UpdateAddress(row, projectID)
    # here we don't have info related to GeneralProject class to update


def file1_isCollectiveProject(pt):
    "Guess if the project is collective"

    return pt == 'org' or pt == 'cic' or pt == 'ex' or pt == 'nal'\
        or pt == 'reb' or pt == 'pub'


def file1_UpdateStatus(row):
    if row[18] == '-1':
        # status "locked"
        loggerLocked.info("%s bloquejat",row[0])


def file1_ProcessRow(row):
    "Gets a row from the CSV and stores it's data to the database"

    try:
        # check if exists a member with the CESnumber
        membership = WelcomeIcMembership.get(
            WelcomeIcMembership.ic_cesnum == row[0])
        logger.info("Membership found: %s", membership.ic_cesnum)
        # check the consistency of the database and try to fix it or update it
        try:
            pm = WelcomeIcPersonMembership.get(
                            ic_membership=membership.ic_record.id)
            # update the person data
            logger.info("Updating Person: %s", pm.person.human)
            file1_UpdatePerson(row, pm.person.human)
            file1_UpdateStatus(row)
        except DoesNotExist:
            try:
                projectMem = WelcomeIcProjectMembership.get(
                    WelcomeIcProjectMembership.ic_membership == membership.ic_record.id)
                logger.info("Updating Project: %s", projectMem.project.human)
                # update project data
                file1_UpdateProject(row, projectMem.project.human)
                file1_UpdateStatus(row)
            except DoesNotExist:
                logger.debug("project of %s not found database inconsistent",
                             row[0])
    except DoesNotExist:
        logger.debug("ces number not found: %s", row[0])
        # TODO: create join_fee on the second file
         # here we don't have info
        # row[1] = User Type (adm,ind,org,cic,ex,nal,reb,pub,vir)
        if row[1] == 'ind':
            # create person
            file1_CreatePerson(row)
            logger.info("Added new member: %s", row[0])
            file1_UpdateStatus(row)
        elif file1_isCollectiveProject(row[1]):
            # create project
            file1_CreateProject(row)
            file1_UpdateStatus(row)
            logger.info("Added new project: %s", row[0])
        else:
            logger.debug("avoid %s -> type: %s", row[0], row[1])


def FirstFile(filename):
    "Gets the first file to read and process it"
    
    loggerLocked.info("Llistat usuaris CES Bloquejats")
    
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        try:
            for row in reader:
                file1_cleanRowProcess(row)
                file1_ProcessRow(row)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

