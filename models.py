from peewee import *

database = MySQLDatabase(
    'gestioCI_butterfly', **
    {'passwd': 'gestioCI', 'host': 'localhost', 'user': 'gestioCI'})


class UnknownField(object):
    pass


class BaseModel(Model):

    class Meta:
        database = database


class GeneralType(BaseModel):
    clas = CharField(max_length=200)
    description = TextField()
    level = IntegerField()
    lft = IntegerField()
    name = CharField(max_length=200)
    parent = ForeignKeyField(db_column='parent_id', null=True, rel_model='self')
    rght = IntegerField()
    tree = IntegerField(db_column='tree_id')

    class Meta:
        db_table = 'General_type'


class GeneralSpaceType(BaseModel):
    typ = ForeignKeyField(
        db_column='typ_id', primary_key=True, rel_model=GeneralType)

    class Meta:
        db_table = 'General_space_type'


class GeneralAddressType(BaseModel):
    space_type = ForeignKeyField(
        db_column='space_type_id', primary_key=True, rel_model=GeneralSpaceType)

    class Meta:
        db_table = 'General_address_type'


class GeneralRegionType(BaseModel):
    space_type = ForeignKeyField(
        db_column='space_type_id', primary_key=True, rel_model=GeneralSpaceType)

    class Meta:
        db_table = 'General_region_type'


class GeneralRegion(BaseModel):
    description = TextField(null=True)
    level = IntegerField()
    lft = IntegerField()
    name = CharField(max_length=100)
    parent = ForeignKeyField(db_column='parent_id', null=True, rel_model='self')
    region_type = ForeignKeyField(
        db_column='region_type_id', null=True, rel_model=GeneralRegionType)
    rght = IntegerField()
    tree = IntegerField(db_column='tree_id')

    class Meta:
        db_table = 'General_region'


class GeneralHuman(BaseModel):
    birth_date = DateField(null=True)
    death_date = DateField(null=True)
    description = TextField(null=True)
    email = CharField(max_length=100)
    name = CharField(max_length=200)
    nickname = CharField(max_length=50, default='')
    telephone_cell = CharField(max_length=20)
    telephone_land = CharField(max_length=20)
    website = CharField(max_length=100)

    class Meta:
        db_table = 'General_human'


class GeneralArtworkType(BaseModel):
    typ = ForeignKeyField(
        db_column='typ_id', primary_key=True, rel_model=GeneralType)

    class Meta:
        db_table = 'General_artwork_type'


class GeneralUnitType(BaseModel):
    artwork_type = ForeignKeyField(
        db_column='artwork_type_id', primary_key=True,
        rel_model=GeneralArtworkType)

    class Meta:
        db_table = 'General_unit_type'


class GeneralUnit(BaseModel):
    code = CharField(max_length=4)
    description = TextField(null=True)
    human = ForeignKeyField(
        db_column='human_id', null=True, rel_model=GeneralHuman)
    name = CharField(max_length=200, null=True)
    region = ForeignKeyField(
        db_column='region_id', null=True, rel_model=GeneralRegion)
    unit_type = ForeignKeyField(
        db_column='unit_type_id', null=True, rel_model=GeneralUnitType)

    class Meta:
        db_table = 'General_unit'


class GeneralAddress(BaseModel):
    address_type = ForeignKeyField(
        db_column='address_type_id', null=True, rel_model=GeneralAddressType)
    description = TextField(null=True)
    ic_larder = IntegerField()
    latitude = IntegerField(null=True)
    longitude = IntegerField(null=True)
    name = CharField(max_length=100)
    p_address = CharField(max_length=200)
    postalcode = CharField(max_length=5, null=True)
    region = ForeignKeyField(
        db_column='region_id', null=True, rel_model=GeneralRegion)
    size = DecimalField(null=True)
    size_unit = ForeignKeyField(
        db_column='size_unit_id', null=True, rel_model=GeneralUnit)
    town = CharField(max_length=150)

    class Meta:
        db_table = 'General_address'


