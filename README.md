gestioCIimporter
================

app to import some CSV files to the gestioCI database

Dependencies
------------

- peewee (creates the models.py file extracting the structure from the database)
 - [Peewee website](http://docs.peewee-orm.com/en/latest/)
- To create/update models.py needs access to a copy of the gestioCI_butterfly_release database

Instructions
------------

- To execute the app just call importer.py
- To create/update the models.py execute this script: updateModels.sh
 
Documentation
-------------

### File1 specification

- row[0] = UID (COOP number)
- row[1] = User Type (adm,ind,org,cic,ex,nal,reb,pub,vir)
 - VALUES: adm, org, cic, ex, nal, reb, pub, vir
- row[2] = Firstname
- row[3] = Surnames
- row[4] = OrgName (Name of the col·lective project)
- row[5] = Address1
- row[6] = Address2
- row[7] = Address3 (Barri/Zona)
- row[8] = Postcode
- row[9] =  SubArea ( != comarca)
- row[10] = PhoneHome
- row[11] = PhoneWork
- row[12] = PhoneFax
- row[13] = PhoneMobile
- row[14] = Email
- row[15] = IM
- row[16] = WebSite
- row[17] = Created 
- row[18] = Locked

### File2 specs

"Num COOP";"Estat CIC";"Forma pagament";"Aportació  Euros";"Aportació  Ecos";"Aportació  Bitcoins";"Aportació  Hores"




