def load_grammar(path):
	f = open(path)
	grammar = {}

	for line in f.readlines():
		rule = line.split(" -> ")

		if '__root__' not in grammar:
			grammar['__root__'] = rule[0]

		if rule[0] not in grammar:
			grammar[rule[0]] = [rule[1].strip()]
		else:
			grammar[rule[0]].append(rule[1].strip())

	return grammar

def peek(s, i, fallback):
	if i < len(s):
		return s[i]

	return fallback

def insert(s, c, i):
	return s[:i]+c+s[i:]

def earley(w, G, k=1):
	n = len(w)

	w += k*'#'

	# sets of states q=(P, i, l, s)
	sets = [[] for x in range(n+2)]
	sets[0].append( (('S', G['__root__']+'#'*k), 0, '#'*k, 0) )

	s_i = 0
	while True:
		current_set = sets[s_i]
		print("\n\nS(%s):" % s_i)
		if current_set == []:
		#	print("    !!!Set is empty. w not in L(G)!!!")
			return False

		# predictor step
		# check for states with noneterminals

		for q in current_set:
			P = q[0]
			i = q[1]
			l = q[2]
			s = q[3]
			
			print("    %s -> %s (%s)" % (P[0], P[1], s))

			if i == len(P[1]):
				#print("attempting to complete %s -> %s" % P)
				if l == w[s_i:s_i+k]:
					#print("lookahead %s matches w[i] %s" % (l, w[s_i:s_i+k]))
					for old_q in sets[s]:
					#	print("checking %s if %s matches %s" % (s, P[0], old_q[0][1]))
						if P[0] == peek(old_q[0][1], old_q[1], old_q[2]):
							q_new = (old_q[0], old_q[1]+1, old_q[2], old_q[3])
							print("         %s -> %s (%s)" % (q_new[0][0], insert(q_new[0][1], '.',q_new[1]), q_new[3]))
							current_set.append(q_new)
				#else:
				#	print("lookahead %s doesn't match w[i] %s" % (l, w[s_i:s_i+k]))
			else:
				P_i = peek(P[1], i, l)
				if P_i in G.keys(): # nonterminal next to dot -> predictor applicable
					for rule_body in G[P_i]:
						q_new = ((P_i, rule_body), 0, peek(P[1], i+k, l), s_i)
						if q_new not in current_set:
							print("         %s -> %s (%s) [P]" % (q_new[0][0], q_new[0][1], q_new[3]))
							current_set.append(q_new)
				elif (P_i == peek(w, s_i, '#')) or (P_i == '#'): # terminal next to dot -> scanner applicable
					q_new = (P, i+1, l, s)
					print("         [SCANNER] %s -> %s (%s)" % (q_new[0][0], q_new[0][1], q_new[3]))
					sets[s_i+1].append(q_new)
		
		#print((('S', G['__root__']+'#'*k), 2, '#'*k, 0))
		#print(current_set[0])
		if (len(current_set) == 1) and (current_set[0] == (('S', G['__root__']+'#'*k), 2, '#'*k, 0)):
			return True

		s_i += 1

	return False

#------------------

def main():
	grammar_path = raw_input('Grammar file: ')
	G = load_grammar(grammar_path)

	while True:
		w = raw_input('Input: ')
		if earley(w, G):
			print("[TRUE]: w is in L(G)")
		else:
			print("[FALSE]: w not in L(G)")

if __name__ == '__main__':
	main()