
from apx import apx
import unittest
import subprocess
from apx.apx import Logger
import shlex

class ExecutorTest(unittest.TestCase):

    def testNoInput(self):
        cmd = 'bin/apx -- echo "--\\n--"'
        args = shlex.split(cmd)
        proc = subprocess.Popen(args,
                        stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        proc.wait()
        self.assertEqual(proc.stderr.read(), "no input data\n")

    def testEcho(self):
        cmd = 'bin/apx -o -- echo "aaaaaa"'
        args = shlex.split(cmd)
        proc = subprocess.Popen(args,
                        stderr=subprocess.PIPE, 
                        stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE) #nodig voor communicate()

        stdout, stderr = proc.communicate(input=open('tests/attachments/one_1.mbox').read())
        self.assertEqual(stdout, "aaaaaa\n")

if __name__ == "__main__":
    Logger.instance = Logger(log_level='error', verbosity=0, quiet=True)
    unittest.main()
