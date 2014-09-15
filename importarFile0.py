#  coding: utf8
import csv
import sys
import re
import logging
import pdb

from peewee import DoesNotExist, IntegrityError
from cleanCSVdata import *
from models import WelcomeIcMembership, WelcomeIcRecord
from models import WelcomeIcPersonMembership, WelcomeIcProjectMembership
from models import GeneralHuman, GeneralPerson, GeneralRelHumanAddresses
from models import GeneralAddress, GeneralProject, OldAuthUser, AuthUser
from models import InvoicesSoci, GeneralRelHumanPersons, WelcomeIcSelfEmployed
from models import PublicFormRegistrationprofile, GeneralRecord, GeneralType
from models import GeneralAccountbank, WelcomeIcType, GeneralUnit
from models import GeneralRelation, WelcomeFee, WelcomeIcSelfEmployedRelFees
from models import WelcomeIcStallholder, InvoicesSalesMovement


###################
## logger config ##
###################

# create loggers
log0 = logging.getLogger('File0')
log0.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh0 = logging.FileHandler('bitacora-file0.log')
fh0.setLevel(logging.INFO)
# create console handler with a higher log level
ch0 = logging.StreamHandler()
ch0.setLevel(logging.WARNING)
# create formatter and add it to the handlers
#format0 = logging.Formatter('%(name)s: %(levelname)s: %(message)s')
format0 = logging.Formatter('%(levelname)s: %(message)s')
fh0.setFormatter(format0)
ch0.setFormatter(format0)
# add the handlers to the logger
log0.addHandler(fh0)
log0.addHandler(ch0)


######################
## Load Global vars ##
######################
def loadGeneralUnitName(name):
    "Load generalUnit values"

    try:
        uid = GeneralUnit.get(name=name)
        return uid
    except DoesNotExist:
        log0.error("The database is not properly populated with %s", name)
        exit()


def loadGeneralType(clas):
    "Load GeneralTypes values"

    try:
        uid = GeneralType.get(clas=clas)
        return uid.id
    except DoesNotExist:
        log0.error("Database not properly populated with %s", clas)
        exit()


def loadGeneralTypeName(name):
    "Load GeneralTypes values"

    try:
        uid = GeneralType.get(name=name)
        return uid.id
    except DoesNotExist:
        log0.error("Database not properly populated with %s", name)
        exit()


def loadGeneralRelation(clas):
    "Load GeneralRelation values"

    try:
        uid = GeneralRelation.get(clas=clas)
        return uid.id
    except DoesNotExist:
        log0.error("Database not properly populated with %s", clas)
        exit()


def loadWelcomeType(clas):
    "Load WelcomeTypes values"
    
    try:
        uid = WelcomeIcType.get(clas=clas)
        return uid.id
    except DoesNotExist:
        log0.error("Database not properly populated with %s", clas)
        exit()


def loadWelcomeTypeName(name):
    "Load WelcomeTypes values"
    
    try:
        uid = WelcomeIcType.get(name=name)
        return uid.id
    except DoesNotExist:
        log0.error("Database not properly populated with %s", name)
        exit()


# membership type
SociCoopInd = loadWelcomeType("iC_Person_Membership")
SociCoopCol = loadWelcomeType("iC_Project_Membership")
ProjPublic = loadWelcomeTypeName("alta Proj. Públic")
SociAutoOcupat = loadWelcomeType("iC_Self_Employed")
SociFiraire = loadWelcomeType("iC_Stallholder")

# project ID
cicProjectID = 3  # projecte: CIC

# project type
collectiveProject_type = loadGeneralTypeName("Cooperatiu Col·lectiu")
ecoxarxa_type = loadGeneralTypeName("Ecoxarxa")


# relation type
rel_persRef = loadGeneralRelation("reference")

#bank account record type
recBankAccount = loadGeneralType("AccountBank")

#unit
unitEUR = loadGeneralUnitName("Euro")
unitECO = loadGeneralUnitName("EcoCoop")
unitHora = loadGeneralUnitName("Hora")

