import json
import csv
import re
import pickle
import pandas as pd
import numpy as np

#This function extracts user attributes from the user data set
def extract_attributes(attribute, int_user_friends):
	f=open('data/yelp_academic_dataset_user.json','r')
	reader=csv.reader(f)
	user_attribute={}
	for i in reader:
		#print i
		try:
			review_count=int(i[2].split(':')[1])
		except:
			print i
		if review_count <500:
			continue
		user=i[0].split(':')[1][1:-1]
		for record in i:
			if(re.search(attribute,record)):
				try:
					user_attribute[int_user_friends[user]]=int(record.split(':')[1])
				except:
					user_attribute[int_user_friends[user]]=0
	return user_attribute

#This function reads user data and generates a dictionary of each user with reviews > 500 their corresponding friends
def extract_user_friends():

	f=open('data/yelp_academic_dataset_user.json','r')
	reader=csv.reader(f)
	user_friends={}
	#user_friends=pickle.load(open('user_friends.pkl'))
	#print user_friends


	for i in reader:
		#print i
		try:
			review_count=int(i[2].split(':')[1])
		except:
			print i
		if review_count <500:
			continue
		user=i[0].split(':')[1][1:-1]
		try:
			user_friends[user]
		except:
			user_friends[user]=[]
		end=0
		start=0
		for index in range(0,len(i)):
			if(re.search('friends',i[index])):
				start=index
				break
		
		for index in range(start,len(i)):
			if(re.search(']$',i[index])):
				end=index
				break
		#print i[end]
		#print i[5]
		if(re.search('None', i[end])):
			continue
		if(re.search('friends', i[end])):
			temp=i[index].split(':')[1][2:-2]
			user_friends[user].append(temp)
			continue
		user_friends[user].append(i[end][:-1])
		try:
			user_friends[user].append(i[start].split('\"')[1])
		except:
			print i
		if end>start+1:
			for index in range(start+1, end):
				user_friends[user].append(i[index])

		#print user
	return user_friends

#This function maps the user IDs(which are complex strings) to integers
def map_user_to_int(user_friends):
	int_user_friends={}
	number=0
	unique_users=set()
	for i in user_friends:
		unique_users.add(i)
		for j in i:
			unique_users.add(j)
	print len(unique_users)

	for i in unique_users:
		int_user_friends[i]=number
		#final_user_friends[number]=[]
		number+=1
	return int_user_friends

#This function creates integer user friends' list
def int_user_friend_list(int_user_friends, user_friends):
	final_user_friends={}
	for i in int_user_friends:
		final_user_friends[int_user_friends[i]]=[]
	for i in user_friends:
		for j in i:
			try:
				final_user_friends[int_user_friends[i]].append(int_user_friends[j])
			except:
				print j, int_user_friends[j]
	#print final_user_friends
	return final_user_friends
	#f=open('user_friends1.pkl','w')
	#pickle.dump(final_user_friends, f)

#This function converts the user attributes into binary using median split
def discretize(attributes):
	c=0
	for i in attributes:
		try:
			attributes[i]=pandas.qcut(attributes[i], 2, labels=False, precision=100)
			c+=1
		except:
			median=np.median(attributes[i])
			b=attributes[i]>median
			add=[]
			for j in b:
				if j==True:
					add.append(1)
				else:
					add.append(0)
			attributes[i]=add
	return attributes

#Storing in pickle files

user_friends=extract_user_friends()
int_user_friends=map_user_to_int(user_friends)
final_user_friends=int_user_friend_list(int_user_friends)
'''
f=open('original_user_friends1.pkl','w')
pickle.dump(user_friends,f)
f=open('int_user_friends.pkl','w')
pickle.dump(int_user_friends,f)
f=open('user_friends1.pkl','w')
pickle.dump(final_user_friends,f)
#pickle.dump(user_friends,f)
#print user_friends
#print data
#print type(data)
'''


##Attributes List
#'useful:19', 'funny:1', 'cool:4', 'fans:3', 'elite:["2017"', '2016]',
# 'average_stars:4.48', 'compliment_hot:0', 'compliment_more:0', 'compliment_profile:0', 
#'compliment_cute:0', 'compliment_list:0', 'compliment_note:1', 'compliment_plain:0', 
#'compliment_cool:2', 'compliment_funny:2', 'compliment_writer:1', 'compliment_photos:0'



#Loading from pickle files
#user_friends=pickle.load(open('original_user_friends1.pkl','r'))
#print user_friends
#int_user_friends=pickle.load(open('int_user_friends.pkl','r'))
#print int_user_friends
#final_user_friends=pickle.load(open('user_friends1.pkl','r'))
#print final_user_friends

attribute_list=['useful', 'funny', 'cool', 'fans', 'average_stars', 'compliment_hot', 'compliment_more', 'compliment_profile', 'compliment_cute', 'compliment_list','compliment_note','compliment_plain', 'compliment_cool', 'compliment_funny','compliment_writer', 'compliment_photos']
attributes=pd.DataFrame()
f=open('attributes.csv','w')

#Get Attributes

for attribute in attribute_list:
	temp={}
	user_attribute=extract_attributes(attribute,int_user_friends)
	sorted_users=sorted(user_attribute)
	for i in sorted_users:
		temp[i]=user_attribute[i]
	print user_attribute
	attributes[attribute]=temp.values()

attributes=pd.read_csv('attributes.csv')
attributes=discretize(attributes)
print attributes
attributes.to_csv('attributes1.csv')
#print attributes
