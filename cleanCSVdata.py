# coding: utf8
import re
import logging


def cleanDate(date):
    "Clean date format from yyyy[/]mm[/]dd hh:mm:ss"

    if date != '':
        date = date.split(' ')  # get yyyy/mm/dd
        date = date[0].replace('/', '-')
        try:
            date = re.match(r'[0-9]{4}-[01]?[0-9]{1}-[0-3]{1}[0-9]{1}',
                date).group(0)
        except AttributeError:
            date = ''
    return date


def cleanPhone(phone):
    "Clean phone date, only spain numbers"

    phone = phone.replace(' ', '')
    phone = phone.replace('.', '')
    phone = phone.replace('-', '')
    phone = phone.replace('+34', '')
    if re.match(r"0034", phone):
        phone = phone[4:]
    phone = phone[0:9]
    if not re.match(r"[0-9]{9}", phone) and len(phone) > 9:
        phone = ''
    return phone


def cleanPostalcode(postalcode):
    if re.search(r"^[0-9]{4}", postalcode) and len(postalcode) == 4:
        postalcode = '0' + postalcode
    if (not re.search(r"^[0-9]{5}", postalcode)) or len(postalcode) != 5:
        postalcode = ''
    return postalcode


def cleanCOOPnumber(coopnumber):
    coopnumber = coopnumber.replace(' ','')
    if re.match(r"COOP[0-9]{4}",coopnumber):
        coopnumber = coopnumber[0:8]
    else:
        coopnumber = ''
    return coopnumber


def cleanIDcard(idcard):
    idcard = idcard.replace('-','')
    idcard = idcard.replace('.','')
    idcard = idcard.replace(' ','')
    if (not re.match(r"[a-zA-Z][0-9]{8}",idcard) or
        not re.match(r"[0-9]{8}[a-zA-Z]",idcard)) and len(idcard) != 9:
        idcard = ''
    return idcard

def cleanFloat(num):
    "Convert swap '.' and ',' (ES format to US)"

    num = num.replace(',','dot')
    num = num.replace('.',',')
    num = num.replace('dot','.')
    if num == '':
        num = 0
    try:
        num = float(num)
    except ValueError:
        print "Not a float: " + num
        num = 0.0
    return num


def cleanInteger(num):
    "In this case only remove the value if it's not an integer"
    
    if num == '':
        num = 0
    try:
        num = int(num)
    except ValueError:
        print "Not an integer: " + num
        num=0
    return num
    

def cleanCooperative(coop):
    if coop == 'x':
        coop = 'X'
    if coop == 'i':
        coop = 'I'
    if coop != 'X' or coop != 'I':
        coop = ''
    return coop


def cleanEmail(email):
    "Return a valid email"

    em = re.search("(<)?([\w\-_.]+@[\w\-_.]+(?:\.\w+)+)(?(1)>)", email)
    if em:
        email = em.group(0)
    else:
        email = ''
    return email