#paymentType
paymentFlow = loadWelcomeTypeName("pagament en Metàl·lic")

#Fees
advancedFee = loadWelcomeType("advanced_fee")

#try to keep the original row each loop
originalrow = []
############################################
## Zerofile: UsersOld database and Transv ##
############################################


def file0_cleanRowProcess(row):
    "Clean the data from the CSV"

    row[0] = cleanDate(row[0])
    row[1] = cleanDate(row[1])
    row[3] = cleanCOOPnumber(row[3])
    row[4] = cleanCooperative(row[4])
    row[5] = cleanEmail(row[5])
    row[6] = cleanPhone(row[6])
    row[8] = cleanPostalcode(row[8])
    row[13] = cleanIDcard(row[13])
    # assegurança
    row[20] = cleanDate(row[20])
    row[22] = cleanFloat(row[22])
    row[31] = cleanPostalcode(row[31])
    # IAE numbers
    row[38] = cleanInteger(row[38])
    row[42] = cleanInteger(row[42])
    row[46] = cleanInteger(row[46])
    row[50] = cleanInteger(row[50])
    row[54] = cleanInteger(row[54])
    row[58] = cleanInteger(row[58])
    row[62] = cleanInteger(row[62])
    row[66] = cleanInteger(row[66])
    row[70] = cleanInteger(row[70])
    # iva trim
    row[78] = cleanFloat(row[78])
    row[79] = cleanFloat(row[79])
    row[80] = cleanFloat(row[80])
    row[92] = cleanFloat(row[92])
    row[93] = cleanFloat(row[93])
    row[94] = cleanFloat(row[94])
    row[106] = cleanFloat(row[106])
    row[107] = cleanFloat(row[107])
    row[108] = cleanFloat(row[108])
    row[120] = cleanFloat(row[120])
    row[121] = cleanFloat(row[121])
    row[122] = cleanFloat(row[122])
    # date ing trim iva
    row[84] = cleanDate(row[84])
    row[98] = cleanDate(row[98])
    row[112] = cleanDate(row[112])
    row[126] = cleanDate(row[126])
    # quot trim
    row[141] = cleanFloat(row[141])
    row[142] = cleanFloat(row[142])
    row[156] = cleanFloat(row[156])
    row[157] = cleanFloat(row[157])
    row[171] = cleanFloat(row[171])
    row[172] = cleanFloat(row[172])
    row[186] = cleanFloat(row[186])
    row[187] = cleanFloat(row[187])
    # date ing trim quot
    row[146] = cleanDate(row[146])
    row[161] = cleanDate(row[161])
    row[176] = cleanDate(row[176])
    row[191] = cleanDate(row[191])
    

def file0_CreateUser(row):
    "Create a django user"

    newuser = None
    # default values
    password = u"pbkdf2_sha256$12000$k93h7VmpEGlY$EirohX1jqCOY3W5KOS9De8UWEizyW9cJ+fLh5bGxGKU="
    last_login, date_joined = "2014-09-11", "2014-09-11"
    is_superuser, is_staff, is_active = 0, 0, 1
    
    # first check into the old_auth_user table
    try:
        # get all the data from olduser
        oldusername = row[3].replace("COOP",'')
        ou = OldAuthUser.get(username = oldusername)
        password = ou.password
        last_login, date_joined = ou.last_login, ou.date_joined
        is_superuser, is_staff = ou.is_superuser, ou.is_staff
        is_active = ou.is_active
        username = "COOP" + ou.username
        first_name, last_name = ou.first_name, ou.last_name
        email = ou.email
    except DoesNotExist:
        # get all data from transversal, can happen? who knows!
        username = row[3]
        first_name = row[11]
        last_name = row[12]
        email = row[5]
    if username == '' and email != '':
        log0.warning("Sense COOP, creant usuari amb l'email")
        username = row[5]
    if username != '':
        newuser = AuthUser.create(date_joined = date_joined, email = email,
            first_name = first_name, is_active = is_active,
            is_staff = is_staff, is_superuser = is_superuser,
            last_login = last_login, last_name = last_name,
            password = password, username = username)
    else:
        log0.Error("Nou usuari %s no creat, no COOP nor email")
    return newuser


