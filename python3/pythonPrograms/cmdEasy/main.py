# -*- coding: CP936 -*-
import subprocess
import sys
import os


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    cmd = "cmd.exe"
    ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    print(ret)
    subprocess.call("dir")

    subprocess.call('ls -l', shell=True)
    res = subprocess.check_output(['ls', '-l'], shell=True)