class GeneralPerson(BaseModel):
    email2 = CharField(max_length=75, default='')
    human = PrimaryKeyField(db_column='human_id')
    id_card = CharField(max_length=9, default='')
    nickname2 = CharField(max_length=20, default='')
    surnames = CharField(max_length=100, default='')

    class Meta:
        db_table = 'General_person'


class GeneralRelation(BaseModel):
    clas = CharField(max_length=50)
    description = TextField()
    gerund = CharField(max_length=50)
    level = IntegerField()
    lft = IntegerField()
    name = CharField(max_length=100)
    parent = ForeignKeyField(db_column='parent_id', null=True, rel_model='self')
    rght = IntegerField()
    tree = IntegerField(db_column='tree_id')
    verb = CharField(max_length=50)

    class Meta:
        db_table = 'General_relation'


class GeneralRelHumanAddresses(BaseModel):
    address = ForeignKeyField(db_column='address_id', rel_model=GeneralAddress)
    human = ForeignKeyField(db_column='human_id', rel_model=GeneralHuman)
    main_address = IntegerField()
    relation = ForeignKeyField(
        db_column='relation_id', null=True, rel_model=GeneralRelation)

    class Meta:
        db_table = 'General_rel_human_addresses'


class GeneralBeingType(BaseModel):
    typ = ForeignKeyField(
        db_column='typ_id', primary_key=True, rel_model=GeneralType)

    class Meta:
        db_table = 'General_being_type'


class GeneralCompanyType(BaseModel):
    being_type = ForeignKeyField(
        db_column='being_type_id', primary_key=True, rel_model=GeneralBeingType)

    class Meta:
        db_table = 'General_company_type'


class GeneralCompany(BaseModel):
    company_type = ForeignKeyField(
        db_column='company_type_id', null=True, rel_model=GeneralCompanyType)
    human = ForeignKeyField(
        db_column='human_id', primary_key=True, rel_model=GeneralHuman)
    legal_name = CharField(max_length=200, null=True)
    vat_number = CharField(max_length=20, null=True)

    class Meta:
        db_table = 'General_company'


class GeneralProject(BaseModel):
    ecommerce = IntegerField(default=0)
    email2 = CharField(max_length=75, default='')
    human = PrimaryKeyField(db_column='human_id')
    level = IntegerField()
    lft = IntegerField()
    parent = IntegerField(db_column='parent_id', null=True)
    project_type = IntegerField(db_column='project_type_id', null=True)
    rght = IntegerField()
    socialweb = CharField(max_length=100, default='')
    tree = IntegerField(db_column='tree_id')

    class Meta:
        db_table = 'General_project'


class WelcomeIcType(BaseModel):
    clas = CharField(max_length=200)
    description = TextField()
    level = IntegerField()
    lft = IntegerField()
    name = CharField(max_length=200)
    parent = ForeignKeyField(db_column='parent_id', null=True, rel_model='self')
    rght = IntegerField()
    tree = IntegerField(db_column='tree_id')

    class Meta:
        db_table = 'Welcome_ic_type'


class WelcomeIcRecordType(BaseModel):
    ic_type = ForeignKeyField(
        db_column='ic_type_id', primary_key=True, rel_model=WelcomeIcType)

    class Meta:
        db_table = 'Welcome_ic_record_type'


class WelcomeIcRecord(BaseModel):
    description = TextField(null=True)
    name = CharField(max_length=200, null=True)
    record_type = ForeignKeyField(
        db_column='record_type_id', null=True, rel_model=WelcomeIcRecordType)

    class Meta:
        db_table = 'Welcome_ic_record'


class WelcomePaymentType(BaseModel):
    ic_type = ForeignKeyField(
        db_column='ic_type_id', primary_key=True, rel_model=WelcomeIcType)

    class Meta:
        db_table = 'Welcome_payment_type'


class GeneralRecordType(BaseModel):
    artwork_type = ForeignKeyField(
        db_column='artwork_type_id', primary_key=True,
        rel_model=GeneralArtworkType)

    class Meta:
        db_table = 'General_record_type'


