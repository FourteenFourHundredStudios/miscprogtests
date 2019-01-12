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
			return str({"type": "Expression", "left": self.left, "right":self.right})

	def __repr__(self):
		if not self.tree:
			return "(" + str(self.left) + " " + str(self.op) + " " + str(self.right) + ")"
		else:
			return str({"type": "Expression", "left": self.left, "right": self.right})


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
		while True:
			value = ""
			if not self.moreTokens():
				break
			token = self.peekToken()
			if type(token) == int:
				value = {"type": "Expression", "value": self.parseMath(0)}
			elif type(token) == Identifier:
				value = self.parseIdentifier()
			elif type(token) == Container:
				value = self.parseContainer()
			if ast is None:
				ast = value
			else:

				temp = copy.copy(ast)
				value["value"] = copy.copy(temp)
				ast = value
				self.ast = ast

		return ast


	def parseIdentifier(self):
		name = self.nextToken().value
		if self.moreTokens() and type(self.peekToken()) is Identifier:
			return {"type": "Data", "name": name}
		else:
			return {"type": "Attribute", "name": name, "value": None}

	def parseContainer(self):
		if self.ast["type"] == "Attribute" or self.ast["type"] == "Data":
			return {"type": "Function", "args": Parser(self.nextToken().value).parse(), "value": None}
		else:
			print("SYNTAX ERROR")

	def parseMath(self, mode):
		results = []
		while True:
			if not self.moreTokens():
				break

			token = self.nextToken()

			if token in delims:
				break

			elif token in ops2 and mode == 0:
				val = Expression(results.pop(), token, self.nextToken(), True)
				results.append(val)

			elif token in ops1 and mode == 1:
				val = Expression(results.pop(), token, self.nextToken(), True)
				results.append(val)

			else:
				results.append(token)

		if mode == 0:
			return Parser(results).parseMath(1)[0]

		return results

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


tokens = [
	Identifier("system"),
	Identifier("print"),
	Container(get_symbols("5 * 2 + 5"))
]

#print(tokens)
print(str(Parser(tokens).parse()).replace("'",'"'))