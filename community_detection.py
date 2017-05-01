import csv
import random
import sys
import math
import scipy
import numpy as np
from scipy.spatial import distance
from igraph import *
from scipy.spatial.distance import cosine
import pickle

alpha=float(sys.argv[1])



data=[]

file = open('attributes.csv')
csv_file = csv.reader(file)
t=0
for row in csv_file:
  temp=[]
  for i in range(len(row)):
    if t!=0:
     temp.append(int(row[i]))
  data.append(temp)
  t=t+1
data.pop(0)
sim=[]
for i in range(0,len(data)):
  temp=[]
  print i
  for j in range(0,len(data)):
    a=np.array(data[i])
    b=np.array(data[j])
    try:
      cosine_distance = 1-cosine(a,b)
    except:
      cosine_distance=0
    temp.append(cosine_distance)
  sim.append(temp)
#f=open('sim.pkl','w')
#pickle.dump(sim,f)

print "Similarity done"
graph=Graph.Read_Edgelist('edge_list1.txt', directed= False)


#Computing similarity between vertices


m=graph.ecount()

vertices=[]
for i in range(5119):
  vertices.append([i])
community_list=[]
for i in range(5119):
  community_list.append([i])

for i in range(2):
  #Phase 1 begins
  print "For Hello"
  while(1):
    print "While Hello"
    last=len(community_list)
    
    for i in vertices:
      max_gain=0
      index=-1
      for j in community_list:
        if(i!=j):
          G=0
          
          QAttr=0
          QAttr1=0
          QAttr2=0
          length=1
          G=0
          #To compute QAttr, we sum up all the similarities between the given vertex and all vertices in the community and normalizing it
          
          for vertexi in i:
            for vertexj in j:
              QAttr1+=sim[vertexi][vertexj]
              if(graph.are_connected(vertexi, vertexj)):
                G+=1
          
          #We also have to account for the decrease in QAttr due to removal of a vertex from current community
          for vertexi in i:
            for community in community_list:
              if(vertexi in community):
                length=len(community)
                for node in community:
                  if(node!=vertexi):
                    QAttr2+=sim[vertexi][node]
                break
          QAttr=(QAttr1/(len(i)+len(j)) - QAttr2/length)/len(community_list)
          

          #Computing the change in modularity
          degreei=0
          degreej=0
          for vertexi in i:
            degreei+=graph.degree(vertexi)
          for vertexj in j:
            degreej+=graph.degree(vertexj)
          temp=float((degreei*degreej))/(2*m)
          QNew=G-temp
          QNew=QNew/(2*m)
          Q = alpha*QNew + (1-alpha)*QAttr
          #Q = alpha*QNew
          if(Q > max_gain):
            max_gain=Q
            index=community_list.index(j)
      if(max_gain>0):
        #Removing vertex from given community
        for vertexi in i:
          for community in community_list:
            try:
              community.remove(vertexi)
              break
            except:
              continue
        #Adding vertex to new community
        community_list[index]=community_list[index]+i
        community_list=[community for community in community_list if community!=[]]
    if(len(community_list)==last):
      break
    #Phase 1 ends
  vertices=community_list
  
f=open('communities1.txt','w')
for community in community_list:
  f.write(str(community)[1:-1])
  f.write('\n')

#print(communities)
#print(len(communities))



    

