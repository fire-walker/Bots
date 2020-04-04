# import yagmail


# sender_email = 'official.providers@gmail.com'
# receiver_email = ''
# sender_password = 'somepass123'

# subject = "Check THIS out"
# contents = [
#     "This is the first paragraph in our email",
#     "As you can see, we can send a list of strings,",
#     "being this our third one",
# ]



# yag = yagmail.SMTP(user=sender_email, password=sender_password)
# yag.send(receiver_email, subject, contents)


import smtplib, ssl
# User configuration
sender_email = 'official.providers@gmail.com'
receiver_email = 'ravinduf123@gmail.com'
password = 'somepass123'
# Email text
email_body = '''
    This is a test email sent by Python. Isn't that cool?
'''

print("Sending the email...")
try:
    # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # Encrypts the email
    context = ssl.create_default_context()
    server.starttls(context=context)
    # We log in into our Google account
    server.login(sender_email, password)
    # Sending email from sender, to receiver with the email body
    server.sendmail(sender_email, receiver_email, email_body)
    print('Email sent!')
except Exception as e:
    print(f'Oh no! Something bad happened!\n {e}')
finally:
    print('Closing the server...')
    server.quit()
