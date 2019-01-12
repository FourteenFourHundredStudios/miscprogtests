class AnyBox(Component):

	def render(self):
		self.text = TextBox("", onClick=clicked)
		return (
			"Whats your name? " + self.text,
			"Hello, " + self.text.value + "!"
		)

	def clicked(self):
		self.text.value =