class GeneralRecord(BaseModel):
    description = TextField(null=True)
    name = CharField(max_length=200, null=True)
    record_type = ForeignKeyField(
        db_column='record_type_id', null=True, rel_model=GeneralRecordType)

    class Meta:
        db_table = 'General_record'


class WelcomeFee(BaseModel):
    amount = DecimalField()
    deadline_date = DateField(null=True)
    human = ForeignKeyField(db_column='human_id', rel_model=GeneralHuman)
    ic_record = ForeignKeyField(
        db_column='ic_record_id', primary_key=True, rel_model=WelcomeIcRecord)
    issue_date = DateField(null=True)
    payment_date = DateField(null=True)
    payment_type = ForeignKeyField(
        db_column='payment_type_id', null=True, rel_model=WelcomePaymentType)
    project = ForeignKeyField(db_column='project_id', rel_model=GeneralProject)
    rel_account = ForeignKeyField(
        db_column='rel_account_id', null=True, rel_model=GeneralRecord)
    unit = ForeignKeyField(db_column='unit_id', rel_model=GeneralUnit)

    class Meta:
        db_table = 'Welcome_fee'


class WelcomeIcMembership(BaseModel):
    contribution = ForeignKeyField(
        db_column='contribution_id', null=True, rel_model=GeneralRelation)
    end_date = DateField(null=True)
    human = ForeignKeyField(db_column='human_id', rel_model=GeneralHuman)
    ic_cesnum = CharField(db_column='ic_CESnum', max_length=8, null=True)
    ic_company = ForeignKeyField(
        db_column='ic_company_id', null=True, rel_model=GeneralCompany)
    ic_project = ForeignKeyField(
        db_column='ic_project_id', rel_model=GeneralProject)
    ic_record = ForeignKeyField(
        db_column='ic_record_id', primary_key=True, rel_model=WelcomeIcRecord)
    join_date = DateField(null=True)
    join_fee = ForeignKeyField(
        db_column='join_fee_id', null=True, rel_model=WelcomeFee)
    virtual_market = IntegerField(default=0)

    class Meta:
        db_table = 'Welcome_ic_membership'


class WelcomeIcDocumentType(BaseModel):
    record_type = ForeignKeyField(
        db_column='record_type_id', primary_key=True, rel_model=WelcomeIcType)

    class Meta:
        db_table = 'Welcome_ic_document_type'


class WelcomeIcDocument(BaseModel):
    doc_file = CharField(max_length=100, null=True)
    doc_type = ForeignKeyField(
        db_column='doc_type_id', null=True, rel_model=WelcomeIcDocumentType)
    ic_record = ForeignKeyField(
        db_column='ic_record_id', primary_key=True, rel_model=WelcomeIcRecord)

    class Meta:
        db_table = 'Welcome_ic_document'


class WelcomeIcLaborContract(BaseModel):
    company = ForeignKeyField(db_column='company_id', rel_model=GeneralCompany)
    end_date = DateField(null=True)
    ic_document = ForeignKeyField(
        db_column='ic_document_id', primary_key=True,
        rel_model=WelcomeIcDocument)
    person = ForeignKeyField(db_column='person_id', rel_model=GeneralPerson)
    start_date = DateField(null=True)

    class Meta:
        db_table = 'Welcome_ic_labor_contract'


class WelcomeIcPersonMembership(BaseModel):
    ic_membership = ForeignKeyField(
        db_column='ic_membership_id', primary_key=True,
        rel_model=WelcomeIcMembership)
    labor_contract = ForeignKeyField(
        db_column='labor_contract_id', null=True,
        rel_model=WelcomeIcLaborContract)
    person = ForeignKeyField(db_column='person_id', rel_model=GeneralPerson)

    class Meta:
        db_table = 'Welcome_ic_person_membership'


class WelcomeIcProjectMembership(BaseModel):
    ic_membership = ForeignKeyField(
        db_column='ic_membership_id', primary_key=True,
        rel_model=WelcomeIcMembership)
    project = ForeignKeyField(db_column='project_id', rel_model=GeneralProject)

    class Meta:
        db_table = 'Welcome_ic_project_membership'