source = " "

id_types = {
	'int': [],
	'float': [],
	'bool': [],
}
const_values = {}
vars_ids = []
type_in_proccess = ''
op_relational_in_proccess = False

class Nodo():
	pass

class program(Nodo):
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2
		
	def generate(self):
		global source
		source += '''
		<!DOCTYPE html>
		<html>
		<head>
			<title>WebCC Program</title>
			<script>
			var consola;
		'''
		self.s1.generate()
		self.s2.generate()
		source += '''
			</script>
			<style>
				body {
    				margin: 0;
    				padding: 0;
				}

				html, body {
    				height: 100%;
    				min-height: 100%;
				}

				.program {
    				font-family: 'Bellota-LightItalic', sans-serif;
    				position: relative;
    				margin-right: auto;
    				margin-left: auto;
    				top: 7%;
    				width: 80%;
    				background-color: #ffffff;
    				border: 1px solid #EDEDED;
    				border-radius: 7px;
    				padding: 10px;
    				opacity: 0.98;
				}

				.p_head {
    				font-family: 'Bellota-LightItalic', sans-serif;
    				padding: 10px;
    				background-color: #3498db;
    				color: #fff;
    				text-align: center;
    				border-top-left-radius: 7px;
    				border-top-right-radius: 7px;
				}

				.console {
    				font-size: 0.9em;
    				color: #dcddde;
    				background: #21272b;
    				font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
    				font-weight: 600;
    				position: relative;
    				border: none;
    				max-width: 100%;
    				overflow: auto;
    				margin: 0 0 11px;
				}
			</style>
		</head>
		<body>
		<div class="program">
			<div class="p_head">
				WebCC Program
			</div>
			<div id="consola" class="console">
			</div>
		</div>
		</body>
		</html>
		'''
		
		return source

class declarations(Nodo):
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2
		
	def generate(self):
		global source 
		self.s1.generate()
		self.s2.generate()

class constant_declaration(Nodo):
	def __init__(self, s1):
		self.s1 = s1
		
	def generate(self):
		global source
		self.s1.generate()

class assigment_list(Nodo):
	def __init__(self, s1, s2, ws):
		self.s1 = s1
		self.s2 = s2
		self.ws = ws
		
	def generate(self):
		global source
		global id_types
		global const_values 
		if self.ws:
			if vars_ids.count(str(self.s1)) == 0:
				const_values[str(self.s1)] = str(self.s2)
				vars_ids.append(str(self.s1))
				if str(self.s2).count('.') == 1:
					id_types['float'].append(str(self.s1))
				else:
					id_types['int'].append(str(self.s1))
			else:
				raise Exception('ERROR: Identificador ' + str(self.s1) + ' ya fue registrado')
		else:
			self.s1.generate()
			self.s2.generate()
			source += ';'

class vars_declaration(Nodo):
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2

	def generate(self):
		global source 
		self.s1.generate()
		self.s2.generate()
		source += ';'

class vartype(Nodo):
	def __init__(self, type):
		self.type = type
		
	def generate(self):
		global source
		global type_in_proccess
		type_in_proccess = str(self.type) 
		source += '\nvar' + ' '

class id_list(Nodo):
	def __init__(self, s1, s2, ws):
		self.s1 = s1
		self.s2 = s2
		self.ws = ws
		
	def generate(self):
		global source
		global id_types
		global type_in_proccess
		global vars_ids
		if self.ws:
			if vars_ids.count(str(self.s1)) == 0:
				if type_in_proccess == 'int':
					if str(self.s2).count('.') == 0 and str(self.s2) != 'true' and str(self.s2) != 'false':
						id_types['int'].append(str(self.s1))
						vars_ids.append(str(self.s1))
						source += str(self.s1) + ' = ' + str(self.s2)			
					else:
						raise Exception('ERROR: Asignacion invalida a variable tipo int')
				elif type_in_proccess == 'float':
					if str(self.s2) != 'true' and str(self.s2) != 'false':
						id_types['float'].append(str(self.s1))
						vars_ids.append(str(self.s1))
						source += str(self.s1) + ' = ' + str(self.s2)			
					else:
						raise Exception('ERROR: Asignacion invalida a variable tipo float')
				elif type_in_proccess == 'bool':
					if str(self.s2) == 'true' or str(self.s2) != 'false':
						id_types['bool'].append(str(self.s1))
						vars_ids.append(str(self.s1))
						source += str(self.s1) + ' = ' + str(self.s2)			
					else:
						raise Exception('ERROR: Asignacion invalida a variable tipo bool')
			else:
				raise Exception('ERROR: Identificador ' + str(self.s1) + ' ya fue registrado')
		else:
			self.s1.generate()
			source += ', '
			self.s2.generate()

