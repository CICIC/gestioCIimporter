# coding: utf8
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

# create logger with 'spam_application'
logger = logging.getLogger('gestioCIimporter')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('bitacora-debug.log')
fh.setLevel(logging.DEBUG)
#fh2 = logging.FileHandler('bitacora-warning.log')
#fh2.setLevel(logging.WARNING)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(name)s %(levelname)s: %(message)s')
fh.setFormatter(formatter)
#fh2.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
#logger.addHandler(fh2)
logger.addHandler(ch)

#################
## Global vars ##
#################

#project related constants
cicProject_parent = 3
generalProject_type = 13  # general project
collectiveProject_type = 27
larderProject_type = 66
commonProject_type = 26
nalProject_type = 21
exProject_type = 22
cicProject_type = 24

#membership related constants
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
# things to check in the database:
# - if the COOP number exists don't do anything
# - if the COOP doesn't exists: create user? create Person and IcMembership
# ----
# list of the content of each field
#row[0] = UID (COOP number)
#row[1] = User Type (adm,ind,org,cic,ex,nal,reb,pub,vir)
 #adm:admin(avoid), com:company, fam:shared, ind:individual,
 #org:organitzation, pub:public, vir:virtual(avoid)
#row[2] = Firstname
#row[3] = Surname
#row[4] = OrgName (Name of the col·lective project)
#row[5] = Address1
#row[6] = Address2
#row[7] = Address3 (Barri/Zona)
#row[8] = Postcode (only 5digits)
#row[9] =  SubArea ( != comarca)
#row[10] = PhoneHome
 #(if beggins with 6 and Mobile empty move to mobile)
#row[11] = PhoneWork
 #(if begins with 6 and Mobile empty move to mobile)
#row[12] = PhoneFax
 #(if no phonehome and no phonework, try to get this, else discard)
#row[13] = PhoneMobile
#row[14] = Email
#row[15] = IM
 #(if beggins with 'http' or 'www' copy to website if empty)
#row[16] = WebSite
#row[17] = Created (join_date)
#row[18] = Locked (if locked avoid to import)


def file1_CreateHuman(row):
    "Process the CSV data related to Human class and saves to the database"

    #saving telephone numbers enhanced
    #row[10] = PhoneHome
    #row[11] = PhoneWork
    #row[12] = PhoneFax
    #row[13] = PhoneMobile
    phone = row[10]
    if row[10] == '':
        if row[11] != '':
            phone = row[11]
        elif row[12] != '':
            phone = row[12]
    #enhanced getting website url
    #row[15] = IM
     #(if beggins with 'http' or 'www' copy to website if empty)
    #row[16] = WebSite
    if row[16] == '':
        if row[15].startswith('www') or row[15].startswith('http'):
            row[16] = row[15]
    #save to the db
    hum = GeneralHuman.create(name=row[2], email=row[14],
        telephone_cell=row[13], telephone_land=phone, website=row[16])
    logger.debug("From:%s creating human:%s", row[0], hum.id)
    return hum


def file1_CreateAddress(row, human):
    "Process the CSV data related to Address class and saves to the database"

    #fix postalcode format
    cp = row[8]
    if re.search(r"[0-9]{4}", cp):
        cp = '0' + cp
    if not re.search(r"[0-9]{5}", cp):
        cp = ''
    #create address
    address = GeneralAddress.create(name='CES address', p_address=row[5],
        ic_larder=0, postalcode=cp, town=row[6])
    logger.debug("create address: %s", address.id)
    #create relation between person and address
    GeneralRelHumanAddresses.create(
        address=address.id, human=human.id, main_address=0)
    logger.debug("Address %s linked to human.id:%s", address.id, human.id)


def file1_CreatePerson(row):
    "Process the data related to Person Membership and saves to the database"
    #create human
    human = file1_CreateHuman(row)
    #create address
    file1_CreateAddress(row, human)
    #create person
    GeneralPerson.create(human=human.id, surnames=row[3])
    logger.debug("Create person: %s", human.id)
    #create record of the membership
    record = WelcomeIcRecord.create(name="Alta Soci Individual:" + row[0],
        record_type=SociCoopInd)
    logger.debug("created record %s", record.id)
    #fix data format
    if row[17] != "":
        data = row[17].split(' ')  # get yyyy/mm/dd
        data = data[0].replace('/', '-')
    else:
        data = "1984-06-08"
        logger.error("Empty creation data!")
    #create membership
    WelcomeIcMembership.create(human=human.id, ic_project=cicProject_parent,
        ic_record=record.id, join_date=data, ic_cesnum=row[0])
    logger.debug("created %s Membership %s", row[0], record.id)
    #link person to membership
    WelcomeIcPersonMembership.create(ic_membership=record.id, person=human.id)
    logger.debug("Person %s linked to membership %s", human.id, record.id)


