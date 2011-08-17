from apx import apx
import unittest
import email
from apx.apx import Logger

class ApxTest(unittest.TestCase):

    def setUp(self):
        self.ap = apx.AttachmentParser()

    def getMail(self, filename):
        string = open('tests/attachments/%s' % filename).read()
        return email.message_from_string(string)

    def testNoAttachments(self):
        files = ['zero_1.eml', 'zero_2.mbox', 'zero_3.mbox']
        for file in files:
            attachments = self.ap.get_attachments(self.getMail(file))
            self.assertEqual(len(attachments), 0)

    def testOneAttachments(self):
        files = ['one_1.mbox', 'one_2.eml', 'one_3.mbox', 'one_4.mbox']
        for file in files:
            attachments = self.ap.get_attachments(self.getMail(file))
            self.assertEqual(len(attachments), 1)

    def testTwoAttachments(self):
        files = ['two_1.mbox', 'two_2.mbox']
        for file in files:
            attachments = self.ap.get_attachments(self.getMail(file))
            self.assertEqual(len(attachments), 2)

    def testThreeAttachments(self):
        files = ['three_1.mbox', 'three_2.mbox']
        for file in files:
            attachments = self.ap.get_attachments(self.getMail(file))
            self.assertEqual(len(attachments), 3)

if __name__ == "__main__":
    Logger.instance = Logger(log_level='error', verbosity=0, quiet=True)
    unittest.main()
