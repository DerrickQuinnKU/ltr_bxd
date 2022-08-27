import os

#Recursive solver function
#state: {letter: state} containing the current game state 
#words: list of available words
#solution: [str] containing current solution
#max_depth: int containing maximum recursion depth/solution length 
#returns a list containing all found solutions
def solve(state, words, solution, max_depth):
	#check for base cases
 	#always return a list containing all found solutions
	if not 0 in [state[c] for c in state]: 
		return([solution])
		
	if len(solution) > max_depth:
		return []
	
	#Trim words
	#if we have a prev word in the solution, make sure next word starts with previous word's last char
	words_to_try = words
	if len(solution) > 0:
		words_to_try = list(filter(lambda x : x[0] == solution[-1][-1], words_to_try))

	solutions = []
	for word in words_to_try:
		#Create new state to recurse
		#Need to use comprehension for deep copy
		n_state = {c:state[c] for c in state} 
		
		for c in state:
			if c in word:
				n_state[c] = 1

		rec_slns = solve(n_state,words, solution + [word], max_depth)
		solutions += rec_slns
	return solutions

	
if __name__== "__main__":
	
	#Download and store dictionary
	print("Downloading today's dictionary:")

	#Regex to find the dictionary from the page html
	#May not be super clean, but it works. Find the form "dictionary":["abc","def"]
	dict_from_json_re = '\"dictionary\":\[\(\"\w*\"\,\?\)*\]'
	words_from_dict_re = '[A-Z]*'

	os.system("curl https://www.nytimes.com/puzzles/letter-boxed | grep -o '{0}' | grep -o '{1}' > words.txt".format(dict_from_json_re, words_from_dict_re))

	f = open("words.txt", "r")
	words = f.read().split()


	print("Done.\n")

	#Download and store sides

	sides_from_json_re = '\"sides\":\[\(\"\w*\"\,\?\)*\]'
	letters_from_sides_re = '[A-Z]*'

	print("Downloading today's sides:")
	os.system("curl https://www.nytimes.com/puzzles/letter-boxed | grep -o '{0}' | grep -o '{1}' | tr -d '\n' > sides.txt".format(sides_from_json_re, letters_from_sides_re))
	f_sides = open("sides.txt", 'r')
	sides = f_sides.read()
	state = {c:0 for c in sides}
	print("Done.\n")



	#Solve it
	i = 1
	solutions = [] 
	while len(solutions) == 0:
		solutions = solve(state,words,[],i)
		i+=1

	solutions.sort(key=lambda soln : sum([len(w) for w in soln]))  

	print("Solution:")

	for w in solutions[0]:
		print(w)
