#
# Copyright 2021 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from datetime import datetime, timedelta
from dateutil import tz
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email import Encoders

import org.slf4j.LoggerFactory as LoggerFactory
logger = LoggerFactory.getLogger("Outlook")

import smtplib

zone_eastern = tz.gettz('America/New_York')
zone_utc = tz.gettz('UTC')

new_line = "\r\n"
attendees = [attendee.strip() for attendee in emails.split(',')]
organizer = "ORGANIZER;CN=Organizer:mailto:" + fromSender
fro = fromSender

ddtstart = (datetime.now() + timedelta(days = 1)).strftime("%Y%m%dT%H%M%SZ")
# offset = timedelta(hours = 4)
dtend = (datetime.now() + timedelta(days = 1) + timedelta(hours = 1)).strftime("%Y%m%dT%H%M%SZ")
dtstamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")

description = message + new_line
attendee = ""
for att in attendees:
    attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE" + new_line + " ;CN=" + att + ";X-NUM-GUESTS=0:" + new_line + " mailto:" + att + new_line

ical = "BEGIN:VCALENDAR" + new_line + "PRODID:pyICSParser" + new_line + "VERSION:2.0" + new_line + "CALSCALE:GREGORIAN" + new_line
ical += "METHOD:REQUEST" + new_line + "BEGIN:VEVENT" + new_line + "DTSTART:" + datetime.strptime(timeStart, "%m/%d/%y %H:%M").replace(tzinfo = zone_eastern).astimezone(zone_utc).strftime("%Y%m%dT%H%M%SZ") + new_line + "DTEND:" + datetime.strptime(timeEnd, "%m/%d/%y %H:%M").replace(tzinfo = zone_eastern).astimezone(zone_utc).strftime("%Y%m%dT%H%M%SZ") + new_line+"DTSTAMP:" + dtstamp + new_line + organizer + new_line
ical += "UID:FIXMEUID" + dtstamp + new_line
ical += attendee + "CREATED:" + dtstamp + new_line + description + "LAST-MODIFIED:" + dtstamp + new_line + "LOCATION:" + new_line + "SEQUENCE:0" + new_line + "STATUS:CONFIRMED" + new_line
ical += "SUMMARY:" + subject + new_line + "TRANSP:OPAQUE" + new_line + "END:VEVENT" + new_line + "END:VCALENDAR" + new_line

eml_body = message
eml_body_bin = "Binary content."
msg = MIMEMultipart('mixed')
msg['Reply-To'] = fro
msg['Date'] = formatdate(localtime = True)
msg['Subject'] = subject
msg['From'] = fro
msg['To'] = ",".join(attendees)

part_email = MIMEText(eml_body,"html")
part_cal = MIMEText(ical,'calendar;method=REQUEST')

msgAlternative = MIMEMultipart('alternative')
msg.attach(msgAlternative)

ical_atch = MIMEBase('application/ics',' ;name="%s"' % ("invite.ics"))
ical_atch.set_payload(ical)
Encoders.encode_base64(ical_atch)
ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"' % ("invite.ics"))

eml_atch = MIMEBase('text/plain', '')
Encoders.encode_base64(eml_atch)
eml_atch.add_header('Content-Transfer-Encoding', "")

msgAlternative.attach(part_email)
msgAlternative.attach(part_cal)

mailServer = smtplib.SMTP(server.get('SMTPServer'), 587)
mailServer.starttls()
mailServer.ehlo()
mailServer.login(server.get('username'), server.get('password'))
mailServer.sendmail(fro, attendees, msg.as_string())
mailServer.close()