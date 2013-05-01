"""Create the Sphinx documentation pages.
Run from the current directory, e.g.:
  python ./create.py build/
"""

import subprocess
import mpipe
import sys
import os

try:
    DEST = sys.argv[1]
except:
    print('Usage:  %s destination'%sys.argv[0])
    sys.exit(1)

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
    ifname = '%s.dia'%diagram
    ofname = '%s.png'%diagram
    cmd = 'dia -e %s %s'%(ofname, ifname)
    print('  %s'%cmd)
    subprocess.call(cmd, shell=True)
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
    )
def runCopy(fname):
    cmd = 'cp %s source/'%os.path.join('..', 'test', fname)
    print('  %s'%cmd)
    subprocess.call(cmd, shell=True)
    return True
pipe = mpipe.Pipeline(mpipe.UnorderedStage(runCopy, len(codes)))
for fname in codes: 
    pipe.put(fname)
pipe.put(None)
for result in pipe.results():
    pass
    
# Build the Sphinx documentation pages.
cmd = 'make BUILDDIR=%s clean html'%DEST
print('  %s'%cmd)
subprocess.call(cmd, shell=True)

# Move the .py examples to the build/ destination directory
# so that documentation links to source code will work.
def runMove(fname):
    cmd = 'mv %s build/html/'%os.path.join('source', fname)
    print('  %s'%cmd)
    subprocess.call(cmd, shell=True)
    return True
pipe = mpipe.Pipeline(mpipe.UnorderedStage(runMove, len(codes)))
for fname in codes: 
    pipe.put(fname)
pipe.put(None)

# Cleanup diagrams.
saved = os.getcwd()
os.chdir('source')
def runDia(diagram):
    fname1 = '%s.dia~'%diagram
    fname2 = '%s.png'%diagram
    cmd = 'rm -f %s %s'%(fname1, fname2)
    print('  %s'%cmd)
    subprocess.call(cmd, shell=True)
    return True
pipe = mpipe.Pipeline(mpipe.UnorderedStage(runDia, len(diagrams)))
for diagram in diagrams: 
    pipe.put(diagram)
pipe.put(None)
for result in pipe.results():
    pass
os.chdir(saved)

# The end.
