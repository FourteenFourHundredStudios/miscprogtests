
# system.print(thing.val1 + thing.find().val2)

token_hard = [
	{"type": "keyword", "value": "system"},
	{"type": "keyword", "value": "print"},
	{"type": "container", "value": [
		{"type": "keyword", "value": "thing"},
		{"type": "keyword", "value": "val1"},
		{"type": "delimiter", "value": "+"},
		{"type": "keyword", "value": "thing"},
		{"type": "keyword", "value": "find"},
		{"type": "container", "value": []},
		{"type": "keyword", "value": "val2"},
	]}
]

# system.print(var)
tokens_easy = [
	{"type": "keyword", "value": "system"},
	{"type": "keyword", "value": "print"},
	{"type": "container", "value": [
		{"type": "keyword", "value": "var"},
	]},
]


tokens_op = [
	{"type": "number", "value": "5"},
	{"type": "operator", "value": "+"},
	{"type": "number", "value": "6"},
	{"type": "operator", "value": "*"},
	{"type": "number", "value": "7"},
]

class Parse:

	def __init__(self, tokens):
		self.tokens = tokens
		self.skipNext = False

	def keyword(self, index):
		keywords = {"type": "var", "name": self.tokens[index]["value"], "member": {}}
		return keywords

	def func(self, index):
		val = {"type": "function", "member": {}, "args": self.tokens[index]["value"]}
		return val

	def number(self, index):
		return self.tokens[index]

	def op(self, index):
		val = {"type": "binary", "left": self.tokens[index-1], "op": self.tokens[index], "right": self.tokens[index+1]}

		return val

	def branch(self, ast, token):

		newAst = token.copy()

		if ast["type"] == "var":
			newAst["member"] = ast
		elif ast["type"] == "function":
			newAst["member"] = ast
		elif ast["type"] == "binary":
			newAst["left"] = ast

		return newAst

	def parse(self):
		ast = {"type": "empty"}
		for i in range(0, len(self.tokens)):
			if self.skipNext:
				self.skipNext = False
				continue
			token = self.tokens[i]

			if token["type"] == "number":
				continue

			token_type = {
				"keyword": self.keyword,
				"container": self.func,
				"number": self.number,
				"operator": self.op
			}
			parsedToken = token_type[token["type"]](i)

			ast = self.branch(ast, parsedToken)

		return ast

	def parse2(self):
		ast = {"type": "empty"}
		for i in range(len(self.tokens)-1, 0, -1):
			if self.skipNext:
				self.skipNext = False
				continue
			token = self.tokens[i]

			if token["type"] == "number":
				continue

			token_type = {
				"keyword": self.keyword,
				"container": self.func,
				"number": self.number,
				"operator": self.op
			}
			parsedToken = token_type[token["type"]](i)

			ast = self.branch(ast, parsedToken)

		return ast


print(Parse(tokens_easy).parse2())