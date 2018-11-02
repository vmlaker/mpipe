"""
Create the Sphinx documentation pages.
Run from the current directory, e.g.:
  venv/bin/python ./create.py build/
"""

import subprocess
import mpipe
import sys
import os


try:
    DEST = sys.argv[1]
except:
    print('Usage:  {} destination'.format(sys.argv[0]))
    sys.exit(1)


def call(command):
    print('  {}'.format(command))
    subprocess.call(command, shell=True)
 

# Diagram filename prefixes.
diagrams = (
    'tiny',
    'helloworld',
    'chain',
    'pipeout',
    'fork',
    'taskresult1',
    'worker1',
    'worker2',
    'stage1',
    'pipeline1',
    'multiwork',
    'filter',
    )

# Export Dia diagrams.
saved = os.getcwd()
os.chdir('source')
def runDia(diagram):
    """Generate the diagrams using Dia."""
    ifname = '{}.dia'.format(diagram)
    ofname = '{}.png'.format(diagram)
    call('dia -t png-libart -e {} {}'.format(ofname, ifname))
    return True
pipe = mpipe.Pipeline(mpipe.UnorderedStage(runDia, len(diagrams)))
for diagram in diagrams: 
    pipe.put(diagram)
pipe.put(None)
for result in pipe.results():
    pass
os.chdir(saved)

# Copy the .py examples from test/ to source/ directory
# so that they can be picked up by the Sphinx build.
codes = (
    'tiny.py',
    'helloworld.py',
    'chain.py',
    'pipeout.py',
    'fork.py',
    'unordered.py',
    'count_nullops.py',
    'multiwork.py',
    'clog.py',
    'drano.py',
    'bottleneck1.py',
    'bottleneck2.py',
    'bottleneck3.py',
    'disable_result0.py',
    )
def runCopy(fname):
    call('cp {} source/'.format(os.path.join('..', 'test', fname)))
    return True
pipe = mpipe.Pipeline(mpipe.UnorderedStage(runCopy, len(codes)))
for fname in codes: 
    pipe.put(fname)
pipe.put(None)
for result in pipe.results():
    pass
    
# Build the Sphinx documentation pages.
call('make BUILDDIR={} SPHINXBUILD={} clean html'.format(DEST, '../venv/bin/sphinx-build'))

# Move the .py examples to the build/ destination directory
# so that documentation links to source code will work.
def runMove(fname):
    call('mv {} build/html/'.format(os.path.join('source', fname)))
    return True
pipe = mpipe.Pipeline(mpipe.UnorderedStage(runMove, len(codes)))
for fname in codes: 
    pipe.put(fname)
pipe.put(None)

# Cleanup diagrams.
saved = os.getcwd()
os.chdir('source')
def runDia(diagram):
    fname1 = '{}.dia~'.format(diagram)
    fname2 = '{}.png'.format(diagram)
    call('rm -f {} {}'.format(fname1, fname2))
    return True
pipe = mpipe.Pipeline(mpipe.UnorderedStage(runDia, len(diagrams)))
for diagram in diagrams: 
    pipe.put(diagram)
pipe.put(None)
for result in pipe.results():
    pass
os.chdir(saved)
