import sys
import time
from decimal import Decimal

ex_path = sys.argv[1] # Path de l'exemplaire

poids = []
poidsMax = 0
    
# lire exemplaire
text_file = open(ex_path, "r")
next(text_file)
lines = text_file.read().split()
text_file.close()

# extraire batons

poids = lines[1::2]
poidsMax = int(lines[-1])

debut = time.time()
poids = sorted(poids, key=int, reverse=True) # Trie les bâtons en ordre décroissant
poids = [ int(x) for x in poids ]
nbDyn = len(poids)

# algo de glouton
sommeBatons = 0
solution = []
for i in range (nbDyn):
    if sommeBatons + poids[i] < poidsMax:
        sommeBatons += poids[i]
        solution.append(poids[i])
fin = time.time()

sommeBatons = 0
temps = fin - debut

for i in range(len(solution)):
    sommeBatons += solution[i]

def imprimerSolution(solution):
    sortie = ""
    for i in range(len(solution)):
        sortie += str(solution[i]) + " "
    print(sortie)
    
def runSolution(solution):
    sommeBatons = 0
    for i in range(len(solution)):
        sommeBatons += solution[i]
    output = str(temps) + ";" + str(sommeBatons)
    print(output)

options = sys.argv[2:]
if '-p' in options: # On imprime la solution
    imprimerSolution(solution)
if '-r' in options: # On imprime la solution et le temps
    runSolution(solution)
if '-t' in options: # On imprime le temps d'exécution
    print(temps)
    