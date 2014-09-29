#  coding: utf8

from models import *
from peewee import DoesNotExist, IntegrityError

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


def loadGeneralCompanyName(name):
    "Load Company row"

    try:
        uid = GeneralCompany.get(legal_name=name)
        return uid.human
    except DoesNotExist:
        log0.error("The database is not properly populated with %s", name)
        exit()

######################
## Load Global vars ##
######################

# membership type
SociCoopInd = loadWelcomeType("iC_Person_Membership")
SociCoopCol = loadWelcomeType("iC_Project_Membership")
ProjPublic = loadWelcomeTypeName("alta Proj. Públic")
SociAutoOcupat = loadWelcomeType("iC_Self_Employed")
SociFiraire = loadWelcomeType("iC_Stallholder")
SociAfi = loadWelcomeType("iC_Akin_Membership")

# cooperative companies
typeCoopCompany = loadGeneralTypeName("Cooperativa")

# project ID
cicProjectID = 3  # projecte: CIC

# project type
generalProject_type = loadGeneralType('ic_project')
collectiveProject_type = loadGeneralTypeName("Cooperatiu Col·lectiu")
ecoxarxaProject_type = loadGeneralTypeName("Ecoxarxa")
larderProject_type = loadGeneralType("ic_larder")
commonProject_type = loadGeneralTypeName("Servei Comú")
nalProject_type = loadGeneralTypeName("Nucli d'Autogestió Local")
ciProject_type = loadGeneralTypeName("Cooperativa Integral")

# relation type
rel_persRef = loadGeneralRelation("reference")

# bank account record type
recBankAccount = loadGeneralType("AccountBank")

# unit
unitEUR = loadGeneralUnitName("Euro")
unitECO = loadGeneralUnitName("EcoCoop")
unitHora = loadGeneralUnitName("Hora")

# paymentType
paymentFlow = loadWelcomeTypeName("pagament en Metàl·lic")

# Fees
advancedFee = loadWelcomeType("(45_eco) advanced_fee")
QuotaAltaInd = loadWelcomeType("(30_euro) individual")
QuotaAltaCol = loadWelcomeType("(60_euro) collective")

# insurance record type
typeInsurance = loadWelcomeType("iC_Insurance")
typeInsuranceCompany = loadGeneralTypeName('Asseguradora')

# get bank company
bankCompany = loadGeneralCompanyName('Triodos')