def file1_CreateProject(row):
    "Process the data related to Project Membership and saves to the database"

    #create human
    human = file1_CreateHuman(row)
    #create address
    file1_CreateAddress(row, human)

    #define membership type
    record_type = SociCoopCol
    record_name = "Alta Soci Col·lectiu:" + row[0]
    #select project type
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
    #create project
    GeneralProject.create(human=human.id, project_type=projType,
        parent=cicProject_parent, social_web=row[16])
    #create membership record
    record = WelcomeIcRecord.create(name=record_name,
        record_type=record_type)
    if row[17] != '':
        data = row[17].split(' ')  # get yyyy/mm/dd
        data = data[0].replace('/', '-')
    else:
        data = "1984-06-08"
        logger.error("Empty creation data!")
    #create membership
    membership = WelcomeIcMembership.create(human=human.id,
            ic_project=cicProject_parent, ic_record=record.id,
            join_date=data, ic_cesnum=row[0])
    logger.debug("Membership %s created", record.id)

    #link project to membership
    WelcomeIcProjectMembership.create(ic_membership=membership.ic_record.id,
                                     project=human.id)
    logger.debug("Project %s linked to membership %s", human.id, record.id)


def isCollectiveProject(pt):
    "Guess if the project is collective"

    return pt == 'org' or pt == 'cic' or pt == 'ex' or pt == 'nal'\
        or pt == 'reb' or pt == 'pub'


def ProcessRow(row):
    "Gets a row from the CSV and stores it's data to the database"

    try:
        #check if exists a member with the CESnumber
        membership = WelcomeIcMembership.get(
            WelcomeIcMembership.ic_cesnum == row[0])
        logger.info("Membership found: %s", membership.ic_cesnum)
        #check the consistency of the database and try to fix it
        #maybe another day...
    except DoesNotExist:
        logger.debug("ces number not found: %s", row[0])
        #TODO: create join_fee on the second file
         #here we don't have enough info
        #row[1] = User Type (adm,ind,org,cic,ex,nal,reb,pub,vir)
        if row[1] == 'ind':
            #create person
            file1_CreatePerson(row)
            logger.info("afegit soci coop ind: %s", row[0])
        elif isCollectiveProject(row[1]):
            #create project
            file1_CreateProject(row)
            logger.info("afegit nou projecte: %s", row[0])
        else:
            logger.debug("avoid %s -> type: %s", row[0], row[1])


def FirstFile(filename):
    "Gets the first file to read and process it"
    with open(filename, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        reader = csv.reader(f, dialect)
        try:
            for row in reader:
                ProcessRow(row)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

###########################
## second file: SocisCIC ##
###########################
# things to check in the database:
# - if the COOP number exists don't do anything
# - if the COOP doesn't exists: create user? create Person and IcMembership


def SecondFile(filename):
    with open(filename, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        reader = csv.reader(f, dialect)
        try:
            for row in reader:
                GeneralPerson()
                human = GeneralHuman()
                #print row
                #print "Num. COOP: "+row[0]
                #FIXME: waiting to adapt to the db values
                #Conditions: Actiu-> has COOP code; Baixa -> data de baixa;
                #Pendent -> quote pending
                if row[1] == "Actiu CIC":
                    row[1] = "En actiu"
                elif row[1] == "Baixa CIC":
                    row[1] = "Donat de baixa"
                #print "Estat CIC: "+row[1]
                data = row[2].split('/')
                if len(data) > 1:
                    row[2] = data[2] + "-" + data[1] + "-" + data[0]
                #print "Data Alta: "+row[2]
                #print "Nom i Cognoms: "+row[3]
                human.name = row[3]
                #print "Comarca: "+row[4]
                # codi postal fix
                if len(row[5]) < 5 and len(row[5]) > 0:
                    row[5] = "0" + row[5]
                #print "Codi Postal: "+row[5]
                #print "Ciutat: "+row[6]
                #print "Tel�fon: "+row[7]
                #print "Correu-e: "+row[8]
                human.email = row[8]
                #print "Forma de pagament: "+row[9]
                #print "Aport. EUR: "+row[10]
                #print "Aport. ECO: "+row[11]
                #print "Aport. BTC: "+row[12]
                #print "Aport. H: "+row[13]
                if human.email != "":
                    if not GeneralHuman.get(email=human.email):
                        #print "Hum� '"+human.name+"' ja existeix a la bbdd"
                        #print "Correu-e: "+human.email
                    #else:
                        human = GeneralHuman.create(name=row[3], email=row[8])
                        print "Afegit Humà '" + human.name + " a la bbdd"
                else:
                    print row[0] + " Humà sense correu, nom: " + human.name
                #human.save()

        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))


############################
## Main call of functions ##
############################

FirstFile('usersCES.csv')
#SecondFile('Socis_CIC-21_7_2014.csv')