#  coding: utf8
import logging
import csv
import pdb

from peewee import DoesNotExist, IntegrityError
from cleanCSVdata import *
from models import *
from globalVars import *

###################
## logger config ##
###################

# create loggers
log1 = logging.getLogger('File1')
log1.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh1 = logging.FileHandler('bitacora-file1.log')
fh1.setLevel(logging.INFO)
# create console handler with a higher log level
ch1 = logging.StreamHandler()
ch1.setLevel(logging.WARNING)
# create formatter and add it to the handlers
#format0 = logging.Formatter('%(name)s: %(levelname)s: %(message)s')
format1 = logging.Formatter('%(levelname)s: %(message)s')
fh1.setFormatter(format1)
ch1.setFormatter(format1)
# add the handlers to the logger
log1.addHandler(fh1)
log1.addHandler(ch1)


############################################
## Zerofile: UsersOld database and Transv ##
############################################

def file1_cleanRowProcess(row):
    "Clean the data from the CSV"

    # saving telephone numbers enhanced
    # row[10] = PhoneHome
    # row[11] = PhoneWork
    # row[12] = PhoneFax
    # row[13] = PhoneMobile
    row[10] = cleanPhone(row[10])
    row[11] = cleanPhone(row[11])
    row[12] = cleanPhone(row[12])
    row[13] = cleanPhone(row[13])

    phone = row[10]
    cellphone = row[13]

    if re.match(r"6", phone) and not cellphone:
        cellphone = phone
        phone = None
    if not phone:
        if row[11]:
            phone = row[11]
        elif row[12]:
            phone = row[12]

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
    row[8] = cleanPostalcode(row[8])
    # fix data format
    row[17] = minicleanDate(row[17])
    #clean e-mail
    row[14] = cleanEmail(row[14])


def file1_CreateHuman(row):
    "Create a human registry"

    if not row[10]: row[10]=''
    return GeneralHuman.create(name=row[2], email=row[14], telephone_cell=row[13],
        telephone_land=row[10])


def file1_CreateAddress(row, humanID):
    "Process the CSV data related to Address class and saves to the database"

    # try to match a 'comarca' in the database
    comarca = None
    if row[9]:
        try:
            comarca = GeneralRegion.get(name=row[9])
        except DoesNotExist:
            pass
    # create address
    address = GeneralAddress.create(name='Adreça del CES', p_address=row[5],
        ic_larder=0, postalcode=row[8], town=row[6], region=comarca)
    # create relation between person and address
    GeneralRelHumanAddresses.create(
        address=address.id, human=humanID, main_address=1)


def file1_CreatePerson(row):
    "create a person registry"

    human = file1_CreateHuman(row)
    # create person
    GeneralPerson.create(human=human.id, surnames=row[12],
        id_card=row[13])
    return human


def file1_isCollectiveProject(pt):
    "Guess if the project is collective"

    return pt == 'org' or pt == 'cic' or pt == 'ex' or pt == 'nal'\
        or pt == 'reb' or pt == 'pub'


def file1_CreateProject(row, projType):
    "Process the data related to Project Membership and saves to the database"
    # create human
    human = file1_CreateHuman(row)
    # create project
    GeneralProject.create(human=human.id, project_type=projType,
        parent=cicProjectID)
    return human


