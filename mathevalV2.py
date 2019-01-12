import copy

ops1 = ["+", "-"]
ops2 = ["*", "/"]
delims = [","]

class KeyWord(object):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return self.value


class Literal(object):
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return str(self.value)


class Identifier(object):
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return str(self.value)


class Container(object):
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		return "("+str(self.value)+")"


class Expression(object):
	def __init__(self, left, op, right, tree = False):
		self.left = left
		self.right = right
		self.op = op
		self.tree = tree
		self.type = "Expression"

	def eval(self):

		if type(self.left) is Expression:
			self.left = self.left.eval()
		if type(self.right) is Expression:
			self.right = self.right.eval()

		self.left = float(self.left)
		self.right = float(self.right)

		if self.op == "+":
			return self.left + self.right
		elif self.op == "-":
			return self.left - self.right
		elif self.op == "*":
			return self.left * self.right
		elif self.op == "/":
			return self.left / self.right

	def __str__(self):
		if not self.tree:
			return "(" + str(self.left) + " " + str(self.op) + " " + str(self.right) + ")"
		else:
			return str({"type": "Expression", "left": self.left, "op":self.op,"right":self.right})

	def __repr__(self):
		if not self.tree:
			return "(" + str(self.left) + " " + str(self.op) + " " + str(self.right) + ")"
		else:
			return str({"type": "Expression", "left": self.left, "op":self.op,"right": self.right})


def get_symbols(string):
	negative = False
	part = ""
	symbols = []
	for i in string:
		if i is " ":
			continue

		if i in delims:

			if part.isdigit():
				symbols.append(int(part))
			else:
				symbols.append(str(part))
			part = ""
			symbols.append(i)

		elif i not in ops1 and i not in ops2 :
			part += i
		else:
			if part == "":
				negative = True
			else:
				if negative:
					part = "-"+part
					negative = False
				if part.isdigit():
					symbols.append(int(part))
				else:
					symbols.append(str(part))
				symbols.append(i)
				part = ""
	if negative:
		part = "-" + part
		negative = False


	if part.isdigit():
		symbols.append(int(part))
	else:
		symbols.append(str(part))

	return symbols



class Parser():

	def __init__(self, tokens):
		self.tokens = tokens
		self.ast = None

	def parse(self):
		ast = None

		collection = None

		while True:
			value = ""
			if not self.moreTokens():
				break
			token = self.peekToken()

			if type(token) == int:
				#value = self.parseMath(0)
				value = self.parseMathV2(0)

			elif type(token) == Identifier:
				value = self.parseIdentifier()
			elif type(token) == Container:
				value = self.parseContainer()
			elif token in delims:
				self.nextToken()
				if collection is None:
					collection = [ast]
				else:
					collection.append(ast)
				ast = None
				continue

			if ast is None:
				ast = value
			else:
				temp = copy.copy(ast)
				value["value"] = copy.copy(temp)
				ast = value
				self.ast = ast

		if collection is not None:
			collection.append(ast)
			return collection

		return ast


	def parseIdentifier(self):
		name = self.nextToken().value
		if (self.moreTokens() and type(self.peekToken()) is Identifier) or ( self.moreTokens()):
			return {"type": "Data", "name": name}
		else:
			return {"type": "Attribute", "name": name, "value": None}

	def parseContainer(self):
		if self.ast["type"] == "Attribute" or self.ast["type"] == "Data":
			return {"type": "Function", "args": Parser(self.nextToken().value).parse(), "value": None}
		else:
			print("SYNTAX ERROR")



	def parseMathV2(self, mode):
		results = []
		while True:
			if not self.moreTokens() or self.peekToken() in delims:
				break

			token = self.nextToken()

			if (token in ops2 and mode == 0) or (token in ops1 and mode == 1):
				left = results.pop()
				op = token
				right = self.nextToken()
				if type(left) is not Expression or int:
					left = Parser([left]).parse()
				if type(right) is not Expression or int:
					right = Parser([right]).parse()

				results.append(Expression(left, op, right, True))
			else:
				results.append(token)

		if mode == 0:
			return Parser(results).parseMathV2(1)

		return results[0]


	def nextToken(self):
		return self.tokens.pop(0)

	def peekToken(self):
		return self.tokens[0]

	def moreTokens(self):
		return len(self.tokens) > 0

def to_tree(exp):
	tokens = get_symbols(exp)

	return Parser(tokens).parse()


def check(val):
	a = to_tree(val).eval()
	b = eval(val)

	return a == b


#f = "3 * 10 * 2 / 2 * 5 + 2 * 35 + 60 + 100 / 60 + 4 * 5 - 4 + 60 / 3 + 55 * 2 + 50 + 10 * 300 + 44 * 30 - 40"
#print(check(f))


#get_symbols("5 * 2 + 7")

"""
tokens = [
	Identifier("system"),
	Identifier("print"),
	Container([5,"*",2, "+", 6, "," ,Identifier("hello"), Identifier("world")])
]
"""

"""
tokens = [
	5, "+", 5, "*", 2, "-", 3 ,",",Identifier("dqwwq")
]
"""

tokens = [
	Identifier("money"), Identifier("dqwwq")
]

"""
tokens = [
	5, "+", 3, "*", 2, ",", 3
]
"""


#print(tokens)
print(str(Parser(tokens).parse()).replace("'",'"'))