def load(path, debug=False):
	f = open(path)
	grammar = {}

	for line in f.readlines():
		rule = line.split(" -> ")

		if '__root__' not in grammar:
			grammar['__root__'] = rule[0]

		if rule[0] not in grammar:
			grammar[rule[0]] = [rule[1].strip().split(' ')]
		else:
			grammar[rule[0]].append(rule[1].strip().split(' '))

	if debug:
		print grammar

	return grammar