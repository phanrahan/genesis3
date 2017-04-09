from functools import lru_cache
from collections import namedtuple
from mako.template import Template
from magma import *

def genname(name, kwargs):
    if 'N' in kwargs:
        name += '%d' % kwargs['N']
    return name

def genparameters(name, kwargs):
    kwargs = dict(kwargs)
    if 'name' not in kwargs:
        kwargs['name'] = name
    return namedtuple(name+'_t', kwargs.keys())(**kwargs)

@lru_cache(maxsize=32)
def DefineVerilog(name, *args, source=None):
    if not source:
        return None
    circuit = DefineCircuit(name, *args)
    circuit.verilog = source
    EndCircuit()
    return circuit

@lru_cache(maxsize=32)
def DefineTemplatedVerilog(name, *args, source=None, file=None, **kwargs):
    if  source is None:
        if file is None:
            return None
        source = open(file).read()

    name = genname(name, kwargs)
    parameters = genparameters(name, kwargs)

    circuit = DefineCircuit(name, *args)
    circuit.verilog = Template(source).render(parameters=parameters)
    EndCircuit()
    return circuit

