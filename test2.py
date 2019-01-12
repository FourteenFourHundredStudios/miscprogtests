import dis as dis
#import new



btc = bytes([dis.opmap['LOAD_FAST'], 1,  dis.opmap['RETURN_VALUE']])


def c(): pass

code = type(modify.__code__)
function = type(modify)
ocode = globals.__code__


new_modify = function(
    code(ocode.co_argcount, ocode.co_kwonlyargcount, ocode.co_nlocals, ocode.co_stacksize,
          ocode.co_flags, btc,
          ocode.co_consts, ocode.co_names, ocode.co_varnames, ocode.co_filename,
          'new_modify', ocode.co_firstlineno, ocode.co_lnotab, ocode.co_freevars,
         ocode.co_cellvars),
    modify.__globals__, 'new_modify', modify.__defaults__, modify.__closure__)

print(new_modify())