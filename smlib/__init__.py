import email.charset
import email.encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os.path
import smtplib

class Message:
    envelope_per = ''
    envelope_to = []
    __per = ''
    __reply_to = ''
    __to = []
    __cc = []
    __subject = ''
    __text = ''
    __html = ''
    __attachments = []
    __message = ''

    def __init__(self):
        email.charset.add_charset('utf-8', email.charset.QP, email.charset.QP)

    def __reset(self):
        self.__message = ''

    def per(self, address, realname=''):
        self.__reset()
        self.__per = (address, realname)
        self.envelope_per = address

    def reply_to(self, address, realname=''):
        self.__reset()
        self.__reply_to = (address, realname)

    def to(self, address, realname=''):
        self.__reset()
        self.__to.append((address, realname))
        self.envelope_to.append(address)

    def cc(self, address, realname=''):
        self.__reset()
        self.__cc.append((address, realname))
        self.envelope_to.append(address)

    def bcc(self, address):
        self.envelope_to.append(address)

    def clear_dest(self):
        self.__reset()
        self.__to = []
        self.__cc = []
        self.envelope_to = []

    def subject(self, subject):
        self.__reset()
        self.__subject = subject

    def text(self, text):
        self.__reset()
        self.__text = text

    def html(self, html):
        self.__reset()
        self.__html = html

    def gen_text(self):
        from html2text import html2text
        self.__reset()
        self.__text = html2text(self.__html)

    def attach(self, fn, type=None):
        self.__reset()
        self.__attachments.append((fn, type))

    def __format_address(self, addr):
        if not addr[1]: return addr[0]
        else: return "%s (%s)" % (addr[0], str(Header(addr[1])).replace('?q?', '?Q?'))

    def __format_multiple_addresses(self, addrs):
        multi_addrs = []
        for addr in addrs:
            fmt_addr = self.__format_address(addr)
            multi_addrs.append(fmt_addr)
        return ', '.join(multi_addrs)

    def __format_attachment(self, fn, type):
        basename = os.path.basename(fn)
        if not type: type, _ = mimetypes.guess_type(fn)
        if not type: type = 'application/octet-stream'
        maintype, subtype = type.split('/')
        fh = open(fn, 'rb')
        file_content = fh.read()
        fh.close()
        attachment = MIMEBase(maintype, subtype)
        attachment.add_header('Content-ID', "<%s>" % basename)
        attachment.add_header('Content-Disposition', "attachment; filename=\"%s\"" % basename)
        attachment.set_payload(file_content)
        email.encoders.encode_base64(attachment)
        return attachment

    def __format_message(self):
        if not self.__per: raise SmException('header_from', "Header 'from (per)' is mandatory")
        if not self.__to: raise SmException('header_to', "Header 'to' is mandatory")
        if not self.__subject: raise SmException('header_subject', "Header 'subject' is mandatory")
        if not self.__text and not self.__html: raise SmException('content', 'Text or html is mandatory')
        if self.__text: msg = msg_text = MIMEText(self.__text, _charset='utf-8')
        if self.__html: msg = msg_html = MIMEText(self.__html, 'html', _charset='utf-8')
        if self.__text and self.__html:
            msg = MIMEMultipart('alternative')
            msg.attach(msg_text)
            msg.attach(msg_html)
        if self.__attachments:
            msg_alt = msg
            msg = MIMEMultipart('mixed')
            msg.attach(msg_alt)
            for fn, type in self.__attachments:
                attachment = self.__format_attachment(fn, type)
                msg.attach(attachment)
        msg['From'] = self.__format_address(self.__per)
        if self.__reply_to: msg['Reply-To'] = self.__format_address(self.__reply_to)
        msg['To'] = self.__format_multiple_addresses(self.__to)
        if self.__cc: msg['Cc'] = self.__format_multiple_addresses(self.__cc)
        msg['Subject'] = str(Header(self.__subject, 'utf-8')).replace('?q?', '?Q?')
        self.__message = msg.as_string()

    def __len__(self):
        if not self.__message: self.__format_message()
        return len(self.__message)

    def __str__(self):
        if not self.__message: self.__format_message()
        return self.__message

class Smtp:
    def __init__(self, host='localhost', port=25, crypto=None, user=None, password=None):
        self.__host = host
        self.__port = port
        self.__ssl = (crypto == 'SSL')
        self.__tls = (crypto == 'TLS')
        self.__user = user
        self.__password = password

    def sendmail(self, message, debug=0):
        if self.__ssl: server = smtplib.SMTP_SSL(self.__host, self.__port)
        else: server = smtplib.SMTP(self.__host, self.__port)
        if self.__tls: server.starttls()
        if self.__user: server.login(self.__user, self.__password)
        server.set_debuglevel(debug)
        server.sendmail(message.envelope_per, message.envelope_to, str(message))
        server.quit()

class SmException(Exception):
    def __init__(self, label, msg):
        self.label = label
        self.msg = msg

    def __str__(self):
        return self.msg
