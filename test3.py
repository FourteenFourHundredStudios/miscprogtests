
import dis
from contextlib import suppress

def nvm(fn):


	btc = bytes([dis.opmap['LOAD_CONST'], 1, dis.opmap['RETURN_VALUE']])

	code = type(fn.__code__)
	function = type(fn)
	ocode = fn.__code__

	#print(ocode.co_consts)

	new_fn = function(
		code(ocode.co_argcount, ocode.co_kwonlyargcount, ocode.co_nlocals, 1,
		     ocode.co_flags, btc,
		     (None, "nvm"), ocode.co_names, ocode.co_varnames, ocode.co_filename,
		     'fn', ocode.co_firstlineno, ocode.co_lnotab, ocode.co_freevars,
		     ocode.co_cellvars),
		fn.__globals__, 'fn', fn.__defaults__, fn.__closure__)


	return new_fn



if __name__ == '__main__':

	#@nvm
	def hi():

		with html():
			with body(background="ff"):
				pass


			pass



		#return 4



	dis.dis(hi)


