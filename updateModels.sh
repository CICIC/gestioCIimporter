#!/bin/bash
pwiz.py -u gestioCI -P gestioCI -e mysql -t General_person,General_address,General_rel_human_addresses,Welcome_ic_person_membership,Welcome_ic_project_membership -H localhost gestioCI_butterfly > models_new.py
autopep8 --experimental --max-line-length=80 models_new.py > models_new_autopep.py
mv models_new_autopep.py models_new.py
colordiff models.py models_new.py