def file0_CreateHuman(row, user):
    "Create a human registry"
    
    email = user.email
    name = user.first_name
    telephone_cell = ''
    telephone_land = ''
    if re.match(r"6",row[6]):
        telephone_cell = row[6]
    else:
        telephone_land = row[6]
    return GeneralHuman.create(name=name, email=email,
        telephone_cell=telephone_cell, telephone_land=telephone_land,
        description=row[15])


def file0_CreateAddress(row, humanID):
    "Process the CSV data related to Address class and saves to the database"

    # create address
    address = GeneralAddress.create(name='Adreça principal', p_address=row[7],
        ic_larder=0, postalcode=row[8], town=row[9])
    # create relation between person and address
    GeneralRelHumanAddresses.create(
        address=address.id, human=humanID, main_address=1)


def file0_CreatePerson(row, user):
    "create a person registry"
    
    human = file0_CreateHuman(row, user)
    # create person
    GeneralPerson.create(human=human.id, surnames=row[12],
        id_card=row[13])
    return human


def file0_CreateProject(row, user):
    "create a project registry"
    human = file0_CreateHuman(row,user)
    if row[16] != '':
        human.name = row[16]
        human.save()
    projType = collectiveProject_type
    if row[14] == "Ecoxarxa":
        projType = ecoxarxa_type
    GeneralProject.create(human=human.id, project_type=projType,
        parent=cicProjectID)
    return human


def file0_isStallholder(row):
    "Try to find if is stallholder"
    
    if re.search('Fira', row[37], re.IGNORECASE):
        return True
    if re.search('Fires', row[37], re.IGNORECASE):
        return True
    if re.search('Fira', row[41], re.IGNORECASE):
        return True
    if re.search('Fires', row[41], re.IGNORECASE):
        return True
    if re.search('Fira', row[45], re.IGNORECASE):
        return True
    if re.search('Fires', row[45], re.IGNORECASE):
        return True
    if re.search('Fira', row[49], re.IGNORECASE):
        return True
    if re.search('Fires', row[49], re.IGNORECASE):
        return True
    if re.search('Fira', row[53], re.IGNORECASE):
        return True
    if re.search('Fires', row[53], re.IGNORECASE):
        return True
    if re.search('Fira', row[57], re.IGNORECASE):
        return True
    if re.search('Fires', row[57], re.IGNORECASE):
        return True
    if re.search('Fira', row[61], re.IGNORECASE):
        return True
    if re.search('Fires', row[65], re.IGNORECASE):
        return True
    if re.search('Fira', row[69], re.IGNORECASE):
        return True
    return False

def file0_addFeeMovements(row, selfemployed):
    "function to store the fee movements"
    
    trimestre = ['1r','2n','3r','4t']
    pointer = [141,156,171,186]
    member = selfemployed.ic_record
    # who manage de sale movement
    manage_gestioEco = 1 # ECOs managed by gestioEco
    manage_members = 0 #EURs managed by members
    for quarter in trimestre:
        i = 0
        concept = "Quota " + quarter + " trimestre. " + row[pointer[i]+6]
        execution_date = row[pointer[i]+5]
        valueEUR = row[pointer[i]]
        valueECO = row[pointer[i]+1]
        if valueEUR != 0.0 and valueEUR != None and valueEUR != 0:
            if execution_date != None and execution_date != '':
                InvoicesSalesMovement.create(
                    ic_membership=selfemployed.ic_membership.ic_record.id,
                    concept=concept, execution_date=execution_date,
                    value=valueEUR, currency=unitEUR, planned_date=execution_date,
                    who_manage=manage_members)
            else:
                log0.warning("Falta data de pagament de:")
                log0.warning("%s: %s\n%s - EUR:%s", row[3], concept,
                    execution_date, valueEUR)
        if valueECO != 0.0 and valueECO != None and valueECO != 0:
            if execution_date != None and execution_date != '':
                InvoicesSalesMovement.create(
                    ic_membership=selfemployed.ic_membership.ic_record.id,
                    concept=concept, execution_date=execution_date,
                    value=valueEUR, currency=unitECO, planned_date=execution_date,
                    who_manage=manage_gestioEco)
            else:
                log0.warning("Falta data de pagament de:")
                log0.warning("%s: %s\n%s - ECO:%s", row[3], concept,
                    execution_date, valueECO)


