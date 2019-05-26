"""Run all tests: look for gold files in given directory,
run the corresponding test, then do a simple line-by-line 
comparison."""

import inspect
import logging
import os
from subprocess import Popen, STDOUT, PIPE
import sys


# If command-line parameter is one of DEBUG, INFO, WARNING, etc. (lower case
# accepted) then use the parameter to set the log level, otherwise ignore it.
try:
    logging.getLogger().setLevel(
        eval('logging.{}'.format(sys.argv[1].upper())))
except:
    pass

logging.basicConfig(format='%(levelname)-8s | %(message)s')

# Compute the absolute path of the directory containing this file.
this_dir = os.path.dirname(
    os.path.abspath(
        inspect.getfile(
            inspect.currentframe())))

for entry in sorted(os.listdir(this_dir)):

    # Decide whether this entry is a gold file. There are two types, based
    # on filename suffix:
    # 1) *.gold files contain the exact content expected from test output.
    # 2) *.goldr files contain expected output, only "randomized."
    #    I.e. we expect the test to produce the same content, but the lines
    #    may not be in the same order.
    gold_fname = os.path.join(this_dir, entry)
    suffix = None
    for choice in ('.gold', '.goldr'):
        if gold_fname[-len(choice):] == choice:
            suffix = choice
    if not suffix:
        logging.debug('Ignoring %s, not a gold file.', entry)
        continue

    # Read the gold file.
    with open(gold_fname) as f:
        gold_lines = f.readlines()
    logging.debug('Gold file %s has %d lines.', gold_fname, len(gold_lines))

    # Run the test.
    test_fname = gold_fname[:-len(suffix):] + '.py'
    command = '{} {}'.format(sys.executable, test_fname)
    logging.info('Running command: %s', command)
    p = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
    test_lines = p.stdout.readlines()
    logging.debug('Test output has %d lines.', len(test_lines))
    
    # In case of "randomized" gold file, sort lines before comparing.
    if suffix == '.goldr':
        gold_lines, test_lines = sorted(gold_lines), sorted(test_lines)

    # Compare gold output with test output, line-by-line.
    for gold_line, test_line in zip(gold_lines, test_lines):
        gold_line, test_line = gold_line.strip(), test_line.strip().decode()
        if gold_line == test_line:
            continue
        print('Error running: {}'.format(command))
        out_fname = gold_fname[:-len(suffix):] + '.out'
        with open(out_fname, 'w') as f:
            for line in test_lines:
                f.write(line.decode())
        print('To see diff run: diff {} {}'.format(gold_fname, out_fname))
        break
