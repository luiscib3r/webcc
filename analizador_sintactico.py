import ply.yacc as yacc
import os
import codecs
import re
from analizador_lexico import tokens, lexer
import sys
from arbol_generador import *

# Definir precedencia (precedence)
# El orden de precedencia es de abajo hacia arriba
precedence = (
	('right', 'COMMA'),
	('right', 'ID', 'BEGIN', 'FOR'),
	('right', 'BOOLVAR', 'INTVAR', 'FLOATVAR'),
	('right', 'OP_ASSIGN'),
	('left', 'OP_NOT_EQUAL'),
	('left', 'OP_LESS', 'OP_LESS_EQUAL', 'OP_GTR', 'OP_GTR_EQUAL'),
	('left', 'OP_PLUS', 'OP_MINUS'),
	('left', 'OP_MULT', 'OP_DIVIDE'),
	('left', 'RPARENT', 'LPARENT'),
)

# Reglas de la gramatica

def p_program(p):
	'''program : declarations main_function'''
	p[0] = program(p[1], p[2])
	
def p_declarations(p):
	'''declarations : declarations constant_declaration
					| declarations vars_declaration
					| empty'''	
	try:
		p[0] = declarations(p[1], p[2])
	except IndexError:
		p[0] = empty()

def p_constant_declaration(p):
	'''constant_declaration : CONST assigment_list SEMMICOLOM'''
	p[0] = constant_declaration(p[2])
	
def p_assigment_list(p):
	'''assigment_list : ID OP_ASSIGN NUMBER
					| ID OP_ASSIGN FNUMBER
					| assigment_list COMMA assigment_list'''

	if str(p[2]) == '=':
		p[0] = assigment_list(p[1], p[3], True)
	else:
		p[0] = assigment_list(p[1], p[3], False)
	
def p_vars_declaration(p):
	'''vars_declaration : vartype id_list SEMMICOLOM'''
	p[0] = vars_declaration(p[1], p[2])
	
def p_vartype(p):
	'''vartype : BOOLVAR
			| INTVAR
			| FLOATVAR'''
	p[0] = vartype(p[1])
	
def p_id_list(p):
	'''id_list : ID
		| ID OP_ASSIGN NUMBER
		| ID OP_ASSIGN FNUMBER
		| id_list COMMA id_list'''
	try:
		if p[2] == '=':
			p[0] = id_list(p[1], p[3], True)
		else:
			p[0] = id_list(p[1], p[3], False)
	except IndexError:
		p[0] = id_simple(p[1])
	
def p_main_function(p):
	'''main_function : INTVAR MAIN LPARENT RPARENT BEGIN block END'''
	p[0] = main_function(p[6])

def p_block(p):
	'''block : block statement
			| empty'''
	try:
		p[0] = block(p[1], p[2])
	except IndexError:
		p[0] = empty()
	
def p_statement(p):
	'''statement : SEMMICOLOM'''
	p[0] = statement()
	
def p_statement_assign(p):
	'''statement : ID OP_ASSIGN expression'''
	p[0] = statement_assign(p[1], p[3])
	
def p_statement_output(p):
	'''statement : COUT output_list'''
	p[0] = statement_output(p[2])
	
def p_output_list(p):
	'''output_list : output_list OP_OUT ID
				| OP_OUT ID'''
	if str(p[2]) == '<<':
		p[0] = output_list(p[1], p[3], True)
	else:
		p[0] = output_list(p[1], p[2], False)
	
def p_statement_input(p):
	'''statement : CIN input_list'''
	p[0] = statement_input(p[2])
	
def p_input_list(p):
	'''input_list : input_list OP_IN ID
				| OP_IN ID'''
	if str(p[2]) == '>>':
		p[0] = input_list(p[1], p[3], True)
	else:
		p[0] = input_list(p[1], p[2], False)
	
def p_statement_for(p):
	'''statement : FOR ID OP_ASSIGN expression TO expression DO BEGIN block END'''
	p[0] = statement_for(p[2], p[4], p[6], p[9])
	
def p_expression_plus(p):
	'''expression : expression OP_PLUS term'''
	p[0] = expression_plus(p[1], p[3])
	
def p_expression_minus(p):
	'''expression : expression OP_MINUS term'''
	p[0] = expression_minus(p[1], p[3])
	
def p_expression_relational(p):
	'''expression : LPARENT expression op_relational expression RPARENT'''
	p[0] = expression_relational(p[2], p[3], p[4])
	
def p_op_relational(p):
	'''op_relational : OP_EQUAL
					| OP_NOT_EQUAL
					| OP_LESS_EQUAL
					| OP_GTR_EQUAL
					| OP_LESS
					| OP_GTR'''
	p[0] = op_relational(p[1])
	
def p_expression_term(p):
	'''expression : term'''
	p[0] = expression_term(p[1])
	
def p_term_mult(p):
	'''term : term OP_MULT factor'''
	p[0] = term_mult(p[1], p[3])
	
def p_term_divide(p):
	'''term : term OP_DIVIDE factor'''
	p[0] = term_divide(p[1], p[3])
	
def p_term_factor(p):
	'''term : factor'''
	p[0] = term_factor(p[1])
	
def p_factor_num(p):
	'''factor : NUMBER'''
	p[0] = factor_num(p[1])
	
def p_factor_fnum(p):
	'''factor : FNUMBER'''
	p[0] = factor_fnum(p[1])
	
def p_factor_id(p):
	'''factor : ID'''
	p[0] = factor_id(p[1])
	
def p_factor_bool(p):
	'''factor : TRUE
			| FALSE'''
	p[0] = factor_bool(p[1])
	
def p_factor_expr(p):
	'''factor : LPARENT expression RPARENT'''
	p[0] = factor_expr(p[2])
	
def p_empty(p):
	'''empty :'''
	p[0] = empty()
	
def p_error(p):
	print "error de sintaxis ", p
	print "error en la linea " + str(p.lineno)