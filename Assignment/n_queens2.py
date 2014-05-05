#Author - Myles Cullen

import pycosat
import sys


def solve(n):
	y =[]
	#rows
	for i in range (1,(n*n)+1,n):
		y += vertical(range(i,i+n,1),True)

	#columns
	for i in range (1,n+1):
		y+= vertical(range(i,(n*n)-n+1+i,n),True)
		
	#diagonals 
	y+=diagonal(1,n)
	
	#results
	result = []
	for sol in pycosat.itersolve(y):
		result.append(sol)

	#replace numbers with something more meaningful
	result = changeFormat(result,n)
	#return a boolean list indicating which solutions are unique 
	isValid = returnWithoutRotations(result)
	#figure out how many unique solutions there are
	NValidSol = 0
	for i in range(0,len(result)): 
		if isValid[i] :
			NValidSol += 1
	#print out all the unique solutions
	for i in range(0,len(result)):
		if(isValid[i]):
			printSol(result[i])

	print("There are " , NValidSol ,  " unique solutions with rotations and reflections")

#-------------------------------------
#returns a list of booleans indicating whether a solution is unique or not
#-------------------------------------
def returnWithoutRotations(result):

	#list of booleans for rotations
	isValid = [True] *len(result)

	#rotate the first list 4 times and check for uniqueness
	newSol =  returnRotatedSol(n,result[0])
	
	#test the rotated list against the rest
	for k in range(0,len(result)):
		#rotate 4 times
		for j in range (0,5):
			if j == 0:
				newSol =  result[k]
			else:
				newSol =  returnRotatedSol(n,newSol)
			#test rotated one against the others
			for i in range(1+k,len(result)):
				if isValid[i]:
					if(isListEqual(newSol,result[i],n)):
						isValid[i] = False
			##test rotated one against the others
			reflectSol =  returnReflectedSol(n,newSol)
			for i in range(1+k,len(result)):
				if isValid[i]:
					if(isListEqual(reflectSol,result[i],n)):
						isValid[i] = False

	return isValid
#-------------------------------------
#changes the format of the orginal list to use chars instead
#-------------------------------------
def changeFormat(result,n):
	index = 0
	for i in result:
		for j in range(0,n*n):
			if result[index][j] > 0 :
				result[index][j] = 'Q'
			else :
				result[index][j] = '-'
		index += 1

	return result
#-------------------------------------
#checks to see if 2 lists are equal				  	
#-------------------------------------
def isListEqual(a,b,n):	
	for i in range(0,n*n):
		if(a[i] != b[i]):
			return False

	return True
#-------------------------------------
#return diagonal clauses
#-------------------------------------
def diagonal(m,n):
	
	clauses = []
	
	for i in range(n-1):
		for cl in vertical([n*j+j+i+1 for j in range(n - i)]):
			clauses.append(cl)

	for i in range(1,n-1):
		for cl in vertical([n*(j+i)+j+1 for j in range(n - i)]):
			clauses.append(cl)

	for i in range(n-1):
		for cl in vertical([n*j+(n-(i+j)) for j in range(n - i)]):
			clauses.append(cl)		
	
	for i in range(1,n-1):
		for cl in vertical([n*(j+i)+(n-j) for j in range(n - i)]):
			clauses.append(cl)
	
	return clauses

#-------------------------------------
#helper function for creating clauses
#-------------------------------------
def makeNegative(v1,v2):
	return [-v1,-v2]

#-------------------------------------
# function for printing out solutions
#-------------------------------------
def printSol(sol):
	for i in range(0,n*n,n):
			print sol[i:i+n]
	print ' '

#-------------------------------------
#function for creating both vertical and horizontal clauses 
#-------------------------------------
def vertical(iterator,diag=False):
	clauses = []
	intermed =[]
	if diag:
		for i in iterator:
			intermed.append(i)
	
		clauses.append(intermed)

	for i in iterator:
		for j in iterator:
			if i < j:
				clauses.append(makeNegative(i,j))
	return clauses
#-------------------------------------
#returns a rotated solution
#-------------------------------------
def returnRotatedSol(n,sol):
	result = []
	newSol = []
	# generate the iterator
	for i in range(0,n):
		result.append([(n*n)-n-j+i  for j  in range(0,n*n,n)])

	#make the new rotated list from the iterator
	for i in range(0,n):
		for j in result[i]:
			newSol.append(sol[j])	

	return newSol
#-------------------------------------
#returns a reflected solution
#-------------------------------------
def returnReflectedSol(n,sol):
	result = []
	newSol = []
	# generate the iterator
	for i in range(0,n):
		result.append([(n*i+n-1)-j  for j  in range(0,n)])
	#make the new rotated list from the iterator
	for i in range(0,n):
		for j in result[i]:
			newSol.append(sol[j])	

	return newSol

if __name__ == '__main__':
	n = int(sys.argv[1],base=10)
	print("The solution for" , n ,  "Queens ")
	if n > 3:
		solve(n)
	
