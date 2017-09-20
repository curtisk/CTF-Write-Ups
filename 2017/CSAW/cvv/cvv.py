#!/usr/bin/python
from random import Random
from pwn import *
import copy
import os

ccarray = []

visaPrefixList = [
        ['4', '5', '3', '9'],
        ['4', '5', '5', '6'],
        ['4', '9', '1', '6'],
        ['4', '5', '3', '2'],
        ['4', '9', '2', '9'],
        ['4', '0', '2', '4', '0', '0', '7', '1'],
        ['4', '4', '8', '6'],
        ['4', '7', '1', '6'],
        ['4']]

mastercardPrefixList = [
        ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']]

amexPrefixList = [['3', '4'], ['3', '7']]

discoverPrefixList = [['6', '0', '1', '1']]

dinersPrefixList = [
        ['3', '0', '0'],
        ['3', '0', '1'],
        ['3', '0', '2'],
        ['3', '0', '3'],
        ['3', '6'],
        ['3', '8']]

enRoutePrefixList = [['2', '0', '1', '4'], ['2', '1', '4', '9']]

jcbPrefixList = [['3', '5']]

voyagerPrefixList = [['8', '6', '9', '9']]


def completed_number(prefix, length):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """

    ccnumber = prefix

    # generate digits

    while len(ccnumber) < (length - 1):
        digit = str(generator.choice(range(0, 10)))
        ccnumber.append(digit)

    # Calculate sum

    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    while pos < length - 1:

        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):

            sum += int(reversedCCnumber[pos + 1])

        pos += 2

    # Calculate check digit

    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10

    ccnumber.append(str(checkdigit))

    return ''.join(ccnumber)
def luhn(n):
	r = [int(ch) for ch in str(n)][::-1]
	return (sum(r[0::2]) + sum(sum(divmod(d*2,10)) for d in r[1::2])) % 10 == 0

def cardLuhnChecksumIsValid(card_number):
    """ checks to make sure that the card passes a luhn mod-10 checksum """

    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1

    for count in range(0, num_digits):
        digit = int(card_number[count])

        if not (( count & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9

        sum = sum + digit

    return ( (sum % 10) == 0 )


def credit_card_number(rnd, prefixList, length, howMany):

    result = ''

    while len(result) < howMany:

        ccnumber = copy.copy(rnd.choice(prefixList))
        result = completed_number(ccnumber, length)

    return result

def credit_card_number_list(rnd, prefixList, length, howMany):

    result = []

    while len(result) < howMany:

        ccnumber = copy.copy(rnd.choice(prefixList))
        ccarray.append(completed_number(ccnumber, length))
	result.append(completed_number(ccnumber, length))
	
    return result

def credit_card_number_other(rnd, prefix, length):

    result = ''
    ccnumber = copy.copy(prefix)
    result = completed_number(ccnumber, length)
   
    #result = result -1

    return result

def output(title, numbers):

    result = []
    result.append(title)
    result.append('-' * len(title))
    result.append('\n'.join(numbers))
    result.append('')

    return '\n'.join(result)

#
# Main
#

generator = Random()
generator.seed()        # Seed from current time

p = remote('misc.chal.csaw.io', 8308)

credit_card_number_list(generator, discoverPrefixList, 16, 20000)
credit_card_number_list(generator, visaPrefixList, 16, 20000)
credit_card_number_list(generator, mastercardPrefixList, 16, 20000)
#credit_card_number_list(generator, amexPrefixList, 15, 5000)
#credit_card_number_list(generator, dinersPrefixList, 14, 5000)
credit_card_number_list(generator, jcbPrefixList, 16, 10000)
credit_card_number_list(generator, enRoutePrefixList, 15, 10000)
#credit_card_number_list(generator, voyagerPrefixList, 15, 5000)


print(ccarray)


while True:
    wha = p.recvline(timeout=3)
    if 'I need a new Discover!\n' in wha:
	print(wha)
	sleep(0.1)
        discover = credit_card_number(generator, discoverPrefixList, 16, 1)
        p.sendline(discover)
	print(discover)
	#ccarray.append(discover)
    elif 'I need a new Visa!\n' in wha:
	print(wha)
	sleep(0.1)
        visa = credit_card_number(generator, visaPrefixList, 16, 1)
        p.sendline(visa)
	print(visa)
 	#ccarray.append(visa)
    elif 'I need a new MasterCard!\n' in wha:
	print(wha)
	sleep(0.1)
        mc = credit_card_number(generator, mastercardPrefixList, 16, 1)
        p.sendline(mc)
	print(mc)
	#ccarray.append(mc)
    elif 'I need a new American Express!\n' in wha:
	print(wha)	
	sleep(0.1)
        amex = credit_card_number(generator, amexPrefixList, 15, 1)
        p.sendline(amex)
	print(amex)
	#ccarray.append(amex)
    elif 'I need a new card that starts with' in wha:
	print(wha)	
	sleep(0.1)
        #get starting sequence 35,-2
        otherPrefix = wha[35:-2]
	print(otherPrefix)
        otharr = []
        otharr.append(list(otherPrefix))
	print(otharr)
        oth = credit_card_number(generator, otharr, 16, 1)
        p.sendline(oth)
	print(oth)
	#ccarray.append(oth)
    elif 'I need a new card which ends with' in wha:
	print(wha)
	oth2a = ''	
	sleep(0.1)
        #get starting sequence 34,-2
        otherSuffix2 = wha[34:-2]
	print(otherSuffix2)
        for cc in ccarray:
            if cc.endswith(otherSuffix2):
		oth2a = cc
		break
	ccarray.remove(oth2a)	
	p.sendline(oth2a)
	print(oth2a)
	#ccarray.append(oth)
    elif 'I need to know if' in wha:
	print(wha)
	v = ''
	sleep(0.1)
        valcc = wha[18:-29]
	print(valcc)
	if luhn(valcc):
		print('true')
        	sleep(0.1)
		p.sendline('1')
	else:
		print('false')
        	sleep(0.1)
		p.sendline('0')
    elif 'Thanks!\n' in wha:
	print(wha)
    else:
	print(wha) # hopefully the flag