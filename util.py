import string 
import re 
import random 
import nltk, math

reflections = {
  "i am"       : "you are",
  "i was"      : "you were",
  "i"          : "you",
  "i'm"        : "you are",
  "i'd"        : "you would",
  "i've"       : "you have",
  "i'll"       : "you will",
  "my"         : "your",
  "you are"    : "I am",
  "you were"   : "I was",
  "you've"     : "I have",
  "you'll"     : "I will",
  "your"       : "my",
  "yours"      : "mine",
  "you"        : "me",
  "me"         : "you"
}
ip=["NA",]
noun=[]
inp=[]
class Chat(object): 
	# Initializes the class
	def __init__(self, pairs, reflections={}):
		self._pairs = [(re.compile(x, re.IGNORECASE),y) for (x,y) in pairs] 
 		self._reflections = reflections

 	#Function for substtuting the response based on the key
 	def _substitute(self, x):
 		words = "" 
		for word in string.split(string.lower(x)): 
			if self._reflections.has_key(word): 
				word = self._reflections[word] 
			words += ' ' + word 
		return words

	 # Refers back to the sentence in cases required.  

	def _wildcards(self, response, match): 
 		pos = string.find(response,'%') 
 		while pos >= 0: 
			num = string.atoi(response[pos+1:pos+2]) 
 			response = response[:pos] + self._substitute(match.group(num)) + response[pos+2:] 
			pos = string.find(response,'%') 
		return response 

	def respond(self, x):

		#Stores all the nouns from the conversation. Also stores the whole inouts with it.

		def NN(x):
		    temp=[]
		    N=['NN', 'NNP']
		    def ie_preprocess(document):
		        sentences = nltk.sent_tokenize(document) 
		        sentences = [nltk.word_tokenize(sent) for sent in sentences] 
		        sentences = [temp.append(nltk.pos_tag(sent)) for sent in sentences] 
		    ie_preprocess(x)
		    for i in range(len(temp[0])):
		        if (temp[0][i][1]) in N:
		            if (temp[0][i][0]) not in noun:
		                if (temp[0][i][1]) not in noun:
		                    noun.append((temp[0][i][0], x))
		    return noun

		# Stores all the third person pronouns in a list. If any third person pronoun is
		#referred to then it looks back and brings back the last noun the user mentioned.
		#If it can't find one it will ask for the person.

		def prp(x):
			temp=[]
			pr= ["he","she","his","her","himself","herself","it","itself","they","them","themselves"]
			sentences = nltk.sent_tokenize(x) 
			sentences = [nltk.word_tokenize(sent) for sent in sentences] 
			[temp.append(nltk.pos_tag(sent)) for sent in sentences]
			for i in range(len(temp)):
			    # print len(temp)
			    if temp[0][i][0] in pr:
			    	if len(noun)>0:
			    		# print "Are you talking about " + str((noun[-1][0]))
			    		pr = "Are you talking about " + str((noun[-1][0]))
			    		print pr
			    	else:
			    		# print "Whom you are talking about"
			    		pr = "Whom you are talking about"
			    		print pr
					return True
			    else:
			    	return None
			# return pr

		#Checks for synonums of mather and refers to mother and fetches response from
		#the dictionary related to mother.

		def mo(x):
			m=["mother","ma", "mom", "madre", "mamma", "maama", "mama"]
			temp=[]
			sentences = nltk.sent_tokenize(x) 
			sentences = [nltk.word_tokenize(sent) for sent in sentences] 
			[temp.append(nltk.pos_tag(sent)) for sent in sentences]
			for i in range(len(temp[0])):
			    if temp[0][i][0] in m:
			    	return True
		
		#Checks for synonums of father and refers to father and fetches response from
		#the dictionary related to father.

		def fa(x):
			f=["father","dad", "papa", "pop", "pappa", "daddy"]
			temp=[]
			sentences = nltk.sent_tokenize(x) 
			sentences = [nltk.word_tokenize(sent) for sent in sentences] 
			[temp.append(nltk.pos_tag(sent)) for sent in sentences]
			for i in range(len(temp[0])):
			    if temp[0][i][0] in f:
			    	return True

			#Checks for synonums of father and refers to brother and fetches response from
		#the dictionary related to brother.

		def fr(x):
			f=["friend","bro","bff","amigo","dude","bestie", "best friend"]
			temp=[]
			sentences = nltk.sent_tokenize(x) 
			sentences = [nltk.word_tokenize(sent) for sent in sentences] 
			[temp.append(nltk.pos_tag(sent)) for sent in sentences]
			for i in range(len(temp[0])):
			    if temp[0][i][0] in f:
			    	return True
		#Function for not to repeat yourself
		ip_temp=[]
		for i in range(len(ip)):
		    ip_temp.append(ip[i][0])
		if x == ip_temp[-1]:
			return "Please do not repeat yourself."

		#Check for father related synonym and redirects to the response pair with
		#father as the key
		if fa(x):
			for (pattern, response) in self._pairs: 
	 			match = pattern.match("father") 
				if match: 
					resp = random.choice(response)    # pick a random response 
	 				resp = self._wildcards(resp, match) # process wildcards 
					if resp[-2:] == '?.': resp = resp[:-2] + '.' 
					if resp[-2:] == '??': resp = resp[:-2] + '?'
					ip.append((x, resp)) 	
					return resp

		#Check for father related synonym and redirects to the response pair with
		#mother as the key

		if mo(x):
			for (pattern, response) in self._pairs: 
	 			match = pattern.match("mother") 
				if match: 
					resp = random.choice(response)    # pick a random response 
	 				resp = self._wildcards(resp, match) # process wildcards 
					if resp[-2:] == '?.': resp = resp[:-2] + '.' 
					if resp[-2:] == '??': resp = resp[:-2] + '?'
					ip.append((x, resp)) 	
					return resp


		#Check for father related synonym and redirects to the response pair with
		#brother as the key

		if fr(x):
			for (pattern, response) in self._pairs: 
	 			match = pattern.match("friend") 
				if match: 
					resp = random.choice(response)    # pick a random response 
	 				resp = self._wildcards(resp, match) # process wildcards 
					if resp[-2:] == '?.': resp = resp[:-2] + '.' 
					if resp[-2:] == '??': resp = resp[:-2] + '?'
					ip.append((x, resp)) 	
					return resp

		#If it's a third person preposition it executes prp(x)
		if prp(x)== True:
			prp(x)

		# Brings the context of previous noun back randomly
		if math.sqrt(len(noun))>2 & len(ip)>20:
			print "So, we have not talked about "+random.choice(noun(1:(len(noun)-1))

		# Checks for each i/p. If the input is already excuted then checks for the
		#previos response and gives you response which is different from previous responses.

		else:
			for (pattern, response) in self._pairs: 
	 			match = pattern.match(x) 
				if match:
					if x in inp:
						for i in range(len(ip)):
							if x==ip[i][0]:
								# print "yes"
								tmp=[]
								temp=str(response).split(",")
								for j in range(len(temp)):
									if temp[j][2:-1]!=ip[i][1]:
										tmp.append(temp[j])
								resp=random.choice(tmp)

					else:
						resp = random.choice(response)
					# print resp    # pick a random response 
	 				resp = self._wildcards(resp, match) # process wildcards 
					
					# if resp[-2:] == '?.': resp = resp[:-2] + '.' 
					# if resp[-2:] == '??': resp = resp[:-2] + '?'
					ip.append((x, resp))
					NN(x)
					if x not in inp:
						inp.append(x)
						
					return resp

	#Converse Function

	def converse(self, quit="quit"): 
		input = "" 
		while input != quit: 
			input = quit 
			try: input = raw_input(">") 
			except EOFError: 
				print input 
			if input: 
				while input[-1] in "!.": input = input[:-1]
				# if self.respond(input) != None:
				print self.respond(input) 
