# coding: utf8
import csv
import sys
import re
import logging

from peewee import DoesNotExist

from models import WelcomeIcMembership, WelcomeIcRecord
from models import WelcomeIcPersonMembership
from models import GeneralHuman, GeneralPerson, GeneralRelHumanAddresses
from models import GeneralAddress

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
ch.setLevel(logging.DEBUG)
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
cicProject = 3
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
#row[1] = User Type (adm,com,fam,ind,org,pub,vir)
 #adm:admin(avoid), com:company, fam:shared, ind:individual,
 #org:organitzation, pub:public, vir:virtual(avoid)
#row[2] = Firstname
#row[3] = Surname
#row[4] = OrgName (Name of the col·lective project)
#row[5] = Address1
#row[6] = Address2
#row[7] = Address3 (Barri/Zona)
#row[8] = Postcode
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


def ProcessRow(row):
    "Gets a row from the CSV and stores it's data to the database"
    existeix = True
    try:
        membership = WelcomeIcMembership.get(
            WelcomeIcMembership.ic_cesnum == row[0])
    except DoesNotExist as e:
        existeix = False
    if existeix:
        try:
            personmembership = WelcomeIcPersonMembership.get(
                WelcomeIcPersonMembership.ic_membership == membership)
            GeneralPerson.get(
                GeneralPerson.human == personmembership.person.human)
            human = GeneralHuman.get(
                GeneralHuman.id == personmembership.person.human)
        except DoesNotExist as e:
            logger.warning("BBDD inconsistent per: %s", row[0])
            logger.warning("e: %s", e)
    else:
        #being doesn't exists, then needs to be created
        #enhanced getting telephone numbers
        #row[10] = PhoneHome
        #row[11] = PhoneWork
        #row[12] = PhoneFax
        #row[13] = PhoneMobile
        phone = row[10]
        if row[10] == '':
            if row[11] != '':
                phone = row[11]
                logger.debug("phoneHome empty but phoneWork filled")
            elif row[12] != '':
                phone = row[12]
                logger.debug("phoneHome, phoneWork empty, FAX filled")
        #enhanced getting website url
        #row[15] = IM
         #(if beggins with 'http' or 'www' copy to website if empty)
        #row[16] = WebSite
        if row[16] == '':
            if row[15].startswith('www') or row[15].startswith('http'):
                row[16] = row[15]
        #create instances of the being to be stored on the db
        #create human
        human = GeneralHuman.create(
            name=row[2], email=row[14],
            telephone_cell=row[13], telephone_land=phone,
            website=row[16])
        #create person
        GeneralPerson.create(human=human.id, surnames=row[3])
        #get only well formed postal codes
        cp = row[8]
        if re.search(r"[0-9]{4}", cp):
            cp = "0" + cp
        if not re.search(r"[0-9]{5}", cp):
            cp = ""
        #create address
        address = GeneralAddress.create(name='CES', p_address=row[5],
            ic_larder=0, postalcode=cp, town=row[6])
        #create relation between person and address
        GeneralRelHumanAddresses.create(
            address=address, human=human.id, main_address=0)
        #TODO: create join_fee on the second file
         #here we don't have enogh info
        #create the membership
        #find what kind of membership
        #row[1] = User Type (adm,com,fam,ind,org,pub,vir)
        record_type = SociCoopInd
        record_name = "Alta Soci Individual:" + row[0]
        if row[1] != 'ind':
            if row[1] == 'com' or row[1] == 'org':
                record_type = SociCoopCol
                record_name = "Alta Soci Col·lectiu:" + row[0]
            elif row[1] == 'pub':
                record_type = ProjPublic
                record_name = "Alta Projecte Públic:" + row[0]
        #create record of the membership
        record = WelcomeIcRecord.create(name=record_name,
            record_type=record_type)
        logger.debug("Inserting membership: %s", row[0])
        logger.debug("ic_project= %d", cicProject)
        logger.debug("ic_record= %d", record.id)
        logger.debug("join_date= %s", row[17])
        membership = WelcomeIcMembership.create(human=human.id,
                ic_project=cicProject, ic_record=record.id,
                join_date=row[17], ic_cesnum=row[0])
        logger.debug("ic_record.id: %d", membership.ic_record.id)
        logger.debug("human.id: %d", human.id)
        #create the relation between person and membership
        personmembership = WelcomeIcPersonMembership.create(
            ic_membership=membership.ic_record.id, person=human.id)
        logger.info("afegit nou soci: %s", row[0])


def FirstFile(filename):
    "Gets the first file to read and process it"
    with open(filename, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        reader = csv.reader(f, dialect)
        try:
            for row in reader:
                #row[0] = UID (COOP number)
                logger.info("Soci: %s", row[0])
                if row[1] == 'ind':
                    #logger.info("Create a Soci ind")
                    ProcessRow(row)
                elif row[1] == 'com' or row[1] == 'org':
                    #logger.info("Create a Soci col")
                    ProcessRow(row)
                elif row[1] == 'pub':
                    #logger.info("Create a Proj Pub")
                    ProcessRow(row)
                else:
                    logger.info("avoid membership type: %s", row[1])
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

FirstFile('usersCES.csv')


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
                #TODO fix: waiting to adapt to the db values
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

#SecondFile('Socis_CIC-21_7_2014.csv')