def file0_addTaxMovements(row, selfemployed):
    "function to store the tax movements"

    return None


def file0_CreateSelfEmployed(row, membership):
    "Store selfemployed data"
    
    # diferentiate between stallholder and the others
    recordName = ''
    recType = ''
    if file0_isStallholder(row):
        recordName = 'Soci Firaire' + row[3]
        recType = SociFiraire
    else:
        recordName = 'Soci Autoocupat' + row[3]
        recType = SociAutoOcupat  
    # crear record
    record = WelcomeIcRecord.create(name=recordName, record_type=recType)
    #mirar dades Invoices_soci
    soci = None
    fee = None
    IVAassignat = 18
    extraD = 0
    preTAX = 0
    coopID = 1
    bankAccount = None
    tarjeta = 0
    try:
        soci = InvoicesSoci.get(
            InvoicesSoci.coop_number == row[3].replace('COOP',''))
        IVAassignat = soci.iva_assignat
        extraD = soci.extra_days
        # Add advanced fee
        if soci.pretax != 0:
            #create record fee
            recFee = WelcomeIcRecord.create(name='Quota Avançada',
                description='Pagament de la quota avançada',
                record_type=advancedFee)
            #create fee
            fee = WelcomeFee.create(amount=soci.pretax,
                deadline_date=row[0], human=membership.human.id,
                ic_record=recFee, issue_date=row[0], payment_date=row[0],
                payment_type=paymentFlow, project=cicProjectID,
                unit=unitEUR)
    except DoesNotExist:
        pass
    #bank account data
    recBank = None
    if row[25] == 'Sí':
        # create record
        recBank = GeneralRecord.create(name='Apoderat Triodos',
            description=row[27],
            record_type=recBankAccount)
        # record type=18
        if row[26] == 'Sí':
            tarjeta=1

        bankAccount = GeneralAccountbank.create(record=recBank,
            human=membership.human.id, unit=unitEUR, bankcard=tarjeta)
    # has end date: status baixa
    # TODO: waiting status to do something more
    end_date = row[1]
    if end_date == '':
        end_date = None
    comment = 'Comentaris Històric\n'
    comment += '-------------------\n'
    comment += row[17] + '\n'
    comment += 'Comentaris IVA assignat\n'
    comment += '-----------------------\n'
    comment += row[18] + '\n'
    selfe = WelcomeIcSelfEmployed.create(ic_record=record.id,
        ic_membership=membership.ic_record.id, join_date=row[0],
        end_date=end_date, organic=0, rel_accountBank=bankAccount,
        assigned_vat=IVAassignat, mentor_comment=row[18], extra_days=extraD)
    #if stallholder
    WelcomeIcStallholder.create(
        ic_self_employed=selfe.ic_record, tent_type=None)
    # if pretax != 0 link the created fee with the membership
    if soci != None and fee != None and soci.pretax != 0:
        WelcomeIcSelfEmployedRelFees.create(
        ic_self_employed=selfe.ic_record, fee=fee.ic_record)
    
    # Quotes Trim
    file0_addFeeMovements(row,selfe)
    # TODO: IVAS Trim
    file0_addTaxMovements(row,selfe)
    # TODO: waiting the Legal Cooperative field
    # TODO: waiting IAEs table


