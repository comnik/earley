from grammar import load_grammar, rule_to_str

def peek(s, i, fallback):
	if i < len(s):
		return s[i]

	return fallback

def earley(w, G, k=1):
	n = len(w)
	w += k*'#'

	# sets of states q=(P, i, l, s)
	sets = [[] for x in range(n+2)]
	sets[0].append( (('S', G['__root__']+'#'*k), 0, '#'*k, 0) )

	s_i = 0
	while True:
		current_set = sets[s_i]
		print("\n\nSet %s:" % s_i)
		
		if current_set == []:
			print("    !!!Set is empty. w not in L(G)!!!")
			return False

		for q in current_set:
			P = q[0]
			i = q[1]
			l = q[2]
			s = q[3]
			
			print("    %s" % rule_to_str(P[0], P[1], i))

			# check if we reached the end of this rule
			if i == len(P[1]):

				# this rule is finished, we need check if completing the
				# substructre is possible
				
				# print("attempting to complete %s..." % rule_to_str(P[0], P[1], s))
				
				# completer is applicable if lookahead matches next k symbols
				if l == w[s_i:s_i+k]:
					
					# lookahead matches, so check every old set for
					# states that led us to q
					
					# [COMPLETER]
					for old_q in sets[s]:
						rule = old_q[0]
						pos = old_q[1]
						lookahead = old_q[2]
						origin = old_q[3]

						if P[0] == peek(rule[1], pos, lookahead):
							q_new = (rule, pos+1, lookahead, origin)
							current_set.append(q_new)

							print("         %s (%s)" % (rule_to_str(rule[0], rule[1], pos+1), origin))
					# [/COMPLETER]

			else: # this rule is still being processed

				next_symbol = peek(P[1], i, l)

				# check if nonterminal next to dot
				if next_symbol in G.keys():

					# [PREDICTOR]
					for rule_body in G[next_symbol]:
						q_new = ((next_symbol, rule_body), 0, peek(P[1], i+k, l), s_i)
						if q_new not in current_set:
							print("         %s (%s) [P]" % (rule_to_str(next_symbol, rule_body, 0), q_new[3]))
							current_set.append(q_new)
					# [/PREDICTOR]

				# check if terminal next to dot
				elif (next_symbol == peek(w, s_i, '#')) or (next_symbol == '#'): 

					# [SCANNER]
					q_new = (P, i+1, l, s)
					print("         Moving %s (%s) [S]" % (rule_to_str(P[0], P[1], i+1), q_new[3]))
					sets[s_i+1].append(q_new)
					# [/SCANNER]
	
		# check if all substructres are closed/finished
		# and if the root-production is completed 	
		if (len(current_set) == 1) and (current_set[0] == (('S', G['__root__']+'#'*k), 2, '#'*k, 0)):
			return True

		s_i += 1

	return False

#------------------

def main():
	grammar_path = raw_input('\nGrammar file: ')
	G = load_grammar(grammar_path, True)
	print(G)
	while True:
		w = raw_input('\nInput: ')
		if earley(w, G):
			print("\n[TRUE]: w is in L(G)")
		else:
			print("\n[FALSE]: w not in L(G)")

if __name__ == '__main__':
	main()