def load_grammar(path, debug=False):
	'''
	' Loads grammars of the form:
	'	A -> y
	' 	A -> B
	' 	A -> A B b
	'
	' etc.. spaces between symbols are currently required.
	' No empty-word support yet.
	'''

	f = open(path)
	grammar = {}

	for line in f.readlines():
		rule = line.split(" -> ")
		root = rule[0]
		rule_body = rule[1].rstrip().split(' ')

		if '__root__' not in grammar:
			grammar['__root__'] = root

		if root not in grammar:
			grammar[root] = [rule_body]
		else:
			grammar[root].append(rule_body)

		if debug is True:
			print(rule_to_str(root, rule_body))

	return grammar

def rule_to_str(root, derivation, pointer=-1):
	'''
	' prints a production of the form root -> derivation
	' adds a '.' to mark the pointer position, if pointer != -1.
	'''
	if pointer == -1:
		return "%s -> %s" % (root, " ".join(derivation))
	else:
		return "%s -> %s.%s" % (root, " ".join(derivation[:pointer]), " ".join(derivation[pointer:]))