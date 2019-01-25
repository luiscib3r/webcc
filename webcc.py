from analizador_sintactico import *

# Funcion para buscar ficheros en el directorio con los codigos de prueba
def findFiles(d):
	num_file = ''
	ret = False
	cont = 1
	
	files = ()
	
	# Obtener ficheros en el directorio
	for base, dirs, files in os.walk(d):
		pass
    
	for f in files:
		print str(cont)+". " + f
		cont = cont + 1
		
	while ret == False:
		num_file = raw_input('\n Numero del codigo: ')
		for f in files:
			if f == files[int(num_file)-1]:
				ret = True
				break
				
	print " Has escogido \"%s\" \n" % files[int(num_file)-1]
	
	return str(files[int(num_file)-1])

# Directorio con los codigos de prueba
path_dir = sys.argv[0]

n = len(path_dir) - 1

while path_dir[n] != '\\':
	n -= 1

test_dir = path_dir[0:n] + '\\test\\'

# Buscar ficheros en el directorio
src_files = findFiles(test_dir)

# Seleccionar fichero
src_file = test_dir + src_files

# Abrir fichero
fp = codecs.open(src_file, "r", "utf-8")

# Obtener el codigo del fichero y cerrar fichero
src_code = fp.read()
fp.close()

parser = yacc.yacc() # Creacion del parser

try: # Analizar el codigo fuente
	result = parser.parse(src_code)

	# generar archivo
	generate_file = open('WebCC.html', 'w')
	generate_file.write(result.generate())
	generate_file.close()

	# mostrar informacion del analisis
	print "Tipo		IDs"
	for tipo in id_types:
		print tipo + '\t\t' + str(id_types[tipo])

	print "\nCONSTANTES: "
	for c in const_values:
		print c + '\t:\t' + const_values[c] 

	print "\nListado de identificadores"
	print vars_ids

	print "\nArchivo WebCC.html generado correctamente presione ENTER para continuar"

except Exception as inst:
	print "Se han detectado errores de sintaxis en el codigo fuente: "
	print(inst)

raw_input()
