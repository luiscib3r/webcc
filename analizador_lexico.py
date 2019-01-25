import ply.lex as lex
import re
import codecs
import os
import sys

# Lista de tokens (tokens)
tokens = [
	'ID', 'NUMBER', 'FNUMBER', 'OP_PLUS', 'OP_MINUS', 'OP_MULT', 'OP_DIVIDE',
	'OP_ASSIGN', 'OP_EQUAL', 'OP_NOT_EQUAL', 'OP_LESS', 'OP_LESS_EQUAL', 'OP_GTR', 'OP_GTR_EQUAL',
	'LPARENT', 'RPARENT', 'COMMA', 'SEMMICOLOM', 'OP_OUT', 'OP_IN',
	'BEGIN', 'END'
]

# Diccionario de palabras reservadas (reserved)
reserved = {
	'for':'FOR',
	'to':'TO',
	'do':'DO',
	'const':'CONST',
	'int':'INTVAR',
	'float':'FLOATVAR',
	'bool':'BOOLVAR',
	'true':'TRUE',
	'false':'FALSE',
	'main':'MAIN',
	'cout':'COUT',
	'cin':'CIN',
}

# Las palabras reservadas tambien forman parte de los tokens
tokens = tokens + list(reserved.values())

# Ignorar el simbolo de tabulacion
t_ignore = ' \t'

# Declaracion de expresiones regulares para el reconocimiento de los tokens
t_OP_PLUS = r'\+'
t_OP_MINUS = r'\-'
t_OP_MULT = r'\*'
t_OP_DIVIDE = r'/'
t_OP_ASSIGN = r'='
t_OP_EQUAL = r'=='
t_OP_NOT_EQUAL = r'!='
t_OP_LESS = r'<'
t_OP_LESS_EQUAL = r'<='
t_OP_GTR = r'>'
t_OP_GTR_EQUAL = r'>='
t_LPARENT = r'\('
t_RPARENT = r'\)'
t_COMMA = r','
t_SEMMICOLOM = r';'
t_BEGIN = r'{'
t_END = r'}'
t_OP_OUT = r'<<'
t_OP_IN = r'>>'

# Funciones para el reconocimiento de tokens

# Funcion con expresion regular que reconoce los identificadores y las palabras reservadas
def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'ID')
	return t


# Funcion con expresion regular que reconoce los comentarios
def t_COMMENT(t):
	r'\#.*'
	pass

# Funcion con expresion regular que reconoce los espacios en blanco
def t_SPACE(t):
	r'\ '
	pass
	
# Funcion para reconocer el salto de linea
def t_newline(t):
	r'[\r\n]'
	t.lexer.lineno += t.value.count("\n")
	

# Funcion con expresion regular que reconoce los numeros
t_NUMBER = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

t_FNUMBER = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# Funcion a ejecutar en caso de error	
def t_error(t):
	print "Caracter ilegal: '%s'" % t.value
	print "Code info: '%s'" % t
	t.lexer.skip(1)

# Funcion para buscar ficheros en el directorio con los codigos de prueba
# def findFiles(d):
	# num_file = ''
	# ret = False
	# cont = 1
	
	# files = ()
	
	# # Obtener ficheros en el directorio
	# for base, dirs, files in os.walk(d):
		# pass
    
	# for f in files:
		# print str(cont)+". " + f
		# cont = cont + 1
		
	# while ret == False:
		# num_file = raw_input('\n Numero del codigo: ')
		# for f in files:
			# if f == files[int(num_file)-1]:
				# ret = True
				# break
				
	# print " Has escogido \"%s\" \n" % files[int(num_file)-1]
	
	# return str(files[int(num_file)-1])


# # Directorio con los codigos de prueba
# source = 'D:\\Compilacion\\pyComp\\Compilador\\test\\'

# # Buscar ficheros en el directorio
# src_files = findFiles(source)

# # Seleccionar fichero
# src_file = source + src_files

# # Abrir fichero
# fp = codecs.open(src_file, "r", "utf-8")

# # Obtener el codigo del fichero y cerrar fichero
# src_code = fp.read()
# fp.close()

# Crear analizador lexico
lexer = lex.lex()
