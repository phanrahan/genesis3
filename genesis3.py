from __future__ import absolute_import
from __future__ import print_function
from collections import namedtuple
from functools import lru_cache
from optparse import OptionParser

from mako.template import Template

from pyverilog.vparser.parser import VerilogParser, Node, Input, Output, ModuleDef
from pyverilog.dataflow.visit import NodeVisitor

from magma import Bit, Array, In, Out, DeclareCircuit, DefineCircuit, EndCircuit


#class IdentifierVisitor(NodeVisitor):
#    def visit_Identifier(self, node):
#        print(node.name)
#        return node

#class ModuleArgumentsVisitor(NodeVisitor):
#    def visit_Portlist(self, node):
#        node.show()
#        return node

#class ArgumentVisitor(NodeVisitor):
#    def __init__(self):
#        self.nodes = []
#
#    def visit_Input(self, node):
#        self.nodes.append(node)
#        return node
#
#    def visit_Output(self, node):
#        self.nodes.append(node)
#        return node

class ModuleVisitor(NodeVisitor):
    def __init__(self):
        self.nodes = []

    def visit_ModuleDef(self, node):
        self.nodes.append(node)
        return node

def FromVerilog(source):
    parser = VerilogParser()

    ast = parser.parse(source)
    #ast.show()

    v = ModuleVisitor()
    v.visit(ast)
    assert len(v.nodes) == 1
    node = v.nodes[0]

    args = []
    for port in node.portlist.ports:
        io = port.first
        args.append( '"{}", '.format(io.name) )
        msb = int(io.width.msb.value)
        lsb = int(io.width.lsb.value)
        if   isinstance(io, Input):  dir = 'In'
        elif isinstance(io, Output): dir = 'Out'
        else: continue
        if msb == 0 and lsb == 0:
            t = Bit
        else:
            t = Array(msb-lsb+1, Bit)
        args.append( In(t) if dir == 'In' else Out(t) )

    return node.name, args

def DeclareFromVerilog(source):
    name, args = FromVerilog(source)
    return DeclareCircuit(name, *args)

def DefineFromVerilog(source):
    name, args = FromVerilog(source)
    circuit =  DefineCircuit(name, *args)
    circuit.verilog = source
    EndCircuit()
    return circuit

@lru_cache(maxsize=32)
def DeclareFromVerilogFile(file):
    if file is None:
        return None

    source = open(file).read()

    return DeclareFromVerilog(source)


#
# generate the name of the module
#
#  this is not robust: we only look at a single keyword argument
#
def genname(name, kwargs):
    if 'N' in kwargs:
        name += '%d' % kwargs['N']
    return name

#
# generate parameters that will be passed to the template
#
def genparameters(name, kwargs):
    kwargs = dict(kwargs)
    if 'name' not in kwargs:
        kwargs['name'] = name
    return namedtuple(name+'_t', kwargs.keys())(**kwargs)

@lru_cache(maxsize=32)
def DefineFromTemplatedVerilogFile(name, file, **kwargs):
    if file is None:
        return None

    source = open(file).read()

    name = genname(name, kwargs)
    parameters = genparameters(name, kwargs)

    verilog = Template(source).render(parameters=parameters)

    return DefineFromVerilog(verilog)

if __name__ == '__main__':
    import sys
    from magma import compile

    if len(sys.argv) != 2:
        print('usage: genesis3 name\n')
        sys.exit(0)

    name = sys.argv[1]
    filename = name+'.vp'

    main = DefineFromTemplatedVerilogFile(name, filename, N=4)

    compile(name, main)

    #main = DeclareFromVerilogFile('CSA.v')
    #print(main, main.IO)

    #main = DefineFromTemplatedVerilogFile('CSA', 'CSA.vp', N=4)
    # print(main, main.IO)





