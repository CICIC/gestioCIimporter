from models import *

membership = WelcomeIcMembership.get(
            WelcomeIcMembership.ic_cesnum == 'COOP0874')

human = GeneralHuman.get(GeneralHuman.id == membership.human)

print "CESnumber:", membership.ic_cesnum 
print "Human name:", human.name 
print "Human email:", human.email 
print "Human nickname:", human.nickname 
print "Human telephone_cell:", human.telephone_cell 
print "Human telephone_land:", human.telephone_land 

person = GeneralPerson(GeneralPerson.human == human.id)
print "Person surnames:", person.surnames 
print "Person email2:", person.email2 
print "Person nickname2:", person.nickname2 
print "Person id_card:", person.id_card 

print "Membership join_date:",membership.join_date 
print "Membership ic_cesnum:",membership.ic_cesnum 
print "Membership ic_project:",membership.ic_project.human
print "Membership ic_record:",membership.ic_record.id

