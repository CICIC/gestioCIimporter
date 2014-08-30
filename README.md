gestioCIimporter
================

app to import some CSV files to the gestioCI database

Dependencies
------------

- peewee (creates the models.py file extracting the structure from the database)
 - [Peewee website](http://docs.peewee-orm.com/en/latest/)
Instructions
------------

to update the models file execute peewee command:

    pwiz.py -u <user> -P <password> -e mysql -t General_person,General_address,General_rel_human_addresses,Welcome_ic_person_membership -H localhost gestioCI_butterfly > models.py
 
 
