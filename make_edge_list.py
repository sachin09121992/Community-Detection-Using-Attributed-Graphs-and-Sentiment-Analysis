import pickle

#This module creates a edge list of user friends. This is further used to form the graph

f=open('user_friends1.pkl','r')
user_friends=pickle.load(f)
users=sorted(user_friends)
f=open('edge_list1.txt','w')
print "Hello"
for i in users:
	for user in user_friends[i]:
		if i<user:
			f.write(str(i)+' '+str(user)+'\n')

#print user_friends