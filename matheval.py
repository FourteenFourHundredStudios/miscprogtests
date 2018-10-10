ops1 = ["+", "-"]
ops2 = ["*", "/"]

class Expression(object):

	def __init__(self, left, op, right):
		self.left = left
		self.right = right
		self.op = op

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
		return "(" + str(self.left) + " " + str(self.op) + " " + str(self.right) + ")"

	def __repr__(self):
		return "(" + str(self.left) + " " + str(self.op) + " " + str(self.right) + ")"


def get_symbols(string):
	negative = False
	part = ""
	symbols = []
	for i in string:
		if i is " ":
			continue
		if i not in ops1 and i not in ops2:
			part += i
		else:
			if part == "":
				negative = True
			else:
				if negative:
					part = "-"+part
					negative = False
				symbols.append(int(part))
				symbols.append(i)
				part = ""
	if negative:
		part = "-" + part
		negative = False
	symbols.append(int(part))
	return symbols


def solve(tokens, mode=0):

	if len(tokens) == 1:
		return tokens[0]

	rightTokens = []

	for i in range(len(tokens)-1, 0, -1):

		if tokens[i] in ops1 or tokens[i] in ops2:
			leftTokens = []
			for j in range(0, i):
				leftTokens.append(tokens[j])

			if mode == 1:
				return Expression(solve(leftTokens, 1), tokens[i], solve(rightTokens, 1))

			if tokens[i] in ops1 and mode == 0:
				return Expression(solve(leftTokens), tokens[i], solve(rightTokens))

		rightTokens.insert(0, tokens[i])

	return solve(tokens, 1)


def to_tree(exp):
	tokens = get_symbols(exp)
	return solve(tokens, 0)



def check(val):
	a = to_tree(val).eval()
	b = eval(val)

	return a == b


f = "3 + 10 * 2 / 2 * 5 + 2 * 35 + 60 + 100 / 60 + 4 * 5 - 4 + 60 / 3 + 55 * 2 + 50 + 10 * 300 + 44 * 30 - 40"
print(to_tree(f))
print(check(f))


