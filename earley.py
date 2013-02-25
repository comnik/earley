import grammar

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
						rule = old_q[0]
						pos = old_q[1]
						lookahead = old_q[2]
						origin = old_q[3]

					#	print("checking %s if %s matches %s" % (s, P[0], rule[1]))
						if P[0] == peek(rule[1], pos, lookahead):
							q_new = (rule, pos+1, lookahead, origin)
							rule_body_verbose = " ".join(rule[1][:pos]) + '.'+ " ".join(rule[1][pos:])
							print("         %s -> %s (%s)" % (rule[0], rule_body_verbose, origin))
							current_set.append(q_new)
				#else:
				#	print("lookahead %s doesn't match w[i] %s" % (l, w[s_i:s_i+k]))
			else:
				next_symbol = peek(P[1], i, l)
				if next_symbol in G.keys(): # nonterminal next to dot -> predictor applicable
					for rule_body in G[next_symbol]:
						q_new = ((next_symbol, rule_body), 0, peek(P[1], i+k, l), s_i)
						if q_new not in current_set:
							print("         %s -> %s (%s) [P]" % (q_new[0][0], q_new[0][1], q_new[3]))
							current_set.append(q_new)
				elif (next_symbol == peek(w, s_i, '#')) or (next_symbol == '#'): # terminal next to dot -> scanner applicable
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
	grammar_path = 'grammars/a-calc.gr' #raw_input('Grammar file: ')
	G = grammar.load(grammar_path)

	print(G)

	while True:
		w = raw_input('Input: ')
		if earley(w, G):
			print("[TRUE]: w is in L(G)")
		else:
			print("[FALSE]: w not in L(G)")

if __name__ == '__main__':
	main()