def file1_CreateMembership(row,user):
    "Save data of a new member"

    if row[1] == 'ind':
        # create person
        person = file1_CreatePerson(row)
        # add address
        file1_CreateAddress(row, person.id)
        # membership record name
        recordName = "Soci Coop. Individual:" + row[0]
        recType = SociCoopInd
        # create membership record
        record = WelcomeIcRecord.create(name=recordName, record_type=recType)
        # create membership
        membership = WelcomeIcMembership.create(human=person.id,
        ic_project=cicProjectID, ic_record=record.id, join_date=row[17],
        ic_cesnum=row[0])
        # link person to membership
        WelcomeIcPersonMembership.create(ic_membership=record.id,
            person=person.id)
        try:
            PublicFormRegistrationprofile.create(activation_key="ALREADY_ACTIVATED",
                person=person, project=None, record_type=recType, user=user.id)
        except IntegrityError as e:
            log1.warning('exists user %s in the public_form', row[3])
            log1.warning(e)
    elif file1_isCollectiveProject(row[1]):
        # define membership type

        if row[1] == 'org':
            projType = collectiveProject_type
            recType = SociCoopCol
            recordName = "Alta Soci Col·lectiu:" + row[0]
        elif row[1] == 'cic':
            projType = cicProject_type
            recType = ProjPublic
            recordName = "Alta Cooperativa Integral:" + row[0]
        elif row[1] == 'ex':
            projType = ecoxarxaProject_type
            recType = ProjPublic
            recordName = "Alta Ecoxarxa:" + row[0]
        elif row[1] == 'nal':
            projType = nalProject_type
            recType = ProjPublic
            recordName = "Alta Nucli d'Autogestió Local:" + row[0]
        elif row[1] == 'reb':
            projType = larderProject_type
            recType = ProjPublic
            recordName = "Alta Rebost:" + row[0]
        elif row[1] == 'pub':
            projType = commonProject_type
            recType = ProjPublic
            recordName = "Alta Projecte Públic:" + row[0]
        # create project
        project = file1_CreateProject(row, projType)
        # add address
        file1_CreateAddress(row, project.id)
        # add ref person
        person  = file1_CreatePerson(row)
        # link ref pers to project
        GeneralRelHumanPersons.create(human=project.id, person=person.id,
             relation=rel_persRef)
        # create membership record
        record = WelcomeIcRecord.create(name=recordName, record_type=recType)
        # create membership
        membership = WelcomeIcMembership.create(human=project.id,
            ic_project=cicProjectID, ic_record=record.id, join_date=row[17],
            ic_cesnum=row[0])
        WelcomeIcProjectMembership.create(ic_membership=membership.ic_record.id,
            project=project.id)
        try:
            PublicFormRegistrationprofile.create(activation_key="ALREADY_ACTIVATED",
                person=person, project=project, record_type=recType, user=user.id)
        except IntegrityError as e:
            log1.warning('exists user %s in the public_form', row[3])
            log1.warning(e)
    else:
        log1.debug("avoid %s -> type: %s", row[0], row[1])


def file1_CreateUser(row):
    "Create a django user"

    # default values
    password = u"pbkdf2_sha256$12000$k93h7VmpEGlY$EirohX1jqCOY3W5KOS9De8UWEizyW9cJ+fLh5bGxGKU="
    last_login, date_joined = row[17], row[17]
    username = row[0]
    first_name = row[2]
    last_name = row[3]
    email = row[14]
    newuser = AuthUser.create(date_joined=date_joined, email=email, is_active=1,
        first_name=first_name, username=username, is_staff=0, is_superuser=0,
        last_login=last_login, last_name=last_name, password=password)
    return newuser

def file1_UpdateMembership(row,memb,user):
    "Update the data from an existing user"

    # update human
    if not memb.human.telephone_cell and row[13]:
        memb.human.telephone_cell = row[13]
    if not memb.human.telephone_land and row[14]:
        memb.human.telephone_land = row[14]
    if not memb.human.website and row[16]:
        memb.human.website = row[16]
    memb.human.save()


def file1_ProcessRow(row):
    "Gets a row from the CSV and stores it's data to the database"
    
    #find if exists a username with the coopnumber
    try:
        user = AuthUser.get(AuthUser.username == row[0])
        try:
            memb = WelcomeIcMembership.get(
                WelcomeIcMembership.ic_cesnum == row[0])
            # update membership
            file1_UpdateMembership(row,memb,user)
        except DoesNotExist:
            #create membership
            file1_CreateMembership(row, user)
    except DoesNotExist:
        try:
            # visibilitzar els correus repetits
            user = AuthUser.get(AuthUser.email == row[14])
            log1.info("%s i %s tenen el mateix correu-e: %s", row[0],
                user.username, row[14])
        except DoesNotExist:
            pass
        # create from scratch
        user = file1_CreateUser(row)
        file1_CreateMembership(row, user)
               

def FirstFile(filename):
    "Gets the before the first file to read and process it"
    
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        try:
            contador = 1
            for row in reader:
                log1.info('row: %d', contador)
                file1_cleanRowProcess(row)
                if row[18] == '0':
                    file1_ProcessRow(row)
                else:
                    log1.info("usuari donat de baixa: %s",row[0])
                contador += 1
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
