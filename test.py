

import dis as dis


default = 0
def modify():
    modified = default + 1
    print(modified)  # replace with OS call, I can't see the output



altered_bytecode = modify.__code__.co_code[:8] + bytes([dis.opmap['LOAD_CONST'], 10,  dis.opmap['RETURN_VALUE']])

print(modify.__code__.co_code[:8])


code = type(modify.__code__)

print(type(modify.__code__))

function = type(modify)
ocode = modify.__code__

print( ocode.co_stacksize)

new_modify = function(
    code(ocode.co_argcount, ocode.co_kwonlyargcount, ocode.co_nlocals, ocode.co_stacksize,
          ocode.co_flags, altered_bytecode,
          ocode.co_consts, ocode.co_names, ocode.co_varnames, ocode.co_filename,
          'new_modify', ocode.co_firstlineno, ocode.co_lnotab, ocode.co_freevars,
         ocode.co_cellvars),
    modify.__globals__, 'new_modify', modify.__defaults__, modify.__closure__)

#print(new_modify())


def hi():
    return 7


print("fewfewfewf",modify.__code__.co_stacksize)

dis.dis(hi)


#print(f)