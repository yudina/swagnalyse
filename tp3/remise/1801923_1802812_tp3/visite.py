import random
import sys

ex_path = sys.argv[1]
options = sys.argv[2:]

# file data
n_sites = 0
adj_matrix = [] # row will be start point, while column will be endpoint
max_time = 0
popularity = [] # 1d array

# probabilistic
I_HOTEL = 0
POP_HOTEL = 0

# travel attributes
travel = [] # list of tuple : index, popularity, time
I_SITE = 0
I_POP = 1
I_TIME = 2
best = 0 # best score

# greedy
avail_popularity = [] # array of indexes of popularity

# go back
N_BACKTRACK = 5

def extractData(file_name):
    global n_sites
    global max_time
    global popularity
    global adj_matrix
    
    # obtain every line as int list
    with open(file_name,'r') as ex:
        for line in ex:
            line = line.strip()
            if len(line) > 1:
               adj_matrix.append([int(a) for a in line.split()])
           
    # collect data
    n_sites = adj_matrix[0][0]
    max_time = adj_matrix[-2][0]
    popularity = adj_matrix[-1]
    
    # delete first, second to last and last rows
    adj_matrix.remove(adj_matrix[0])
    adj_matrix.remove(adj_matrix[-2])
    adj_matrix.remove(adj_matrix[-1])

# probabilist algorithm
def randomBeginTravel():
    global travel
    global avail_popularity
    
    # generate n_sites*0.1 random indexes for the beginning of the travel
    n_random_sites = int( (n_sites)*0.1 )
    # range(1, n_sites) so hotel is not generated
    i_random_sites = random.sample(range(1, n_sites), n_random_sites)
    
    cumul_time = 0
    
    # choose random sites
    for i in range(1, n_random_sites):
        if (cumul_time <= max_time):
            i_previous_site = travel[i-1][I_SITE]
            new_time = adj_matrix[i_previous_site][i_random_sites[i]]
            
            # check if can add the next random site.
            # travel tuplet : site index, site popularity, travel time to site
            if (cumul_time + new_time <= max_time):
                travel.append((i_random_sites[i], popularity[i_random_sites[i]], new_time))
                cumul_time += new_time
            else: # max_time reached
                break
        else:
            break
    
    # copy popularity, and remove visited sites in the copy
    # visited is reversed, so we delete elements in decreasing order of index
    visited = sorted(i_random_sites, key=int, reverse=True)
    avail_popularity = []
    
    # avail_popularity contains the index of unvisited sites
    for i in range(n_sites):
        avail_popularity.append(i)
    
    # remove visited places
    for i in range(len(visited)):
        j = visited[i]
        avail_popularity.remove(avail_popularity[j])
        
    avail_popularity.remove(I_HOTEL) # remove hotel

# calculate total time of travel
def calculateCumul(trav):
    total = 0
    for i in range(len(trav)):
        total += trav[i][I_TIME]
    return total

# calculate total popularity of travel
def calculatePop(trav):
    total = 0
    for i in range(len(trav)):
        total += trav[i][I_POP]
    return total

# return de density matrix for the row i_current_site (last site of the travel)
def calculateDensityLine(i_current_site):
    d_line = [] # tuplet : density, index of column
    for i in range(n_sites):
        if (adj_matrix[i_current_site][i] != 0):
            d_line.append( (popularity[i]/adj_matrix[i_current_site][i], i) )
        else:
            d_line.append( (0, i) )
    return d_line

# sort density in decreasing order, then return the index of the highest possible
# density (a density which column corresponds to a free n in avail_popularity)
def maxDensity(d_line, a_popularity):
    sorted_d_line = []
    i_column = 1
    
    # tuplet : density, index of column. density is first, it allows to use sorted
    sorted_d_line = sorted(d_line, key=lambda x: x[0], reverse=True)
    
    for i in range(len(sorted_d_line)):
        if(sorted_d_line[i][i_column] in a_popularity):
            return sorted_d_line[i][i_column]
    return 0

def findGreedyTravel():
    global travel
    global avail_popularity
    density_line = []
    
    avail_len = len(avail_popularity)
    for i in range(avail_len):
        
        cumul_time = calculateCumul(travel)
        
        if(cumul_time <= max_time):
            # current row index is index of current travel site
            i_current_site = travel[-1][I_SITE]
            density_line = calculateDensityLine(i_current_site)
            
            # get the index of the maximum available density
            i_max_density = maxDensity(density_line, avail_popularity)
            
            # time from current site to new site
            new_time = adj_matrix[i_current_site][i_max_density]
            
            # check if can add the new site
            # travel tuplet : site index, site popularity, travel time to site
            if (cumul_time + new_time <= max_time):
                travel.append((i_max_density, popularity[i_max_density], new_time))
                avail_popularity.remove(i_max_density)
            else: # max_time reached
                break
        else:
            break
        
def goBackHotel():
    global travel
    
    # please forgive us for some code duplication.
    
    # current row index is index of current travel site
    i_current_site = travel[-1][I_SITE]
    
    # time from current site to hotel
    new_time = adj_matrix[i_current_site][I_HOTEL]
    
    # try to directly go to hotel, else backtrack and try
    if (calculateCumul(travel) + new_time <= max_time):
        travel.append( (I_HOTEL, POP_HOTEL, new_time) )
        return
    else:
        for i in range(N_BACKTRACK):
            if(travel[-1][I_SITE] != I_HOTEL):
                travel.remove(travel[-1])
                
                new_time = adj_matrix[travel[-1][I_SITE]][I_HOTEL]
                
                if (calculateCumul(travel) + new_time <= max_time):
                    travel.append( (I_HOTEL, POP_HOTEL, new_time) )
                    return

def printTravel():
    for i in range(len(travel)):
        print(travel[i][0], end=" ")
    print()

# MAIN
extractData(ex_path)

while True:
    travel.clear()
    avail_popularity.clear()
    travel.append((I_HOTEL, POP_HOTEL, adj_matrix[I_HOTEL][I_HOTEL])) # go to hotel
    randomBeginTravel()
    findGreedyTravel()
    goBackHotel()
    
    # print quality of travel
    score = calculatePop(travel)
    if best < score:
        best = score
        print(score)
        if '-p' in options: # Print result
            printTravel()
# END OF MAIN




