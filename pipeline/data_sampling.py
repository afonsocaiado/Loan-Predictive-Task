import pandas as pd
import sys,getopt
import random


def sampling(train):
	random.seed(10)

	positive = train.copy()
	negative = train.copy()
	
	positive = negative.loc[negative["status"] == 1]
	negative = negative.loc[negative["status"] == -1]
	
	print([len(positive),len(negative)])
	
	while(len(positive) != len(negative)):
		if(len(positive) > len(negative)):
			positive = randomRemove(positive)
		elif(len(positive) > len(negative)):
			negative = randomRemove(negative)
	
	return[positive,negative]
	
def randomRemove(df):
	return df.drop(df.index[random.randint(0,len(df)-1)])
	