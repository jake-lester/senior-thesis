# takes the senators twitter handle text file and converts to a list of lists
import numpy as np

senators = []
senator_file = open("senators.txt", 'r')
for line in senator_file.readlines():
    lst = line.split(" ")
    if len(lst) == 5:
        lst = lst[:2] + lst[-2:]
    elif len(lst) == 6:
        lst = lst[:2] + [lst[3], lst[-1]]
    lst[-1] = lst[-1][:-1] #remove \n
    senators.append(lst)

senators = np.array(senators)
f = open("senators_list.txt", 'w')
f.write(str(list(senators[:,-1])))
f.close()
#print(list(senators[:,-1]))