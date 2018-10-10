
ops = ["+", "-", "*", "/"]


class Expression(object):

	def __init__(self, left, op, right):
		if type(left) is Expression:
			left = left.eval()
		if type(right) is Expression:
			right = right.eval()

		self.left = float(left)
		self.right = float(right)
		self.op = op

	def eval(self):
		if self.op == "+":
			return self.left + self.right
		elif self.op == "-":
			return self.left - self.right
		elif self.op == "*":
			return self.left * self.right
		elif self.op == "/":
			return self.left / self.right

	def __str__(self):
		return "(" + self.left + "," + self.right + ")"

	def __repr__(self):
		return "(" + str(self.left) + " " + self.op + " " + str(self.right) + ")"


def get_symbols(string):
	negative = False
	part = ""
	symbols = []
	for i in string:
		if i is " ":
			continue
		if i not in ops:
			part += i
		else:
			if part == "":
				negative = True
			else:
				if negative:
					part = "-"+part
					negative = False
				symbols.append(part)
				symbols.append(i)
				part = ""
	if negative:
		part = "-" + part
		negative = False
	symbols.append(part)
	return symbols


def remove_none(lst):
	f_list = []
	for i in lst:
		if i is not None:
			f_list.append(i)
	return f_list


def simplify(symbols, n_ops):
	symbols = remove_none(symbols)
	if len(symbols) == 3:
		return symbols
	for i in range(0, len(symbols)):
		symbol = symbols[i]
		if symbol in n_ops:
			left = symbols[i - 1]
			right = symbols[i + 1]
			expression = Expression(left, right, symbol)
			symbols[i - 1] = None
			symbols[i + 1] = None
			symbols[i] = None
			symbols.insert(i, expression)
			return simplify(symbols, n_ops)
	return symbols


def math(string):
	symbols = get_symbols(string)
	symbols = simplify(symbols, ["*", "/"])
	symbols = simplify(symbols, ["+", "-"])
	return Expression(symbols[0], symbols[2], symbols[1]).eval()


print(math("-3 + 10 * 2 / 2 * 5 - 2 * 35 + 60 + 100 / 4 + 60 / 3 + 55 * 2 -50 + 10 * 300 + -44"))

#adef f():
#	return "hi"+6

#print(f())


#print(math("3+50*200+-50*300"))

