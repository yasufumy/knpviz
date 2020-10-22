import re
import subprocess

import six


class Subprocess(object):

    def __init__(self, command, timeout=180):
        self.subproc_args = {'stdout': subprocess.PIPE, 'stderr': subprocess.STDOUT, 'timeout': timeout}
        self.command = command

    def query(self, sentence, pattern):
        assert(isinstance(sentence, six.text_type))
        proc = subprocess.run(self.command, input=(sentence+"\n").encode(), check=True, **self.subproc_args)
        result = ""
        for line in proc.stdout.decode().split("\n"):
            if re.search(pattern, line):
                break
            result = "%s%s\n" % (result, line)
        return result
