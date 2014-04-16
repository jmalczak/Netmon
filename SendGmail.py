# netmon script #

import os
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64

class SendGMail:
    def __init__(self, user, password):
        self.user = user
        self.password = password
    def send(self, recipient, subject, text, *attachmentPaths):
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(text))

        for attachmentPath in attachmentPaths:
            msg.attach(self.getAttachment(attachmentPath))

        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(self.user, self.password)
        mailServer.sendmail(gmailUser, recipient, msg.as_string())
        mailServer.close()

    def getAttachment(self, attachmentFilePath):
        contentType, encoding = mimetypes.guess_type(attachmentFilePath)

        if contentType is None or encoding is not None:
            contentType = 'application/octet-stream'

        mainType, subType = contentType.split('/', 1)
        file = open(attachmentFilePath, 'rb')

        if mainType == 'text':
            attachment = MIMEText(file.read())
        elif mainType == 'message':
            attachment = email.message_from_file(file)
        elif mainType == 'image':
            attachment = MIMEImage(file.read(),_subType=subType)
        elif mainType == 'audio':
            attachment = MIMEAudio(file.read(),_subType=subType)
        else:
            attachment = MIMEBase(mainType, subType)
            attachment.set_payload(file.read())
            encode_base64(attachment)

        file.close()
        attachment.add_header('Content-Disposition', 'attachment',  filename=os.path.basename(attachmentFilePath))
        
        return attachment