class id_simple(Nodo):
	def __init__(self, s1):
		self.s1 = s1

	def generate(self):
		global source
		global id_types
		global vars_ids
		global type_in_proccess

		if vars_ids.count(str(self.s1)) == 0:
			id_types[type_in_proccess].append(str(self.s1))
			vars_ids.append(str(self.s1))
			source += str(self.s1)
		else:
			raise Exception('ERROR: Identificador ' + str(self.s1) + ' ya fue registrado')

class main_function(Nodo):
	def __init__(self, block):
		self.block = block
		
	def generate(self):
		global source 
		source += '\nwindow.onload = function(){\n  consola = document.getElementById("consola");\n'
		self.block.generate()
		source += '\n};'

class block(Nodo):
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2
		
	def generate(self):
		global source 
		self.s1.generate()
		self.s2.generate()

class statement(Nodo):
	def __init__(self):
		pass
		
	def generate(self):
		global source 
		source += ';\n'

class statement_assign(Nodo):
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2
		
	def generate(self):
		global source
		global vars_ids
		global const_values
		global id_types
		global type_in_proccess
		if vars_ids.count(str(self.s1)) == 1:
			if not str(self.s1) in const_values:
				if id_types['int'].count(str(self.s1)) == 1:
					type_in_proccess = 'int'
				elif id_types['float'].count(str(self.s1)) == 1:
					type_in_proccess = 'float'
				elif id_types['bool'].count(str(self.s1)) == 1:
					type_in_proccess = 'bool'

				source += str(self.s1) + ' = '
				self.s2.generate()
			else:
				raise Exception('ERROR: ' + str(self.s1) + ' es una constante y no admite asignacion')
		else:
			raise Exception('ERROR: identificador ' + str(self.s1) + ' no fue declarado')

class statement_output(Nodo):
	def __init__(self, s1):
		self.s1 = s1
		
	def generate(self):
		global source 
		self.s1.generate()

class output_list(Nodo):
	def __init__(self, s1, s2, cont):
		self.s1 = s1
		self.s2 = s2
		self.cont = cont

	def generate(self):
		global source
		global vars_ids
		global const_values
		
		if vars_ids.count(str(self.s2)) == 1:
			if self.cont:
				self.s1.generate()

				if not str(self.s2) in const_values:
					source += '\nconsola.innerHTML += "'+ str(self.s2) + ': " + ' + str(self.s2) + ' + "<br>"'
				else:
					source += '\nconsola.innerHTML += "' + str(self.s2) + ': " + ' + const_values[str(self.s2)] + ' + "<br>"'
			else:
				if not str(self.s2) in const_values:
					source += '\nconsola.innerHTML += "'+ str(self.s2) + ': " + ' + str(self.s2) + ' + "<br>"'
				else:
					source += '\ndocument.innerHTML += "' + str(self.s2) + ': " + ' + const_values[str(self.s2)] + ' + "<br>"'
		else:
			raise Exception('ERROR: identificador ' + str(self.s2) + ' no fue declarado')


class statement_input(Nodo):
	def __init__(self, s1):
		self.s1 = s1
		
	def generate(self):
		global source 
		self.s1.generate()

class input_list(Nodo):
	def __init__(self, s1, s2, cont):
		self.s1 = s1
		self.s2 = s2
		self.cont = cont
		
	def generate(self):
		global source
		global vars_ids
		global const_values
		global id_types

		if vars_ids.count(str(self.s2)) == 1:
			if self.cont:
				self.s1.generate()

				if not str(self.s2) in const_values:
					if id_types['int'].count(str(self.s2)) == 1:
						source += '\n' + str(self.s2) + ' = parseInt(prompt("' + str(self.s2) + '"));'
					else:
						source += '\n' + str(self.s2) + ' = Number(prompt("' + str(self.s2) + '"));'
				else:
					raise Exception('ERROR: ' + str(self.s2) + ' es una constante y no admite operaciones de entrada')
			else:
				if not str(self.s2) in const_values:
					if id_types['int'].count(str(self.s2)) == 1:
						source += '\n' + str(self.s2) + ' = parseInt(prompt("' + str(self.s2) + '"));'
					else:
						source += '\n' + str(self.s2) + ' = Number(prompt("' + str(self.s2) + '"));'
				else:
					raise Exception('ERROR: ' + str(self.s2) + ' es una constante y no admite operaciones de entrada')
		else:
			raise Exception('ERROR: identificador ' + str(self.s2) + ' no fue declarado')

