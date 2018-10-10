
ops1 = ["+", "-"]
ops2 = ["*", "/"]

tokens = ["5", "*", "3", "+", "4"]



def parse2(index, maxPos):
	left = None
	op = None
	right = None

	if index+1 == len(tokens):
		return tokens[index]

	#return {"left": tokens[index], "op": tokens[index+1], "right": parse(index+2)}


	for i in range(index, len(tokens)):

		t = tokens[i]

		if t in ops2:
			left = tokens[i - 1]
			op = tokens[i]
			right = parse(i + 1)
			return {"left": left, "op": op, "right": right}


	#return {"left": left, op: op, "right": right}


def parse(index, maxPos):

	left = None
	op = None
	right = None

	#tokens.reverse()

	if index+1 == len(tokens) :
		return tokens[index]

	for i in range(index, len(tokens)):

		if i == maxPos:
			return tokens[i+1]

		t = tokens[i]

		if t in ops1:

			"""
			left = tokens[i-1]
			op = tokens[i]
			right = parse(i+1, i)
			return {"left": left, "op": op, "right": right}
			"""


			value = parse(i+1, i)

			l=None

			if type(value) == dict:
				l = value["right"]
				a = {"left": l, "op": t, "right": tokens[i - 1]}

				value["right"] = a
			else:
				l = value



			return value




		elif t in ops2:
			x = parse(i + 1, len(tokens))

			if type(x) is int:
				return {"left": tokens[i - 1], "op": tokens[i], "right": x}

			f = {"left": tokens[i - 1], "op": tokens[i], "right": x["left"]}

			left = x["right"]
			op = x["op"]


			return {"left": f, "op": op, "right": left}




	#return {"left": left, "op":op, "right":right}


def solve(val):
	left = val["left"]
	right = val["right"]

	if type(left) == dict:
		left=solve(left)

	if type(right) == dict:
		right=solve(right)

	if type(left) == str:
		left = int(left)

	if type(right) == str:
		right = int(right)

	if val["op"] == "+":
		return left + right
	elif val["op"] == "-":
		return left - right
	elif val["op"] == "*":
		return left * right
	elif val["op"] == "/":
		return left / right







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


"""
tokens = get_symbols("3 + 10 * 2 / 2 * 5 + 2 * 35 + 60 + 100 / 4 + 60 / 3 + 55 * 2 + 50 + 10 * 300 + 44")
print(parse(0, len(tokens)))
print(solve(parse(0, len(tokens))))
print()
"""

def test(strs):
	global tokens
	a = int(eval(strs))
	tokens = get_symbols(strs)
	b = solve(parse(0, len(tokens)))

	if a != b:
		print(strs)
		print(parse(0, len(tokens)))
		pass

	return a == b


#print(test("5 + 3"))
#print(test("5 * 3"))
#print(test("5 * 3 + 4"))
#print(test("5 + 3 * 4"))
#print(test("5 + 3 * 4 - 10"))
#print(test("5 + 3 * 4 - 10"))
print(test("5 - 3 - 6"))


#5 + ((3 + (4 - (10 + 5))