from libtbx.program_template import program_template

class Program(program_template):
	datatypes = ['model']

	def validate(self): pass
	def run(self): print("hello")

	