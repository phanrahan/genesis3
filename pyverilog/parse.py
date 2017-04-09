from __future__ import absolute_import
from __future__ import print_function
import sys
import os
from optparse import OptionParser

# the next line can be removed after installation
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyverilog.vparser.parser import parse, Node, Input, Output, ModuleDef
from pyverilog.dataflow.visit import NodeVisitor

class IdentifierVisitor(NodeVisitor):
    def visit_Identifier(self, node):
        print(node.name)
        return node

class ModuleArgumentsVisitor(NodeVisitor):
    def visit_Portlist(self, node):
        node.show()
        return node

class ArgumentVisitor(NodeVisitor):
    def __init__(self):
        self.nodes = []

    def visit_Input(self, node):
        self.nodes.append(node)
        return node

    def visit_Output(self, node):
        self.nodes.append(node)
        return node

class DefVisitor(NodeVisitor):
    def __init__(self):
        self.nodes = []

    def visit_ModuleDef(self, node):
        self.nodes.append(node)
        return node

def usage():
    print("Usage: python parse.py file ...")
    sys.exit()

def main():

    optparser = OptionParser()
    (options, filelist) = optparser.parse_args()

    if len(filelist) == 0:
        usage()

    ast, directives = parse(filelist)
    
    #ast.show()

    v = DefVisitor()
    v.visit(ast)
    for node in v.nodes:
        print(node.name, '=', 'DeclareCircuit(', '"{}", '.format(node.name), end='')
        for port in node.portlist.ports:
            io = port.first
            print('"{}", '.format(io.name), end='')
            msb = int(io.width.msb.value)
            lsb = int(io.width.lsb.value)
            if isinstance(io, Input):  dir = 'In'
            if isinstance(io, Output): dir = 'Out'
            if msb == 0 and lsb == 0:
                print('{}(Bit), '.format(dir), end='')
            else:
                print('{}(Array({},Bit)), '.format(dir, msb-lsb+1), end='')
        print()
        
if __name__ == '__main__':
    main()