class statement_for(Nodo):
	def __init__(self, varctr, expr1, expr2, stm):
		self.varctr = varctr
		self.expr1 = expr1
		self.expr2 = expr2
		self.stm = stm
		
	def generate(self):
		global source 
		global vars_ids
		global const_values

		if vars_ids.count(str(self.varctr)) == 1:
			if not str(self.varctr) in const_values:
				if id_types['int'].count(str(self.varctr)) == 1:
					type_in_proccess = 'int'
				elif id_types['float'].count(str(self.varctr)) == 1:
					type_in_proccess = 'float'
				elif id_types['bool'].count(str(self.varctr)) == 1:
					type_in_proccess = 'bool'

				source += str(self.varctr) + ' = '
				self.expr1.generate()
				source += '\nwhile(' + self.varctr + ' != '
				self.expr2.generate()
				source += ') {\n'
				self.stm.generate()
				source += '\n}'

			else:
				raise Exception('ERROR: ' + str(self.varctr) + ' es una constante y no admite asignacion')
		else:
			raise Exception('ERROR: identificador ' + str(self.varctr) + ' no fue declarado')

class expression_plus(Nodo):
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2
		
	def generate(self):
		global source 
		self.s1.generate()
		source += ' + '
		self.s2.generate()

class expression_minus(Nodo):
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2
		
	def generate(self):
		global source 
		self.s1.generate()
		source += ' - '
		self.s2.generate()

class expression_relational(Nodo):
	def __init__(self, s1, s2, s3):
		self.s1 = s1
		self.s2 = s2
		self.s3 = s3
		
	def generate(self):
		global source
		global type_in_proccess
		global op_relational_in_proccess
		if type_in_proccess == 'bool':
			source += '('
			op_relational_in_proccess = True
			self.s1.generate()
			self.s2.generate()
			self.s3.generate()
			op_relational_in_proccess = False
			source += ');\n'
		else:
			raise Exception("ERROR: Conflicto en asignacion para expression relational")

class op_relational(Nodo):
	def __init__(self, name):
		self.name = name
		
	def generate(self):
		global source 
		source += str(self.name)

class expression_term(Nodo):
	def __init__(self, s1):
		self.s1 = s1
		
	def generate(self):
		global source 
		self.s1.generate()

class term_mult(Nodo):
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2
		
	def generate(self):
		global source
		self.s1.generate()
		source += ' * '
		self.s2.generate()

class term_divide(Nodo):
	def __init__(self, s1, s2):
		self.s1 = s1
		self.s2 = s2
		
	def generate(self):
		global source
		self.s1.generate()
		source += ' / '
		self.s2.generate()

class term_factor(Nodo):
	def __init__(self, s1):
		self.s1 = s1
		
	def generate(self):
		global source 
		self.s1.generate()

class factor_num(Nodo):
	def __init__(self, s1):
		self.s1 = s1
		
	def generate(self):
		global source 
		source += str(self.s1)

class factor_fnum(Nodo):
	def __init__(self, s1):
		self.s1 = s1
		
	def generate(self):
		global source
		global type_in_proccess

		if type_in_proccess == 'float': 
			source += str(self.s1)
		else:
			raise Exception('ERROR: identificador ' + str(self.s1) + ' no cumple con el tipo de asignacion')

class factor_id(Nodo):
	def __init__(self, s1):
		self.s1 = s1
		
	def generate(self):
		global source
		global const_values
		global vars_ids
		
		if vars_ids.count(str(self.s1)) == 1:
			if not str(self.s1) in const_values:
				if type_in_proccess == 'int' and id_types['float'].count(str(self.s1)) != 1 and id_types['bool'].count(str(self.s1)) != 1:
					source += str(self.s1)
				elif type_in_proccess == 'float' and id_types['bool'].count(str(self.s1)) != 1:
					source += str(self.s1)
				elif type_in_proccess == 'bool' and id_types['bool'].count(str(self.s1)) == 1:
					source += str(self.s1)
				elif op_relational_in_proccess:
					source += str(self.s1)
				else:
					raise Exception('ERROR: identificador ' + str(self.s1) + ' no cumple con el tipo de asignacion')
			else:
				source += const_values[str(self.s1)]
		else:
			raise Exception('ERROR: identificador ' + str(self.s1) + ' no fue declarado')

class factor_bool(Nodo):
	def __init__(self, name):
		self.name = name
		
	def generate(self):
		global source 

		if type_in_proccess == 'bool':
			source += str(self.name)
		else:
			raise Exception("ERROR: Conflicto en asignacion para expression relational")

class factor_expr(Nodo):
	def __init__(self, s1):
		self.s1 = s1
		
	def generate(self):
		global source
		source += '('		 
		self.s1.generate()
		source += ')'

class empty(Nodo):
	def __init__(self):
		pass
		
	def generate(self):
		global source 
		pass
