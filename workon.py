#!/usr/bin/env python3
#
# workon - spawn a new subshell with appropriate working dir and environment
#
# Forked and updated by <Your Name>, <Year>
#   - Ported to Python 3 from the original Python 2 script
#   - Expands `~` and `$HOME` in `<chdir>` paths.
#
# Originally written by Ivan Nestlerode, 2004
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# This program was inspired by the Perl program of the same name written by
# Rajesh Vaidheeswarran. However, it does not share any code. The ~/.workon
# syntax in this version is different (this one is XML-based). Also, this
# version is less CVS-centric.

import getopt, os, sys
import xml.dom.minidom

majorVersion = 2
minorVersion = 0
versionString = '%d.%d' % (majorVersion, minorVersion)

def usage(progName):
    print('usage: %s [-h] [-l] [-n] [-v] <state>' % progName)

class ParseException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def getText(node):
    result = ''
    for n in node.childNodes:
        if n.nodeType == node.TEXT_NODE:
            result += n.data
    return result

def getChdir(nodes):
    for node in nodes:
        if node.nodeType == node.ELEMENT_NODE and node.nodeName == 'chdir':
            result = getText(node)
            return result
    return None

def getVars(nodes):
    result = {}
    for node in nodes:
        if node.nodeType == node.ELEMENT_NODE and node.nodeName == 'var':
            # Get value from the 'value' attribute, not from text content
            value = node.getAttribute('value')
            if not value:
                # Fallback to text content for backward compatibility
                value = getText(node)
            # Use shell evaluation to handle command substitution like $(pwd)
            shellCmd = 'eval echo "' + value + '"'
            f = os.popen(shellCmd, 'r')
            result[node.getAttribute('name')] = f.read()[:-1]
            f.close()
    return result

def getWorkonState(state):
    fileName = os.path.join(os.environ['HOME'], '.workon')
    dom = xml.dom.minidom.parse(fileName)
    if len(dom.childNodes) != 1:
        raise ParseException('only one top level element allowed (workon)')
    workon = dom.childNodes[0]
    if workon.nodeName != 'workon':
        raise ParseException('top level element must be named workon')
    chdir = None
    xmlEnv = {}
    xmlEnv.update(getVars(workon.childNodes))
    foundState = False
    for node in workon.childNodes:
        if node.nodeType == node.ELEMENT_NODE and \
           node.nodeName == 'state' and \
           node.getAttribute('name') == state:
            foundState = True
            chdir = getChdir(node.childNodes)
            xmlEnv.update(getVars(node.childNodes))
    if not foundState:
        raise ParseException('%s is an unknown work state' % state)
    if chdir == None:
        chdir = '.'
    # Expand ~ and $HOME in chdir
    chdir = os.path.expanduser(os.path.expandvars(chdir))
    xmlEnv['WORKONSTATE'] = state
    newEnv = os.environ.copy()
    newEnv.update(xmlEnv)
    return {'chdir' : chdir, 'env' : newEnv}

def getStates():
    fileName = os.path.join(os.environ['HOME'], '.workon')
    dom = xml.dom.minidom.parse(fileName)
    if len(dom.childNodes) != 1:
        raise ParseException('only one top level element allowed (workon)')
    workon = dom.childNodes[0]
    if workon.nodeName != 'workon':
        raise ParseException('top level element must be named workon')
    foundState = False
    for node in workon.childNodes:
        if node.nodeType == node.ELEMENT_NODE and \
           node.nodeName == 'state':
            print(node.getAttribute('name'))
            foundState = True
    if not foundState:
        print('No workon state found!')
    return

def main(argv):
    progName = os.path.basename(argv[0])
    try:
        opts, args = getopt.getopt(argv[1:], 'hlnv', ['help', 'list', 'nochdir', 'no-chdir', 'version'])
    except getopt.GetoptError:
        usage(progName)
        sys.exit(1)
    doChdir = True
    for o, a in opts:
        if o in ('-n', '--nochdir', '--no-chdir'):
            doChdir = False
        if o in ('-h', '--help'):
            usage(progName)
            sys.exit(0)
        if o in ('-v', '--version'):
            print('%s version %s' % (progName, versionString))
            sys.exit(0)
        if o in ('-l', '--list'):
            getStates()
            sys.exit(0)
    if len(args) != 1:
        usage(progName)
        sys.exit(1)
    try:
        state = getWorkonState(args[0])
    except ParseException as e:
        sys.stderr.write('parse error: %s\n' % str(e))
        sys.exit(2)
    if doChdir:
        os.chdir(state['chdir'])
    os.execle(os.environ['SHELL'], os.environ['SHELL'], state['env'])

if __name__ == '__main__':
    main(sys.argv) 