def file0_CreateMembership(row, user):
    "Create the data structure to store a new member"
    #beingID tuple with the 0:personID, 1:projectID
    beingID = None, None

    recType = None
    if re.search(r'Individual', row[14], re.IGNORECASE):
        # create indiv membership record
        record = WelcomeIcRecord.create(
            name="Soci Coop. Individual:"+row[3],
            record_type=SociCoopInd)
        recType = SociCoopInd
        # create person
        human = file0_CreatePerson(row, user)
        # add address
        file0_CreateAddress(row, human.id)
        # create membership
        membership = WelcomeIcMembership.create(human=human.id,
            ic_project=cicProjectID, ic_record=record.id,
            join_date=row[0], ic_cesnum=row[3])
        # link person to membership
        WelcomeIcPersonMembership.create(ic_membership=record.id,
            person=human.id)
        # create self_employed membership
        file0_CreateSelfEmployed(row, membership)
        # value to return
        beingID = human.id, None
    elif re.search(r'Col·lectiu', row[14], re.IGNORECASE)\
        or re.search(r'Ecoxarxa', row[14], re.IGNORECASE)\
        or re.search(r'projecte productiu public',
            row[14], re.IGNORECASE):
        record = None
        if re.search(r'Col·lectiu', row[14], re.IGNORECASE):
            # create membership record
            record = WelcomeIcRecord.create(
                name="Soci Proj. Col·lectiu:" + row[3],
                record_type=SociCoopCol)
            recType = SociCoopCol 
        else:
            record = WelcomeIcRecord.create(
                name="Soci Proj. Públic:" + row[3],
                record_type=ProjPublic)
            recType = ProjPublic
        # create project
        human = file0_CreateProject(row,user)
        # add address
        file0_CreateAddress(row, human.id)
        # create reference person
        refPers = file0_CreatePerson(row,user)
        # link ref pers to project
        GeneralRelHumanPersons.create(human=human.id,
            person=refPers.id, relation=rel_persRef)
        # create membership
        membership = WelcomeIcMembership.create(human=human.id,
            ic_project=cicProjectID, ic_record=record.id,
            join_date=row[0], end_date=row[1], ic_cesnum=row[3])
        # link project to membership
        WelcomeIcProjectMembership.create(
            ic_membership=membership.ic_record.id, project=human.id)
        # create self_employed membership
        file0_CreateSelfEmployed(row, membership)
        # values to return
        beingID = refPers.id, human.id
    else:
        log0.warning('Projecte %s, email:%s, Tipus desconegut (Ind/Col...): %s', row[3],
            row[5], row[14].decode('ascii', 'ignore'))
        log0.warning("name: %s surnames: %s", row[11], row[12])
    return beingID, recType
    

def file0_NewUser(row):
    user = file0_CreateUser(row)
    activation_key = "ALREADY_ACTIVATED"
    beingID, recType = file0_CreateMembership(row, user)
    if recType:
        try:
            PublicFormRegistrationprofile.create(
            activation_key=activation_key, person=beingID[0],
            project=beingID[1], record_type=recType, user=user.id)
        except IntegrityError as e:
            log0.warning('exists user %s in the public_form', row[3])
            log0.warning(e)


def file0_ProcessRow(row):
    "Gets a row from the CSV and stores it's data to the database"
    user = None
    if row[3] != None and row[3] != '':
        #soci has coop
        try:
            user = AuthUser.get(AuthUser.username == row[3])
        except DoesNotExist:
            if row[5] != None and row[5] != '':
                try:
                    user = AuthUser.get(AuthUser.email == row[5])
                    if user.username != row[3]:
                        #create igual
                        file0_NewUser(row)
                    else:
                        log0.warning("Ja hi ha un  usuari amb email:%s",row[5])
                        log0.warning("diferents usuaris, mateix email?")
 
                except DoesNotExist:
                    file0_NewUser(row)
    else:
        if row[5] == None or row[5] == '':
            log0.warning("Sense COOP ni email, nom: %s",
                (row[11] + ' ' + row[12]).decode('ascii','ignore'))
        else:
            log0.warning("És un 'Pendent'? %s",row[5])
            # TODO: afegir alguna cosa?

def ZeroFile(filename):
    "Gets the before the first file to read and process it"
    
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        try:
            contador = 1
            for row in reader:
                originalrow = list(row)
                log0.info('row: %d', contador)
                file0_cleanRowProcess(row)
                file0_ProcessRow(row)
                contador += 1
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

