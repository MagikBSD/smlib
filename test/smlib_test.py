from smlib import *
import unittest

class MessageTest(unittest.TestCase):
    def test_basic(self):
        msg = Message()
        msg.per('from@example.com')
        msg.to('to@example.com')
        msg.subject('Test')
        msg.text('This is a test.')
        self.assertEqual(str(msg), 'Content-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: quoted-printable\nFrom: from@example.com\nTo: to@example.com\nSubject: =?utf-8?Q?Test?=\n\nThis is a test.')

    def test_envelope_per(self):
        msg = Message()
        msg.per('from@example.com')
        self.assertEqual(msg.envelope_per, 'from@example.com')

    def test_envelope_to(self):
        msg = Message()
        msg.to('to1@example.com')
        msg.to('to2@example.com')
        msg.cc('to3@example.com')
        msg.bcc('to4@example.com')
        self.assertEqual(msg.envelope_to, ['to1@example.com', 'to2@example.com', 'to3@example.com', 'to4@example.com'])

    def test_reply_to(self):
        msg = Message()
        msg.per('from1@example.com')
        msg.reply_to('from2@example.com')
        msg.to('to@example.com')
        msg.subject('Test')
        msg.text('This is a test.')
        self.assertEqual(str(msg), 'Content-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: quoted-printable\nFrom: from1@example.com\nReply-To: from2@example.com\nTo: to@example.com\nSubject: =?utf-8?Q?Test?=\n\nThis is a test.')

    def test_to(self):
        msg = Message()
        msg.per('from@example.com')
        msg.to('to1@example.com')
        msg.to('to2@example.com')
        msg.subject('Test')
        msg.text('This is a test.')
        self.assertEqual(str(msg), 'Content-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: quoted-printable\nFrom: from@example.com\nTo: to1@example.com, to2@example.com\nSubject: =?utf-8?Q?Test?=\n\nThis is a test.')

    def test_cc(self):
        msg = Message()
        msg.per('from@example.com')
        msg.to('to1@example.com')
        msg.cc('to2@example.com')
        msg.cc('to3@example.com')
        msg.subject('Test')
        msg.text('This is a test.')
        self.assertEqual(str(msg), 'Content-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: quoted-printable\nFrom: from@example.com\nTo: to1@example.com\nCc: to2@example.com, to3@example.com\nSubject: =?utf-8?Q?Test?=\n\nThis is a test.')

    def test_bcc(self):
        msg = Message()
        msg.per('from@example.com')
        msg.to('to1@example.com')
        msg.bcc('to2@example.com')
        msg.bcc('to3@example.com')
        msg.subject('Test')
        msg.text('This is a test.')
        self.assertEqual(str(msg), 'Content-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: quoted-printable\nFrom: from@example.com\nTo: to1@example.com\nSubject: =?utf-8?Q?Test?=\n\nThis is a test.')

    def test_clear_dest(self):
        msg = Message()
        msg.per('from@example.com')
        msg.to('to1@example.com')
        msg.cc('to2@example.com')
        msg.bcc('to3@example.com')
        msg.clear_dest()
        msg.to('to4@example.com')
        msg.subject('Test')
        msg.text('This is a test.')
        self.assertEqual(str(msg), 'Content-Type: text/plain; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: quoted-printable\nFrom: from@example.com\nTo: to4@example.com\nSubject: =?utf-8?Q?Test?=\n\nThis is a test.')

    def test_html(self):
        msg = Message()
        msg.per('from@example.com')
        msg.to('to@example.com')
        msg.subject('Test')
        msg.html('<p>This is a test.</p>')
        self.assertEqual(str(msg), 'Content-Type: text/html; charset="utf-8"\nMIME-Version: 1.0\nContent-Transfer-Encoding: quoted-printable\nFrom: from@example.com\nTo: to@example.com\nSubject: =?utf-8?Q?Test?=\n\n<p>This is a test.</p>')

    def test_text_and_html(self):
        msg = Message()
        msg.per('from@example.com')
        msg.to('to@example.com')
        msg.subject('Test')
        msg.text('This is a test.')
        msg.html('<p>This is a test.</p>')
        self.assertRegexpMatches(str(msg), 'Content\-Type: multipart/alternative;\\n boundary="===============[0-9]{19}=="\\nMIME\-Version: 1.0\\nFrom: from@example.com\\nTo: to@example.com\\nSubject: =\?utf\-8\?Q\?Test\?=\\n\\n\-\-===============[0-9]{19}==\\nContent\-Type: text/plain; charset="utf\-8"\\nMIME\-Version: 1.0\\nContent\-Transfer\-Encoding: quoted\-printable\\n\\nThis is a test.\\n\-\-===============[0-9]{19}==\\nContent\-Type: text/html; charset="utf\-8"\\nMIME\-Version: 1.0\\nContent\-Transfer\-Encoding: quoted\-printable\\n\\n<p>This is a test.</p>\\n\-\-===============[0-9]{19}==\-\-\\n')
