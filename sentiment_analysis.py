import csv
import re
from gensim.models.doc2vec import LabeledSentence, Doc2Vec
import collections
import random
import pickle
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
import pandas as pd

random.seed(0)


def read_data():
	with open('data/yelp_academic_dataset_review.json', 'rb') as csvfile:
		data = csv.reader(csvfile)
		for row in data:
			print(row)

#Creates dictionary of user with their reviews
def user_review_mapping():
	my_user_reviews={}
	with open('data/yelp_academic_dataset_review.json', 'rb') as csvfile:
		data = csv.reader(csvfile)
		for review in data:
			user_id=(review[1].split(':'))[1]
			#print(user_id)
			try:
				my_user_reviews[user_id].append((review[5].split(':')[1]))
			except:
				my_user_reviews[user_id]=[(review[5].split(':')[1])]
	return my_user_reviews			

#Cleans the reviews and converts to list of tokens
def refine(reviews):
	test=[]
	for review in reviews:
		words = [w.lower() for w in review.strip().split() if len(w)>=3]
		final_words=[]
		for word in words:
			try:
				temp=re.search('[a-zA-Z]+',word)
				final_words.append(temp.group())
			except:
				a=1
		test.append(final_words)
	return test

#Creates a dictionary for user with values as list of their reviews in tokenized form
def refine_reviews(user_reviews):
	user_review={}
	#print(user_reviews)
	for user in user_reviews:
		result=refine(user_reviews[user])
		#print(user)
		#print(result)
		user_review[user[1:(len(user)-1)]]=result
	#print(user_review)
	return user_review


#This reads the labelled reviews of users and creates corresponding training sets for positive and negative reviews
def refine_labelled_data():
	training_data_pos=[]
	training_data_neg=[]
	labels_pos=[]
	labels_neg=[]
	with open('yelp_labelled.txt') as f:
		data = f.readlines()
	data = [line.strip() for line in data]
	for review in data:
		if((review.split('	')[1])=='1'):
			training_data_pos.append(review.split('	')[0])
			labels_pos.append(1)
		else:
			training_data_neg.append(review.split('	')[0])
			labels_neg.append(0)
	train_pos=[]
	train_neg=[]
	for review in training_data_pos:
		words = [w.lower() for w in review.strip().split() if len(w)>=3]
		final_words=[]
		for word in words:
			try:
				temp=re.search('[a-zA-Z]+',word)
				final_words.append(temp.group())
			except:
				a=1
		train_pos.append(final_words)
	for review in training_data_neg:
		words = [w.lower() for w in review.strip().split() if len(w)>=3]
		final_words=[]
		for word in words:
			try:
				temp=re.search('[a-zA-Z]+',word)
				final_words.append(temp.group())
			except:
				a=1
		train_neg.append(final_words)
	return [train_pos,train_neg,labels_pos,labels_neg]

#Converts reviews into feature vectors using doc2vec and returns feature vectors for both training and testing data
def feature_vecs_DOC(train_pos, train_neg,my_user_reviews):
	labeled_train_pos=[]
	labeled_train_neg=[]
	labeled_test=[]
	for i in range(len(train_pos)):
		sent=LabeledSentence(words=train_pos[i], tags=["TRAIN_POS_%s" %str(i)])
		labeled_train_pos.append(sent)
	
	for i in range(len(train_neg)):
		sent=LabeledSentence(words=train_neg[i], tags=["TRAIN_NEG_%s" %str(i)])
		labeled_train_neg.append(sent)

	n=0
	for user in my_user_reviews:
		test=my_user_reviews[user]
		for i in range(len(test)):
			sent=LabeledSentence(words=test[i], tags=["TEST_%s" %str(n)])
			n=n+1
			labeled_test.append(sent)



	model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=4)
	sentences = labeled_train_pos + labeled_train_neg + labeled_test
	model.build_vocab(sentences)

	for i in range(5):
		print "Training iteration %d" % (i)
		random.shuffle(sentences)
		model.train(sentences)

	train_pos_vec=[]
	train_neg_vec=[]
	test_vec_dic={}

	for i in range(len(train_pos)):
		train_pos_vec.append(model.docvecs["TRAIN_POS_%s" %str(i)])

	for i in range(len(train_neg)):
		train_neg_vec.append(model.docvecs["TRAIN_NEG_%s" %str(i)])

	n=0
	for user in my_user_reviews:
		test=my_user_reviews[user]
		test_vec=[]
		for i in range(len(test)):
			test_vec.append(model.docvecs["TEST_%s" %str(n)])
			n=n+1
		test_vec_dic[user]=test_vec

	return train_pos_vec, train_neg_vec, test_vec_dic



if __name__ == '__main__':
	'''
	user_reviews=user_review_mapping()
	my_user_reviews=refine_reviews(user_reviews)
	#print(my_user_reviews)
	reduced_my_user_reviews={}
	int_user_friends=pickle.load(open('int_user_friends.pkl','r'))
	for string_user in int_user_friends:
		try:
			reduced_my_user_reviews[int_user_friends[string_user]]=my_user_reviews[string_user]
		except:
			continue
	print reduced_my_user_reviews
	f=open('reduced_my_user_reviews.pkl','w')
	pickle.dump(reduced_my_user_reviews,f)
	'''
	'''
	reduced_my_user_reviews=pickle.load(open('reduced_my_user_reviews.pkl','r'))
	[train_pos,train_neg,labels_pos,labels_neg]=refine_labelled_data()
	train_pos_vec, train_neg_vec, test_vec_dic = feature_vecs_DOC(train_pos, train_neg,reduced_my_user_reviews)
	Y = [1]*len(train_pos_vec) + [0]*len(train_neg_vec)
	model=GaussianNB()
	model.fit(train_pos_vec+train_neg_vec,Y)
	sentiment={}
	for user in test_vec_dic:
		sentiment[user]=model.predict(test_vec_dic[user])
	f=open('sentimnt.pkl','w')
	pickle.dump(sentiment,f)
	#print(sentiment)
	'''
	#Evaluating the overall sentiment for every user and dumping it into a pickle file named as sentiment_analysis.pkl
	'''
	my_sentiment=pickle.load(open('sentimnt.pkl','r'))
	sentiment_analysis={}
	for user in my_sentiment:
		value=sum(my_sentiment[user])/float(len(my_sentiment[user]))
		if value<0.5:
			sentiment_analysis[user]=0
		else:
			sentiment_analysis[user]=1
	print(sentiment_analysis)
	f=open('sentiment_analysis.pkl','w')
	pickle.dump(sentiment_analysis,f)
	'''
	sentiment_analysis=pickle.load(open('sentiment_analysis.pkl','r'))
	attributes=pd.read_csv('attributes.csv')
	print attributes
	sorted_users=sorted(sentiment_analysis)
	temp={}
	for i in sorted_users:
		temp[i]=sentiment_analysis[i]
	#print user_attribute
	attributes['sentiment']=temp.values()
	attributes.to_csv('attributes.csv')

	
	'''
	i=0
	print(len(my_user_reviews))
	for user in my_user_reviews:
		if i==0:
			train_pos_vec,train_neg_vec,test_vec=feature_vecs_DOC2(train_pos,train_neg,my_user_reviews[user])
			i=i+1
		else:
			break
		#print(train_pos_vec)
		#print(train_neg_vec)
		#print(test_vec)
	'''
	#print("I am here")
	#print(train_pos_vec)
	#print(train_neg_vec)
	#print(test_vec_dic)