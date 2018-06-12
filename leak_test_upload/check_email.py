#!/usr/bin/env python
#
# This program checks mu2e.bot.umn@gmail.com email for blank email
# response from mu2e factory on a certain day. If there is a blank email
# response 
#
# RKI July 2013
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#


import email

def check_for_confirmation(M, date_to_upload):
        M.select()
	rv, data = M.search(None, "ALL")
	if rv != 'OK': # empty inbox
		print("No messages found!")
		return
	
	# iterate through emails
	for num in data[0].split():
		rv, data = M.fetch(num, '(RFC822)')
		if rv != 'OK':
			print("ERROR getting message", num)
			return
            
		# message attributes
		msg = email.message_from_string(data[0][1].decode('utf-8'))
		body = str(msg.get_payload(0))
		decode = email.header.decode_header(msg['Subject'])[0]
		subject = str(decode[0])    
	
		if (subject.startswith("Re: 20")):
			blankline = body.splitlines()[2]
			REline = body.splitlines()[3] # line after blank--start of quoted message
			date_of_email = body.splitlines()[5]
			date_of_email = date_of_email[2:len(date_of_email)] # date of data
			if( blankline == '' and REline[0:2] == 'On' and date_of_email == date_to_upload):
				return True
		
		#print(body)		
		#print('-------------')
		#print(date_of_email)
		#print(blankline)
		#print(REline[0:2])
		#print( REline[0:2], '###', blankline,'##', date_of_email )

	return False
    
