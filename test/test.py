"""Run all tests: look for gold files in given directory,
run the corresponding test, then do a simple line-by-line 
comparison."""

import sys
import os
import inspect
from subprocess import Popen, STDOUT, PIPE

# Compute the absolute path to directory of this file.
this_dir = os.path.dirname(
    os.path.abspath(
        inspect.getfile(
            inspect.currentframe())))

for entry in sorted(os.listdir(this_dir)):

    # Identify the file -- whether it is gold.
    # Gold files are *.go for exact gold content, or 
    # *.gor if "random" (to be sorted before comparing.
    gold_fname = os.path.join(this_dir, entry)
    suffix = None
    for choice in ('.go', '.gor'):
        if gold_fname[-len(choice):] == choice:
            suffix = choice
    if not suffix:
        continue

    # Read the gold file.
    f = open(gold_fname)
    gold_lines = f.readlines()
    f.close()

    # Run the test.
    test_fname = gold_fname[:-len(suffix):] + '.py'
    command = '{0} {1}'.format(sys.executable, test_fname)
    print(command)
    p = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
    test_lines = p.stdout.readlines()

    # If test "randomizes" output, sort lines before comparing.
    if suffix == '.gor':
        gold_lines = sorted(gold_lines)
        test_lines = sorted(test_lines)

    # Compare line by line.
    failed = False
    for gline, tline in zip(gold_lines, test_lines):
        gline = gline.strip()
        tline = tline.strip().decode()
        if gline != tline:
            print('Error running: {0}'.format(command))
            failed = True            
            break

    # On failure, save test output.
    if failed:
        out_fname = gold_fname[:-len(suffix):] + '.out'
        f = open(out_fname, 'w')
        for line in test_lines:
            f.write(line.decode())
        f.close
