# -*- coding: UTF-8 -*-

#Random names generator
#by Jefferson Pinheiro

import glob, random, string, os

#hold generated names, they must be unique
CultureNames = []
FactionNames = []

#Generate a random person name
#IsFirstName=1: a prefix may be added; 0: a suffix may be added; other: no suffixes or prefixes
def GenerateName(DictionaryName, IsFirstName):
	Name = ""
	HasNames1=0
	try: #try CultureGroups/Names/ first
		Dictionary1 = open("Generator/CultureGroups/Names/"+DictionaryName+".names1").readlines()
		HasNames1=1
	except: #if it's not there, try CultureGroups/
		Dictionary1 = open("Generator/CultureGroups/"+DictionaryName+".names1").readlines()
	Dictionary2 = []
	try:
		Dictionary2 = open("Generator/CultureGroups/Names/"+DictionaryName+".names2").readlines()
	except:
		pass
	if len(Dictionary2) == 0 and not HasNames1:
		try:
			Dictionary2 = open("Generator/CultureGroups/"+DictionaryName+".names2").readlines()
		except:
			pass
	try:
		Dictionary3 = open("Generator/CultureGroups/Names/"+DictionaryName+".names3").readlines()
	except:
		Dictionary3 = open("Generator/CultureGroups/"+DictionaryName+".names3").readlines()
	
	#prefix:
	try:
		Prefixes = open("Generator/CultureGroups/Names/"+DictionaryName+".prefix").readlines()
		PrefixChance = int(Prefixes[0])
		Prefixes.pop(0)
		if random.randint(0,100)<=PrefixChance and IsFirstName==1:
			Prefix = random.choice(Prefixes)
			Prefix = Prefix.replace('\n','')
			Name += Prefix
			if Prefix[len(Prefix)-1] != '-' and Prefix[len(Prefix)-1] != '\'' and Prefix[len(Prefix)-1] != '^':
				Name += " "
			Name = Name.replace('^','')
	except:
		pass
			
	#middle:		
	Name += random.choice(Dictionary1)
	if len(Dictionary2)>0:
		ChanceMin=0
		ChanceMax=1
		try:
			ChanceMin=int(Dictionary2[0])
			ChanceMax=int(Dictionary2[1])
			Dictionary2.pop(0)
			Dictionary2.pop(0)
		except:
			pass
		for i in range(random.randint(ChanceMin,ChanceMax)):
			Name += random.choice(Dictionary2)
	Name += random.choice(Dictionary3)		
	
	#suffix:
	try:
		Suffixes = open("Generator/CultureGroups/Names/"+DictionaryName+".suffix").readlines()
		SuffixChance = int(Suffixes[0])
		Suffixes.pop(0)
		if random.randint(0,100)<=SuffixChance and IsFirstName==0:
			Suffix = random.choice(Suffixes)
			Suffix = Suffix.replace('\n','')
			if Suffix[0] != '-' and Suffix[0] != ',' and Suffix[0] != '^':
				Name += " "
			Name += Suffix
			Name = Name.replace('^','')
	except:
		pass
	if IsFirstName==0 or IsFirstName==1:
		Name = Name.replace("$city$",GeneratePlaceName(DictionaryName,1))
		Name = Name.replace("$name$",GenerateName(DictionaryName,2))
	Name = Name.replace('\n','')
	return Name
	
#Generate a random place name
def GeneratePlaceName(DictionaryName, Recursion=0, UseShortNames=0):
	Name = ""
	Dictionary1 = open("Generator/CultureGroups/"+DictionaryName+".names1").readlines()
	Dictionary2 = []
	try:
		Dictionary2 = open("Generator/CultureGroups/"+DictionaryName+".names2").readlines()
	except:
		pass
	Dictionary3 = open("Generator/CultureGroups/"+DictionaryName+".names3").readlines()
	#prefix:
	if not UseShortNames:
		try:
			Prefixes = open("Generator/CultureGroups/"+DictionaryName+".prefix").readlines()
			PrefixChance = int(Prefixes[0])
			Prefixes.pop(0)
			if random.randint(0,100)<=PrefixChance and Recursion==0:
				Prefix = random.choice(Prefixes)
				Prefix = Prefix.replace('\n','')
				Name += Prefix
				if Prefix[len(Prefix)-1] != '-' and Prefix[len(Prefix)-1] != '^':
					Name += " "
				Name = Name.replace('^','')
		except:
			pass
			
	Name += random.choice(Dictionary1)
	if len(Dictionary2)>0:
		ChanceMin=0
		ChanceMax=1
		try:
			ChanceMin=int(Dictionary2[0])
			ChanceMax=int(Dictionary2[1])
			if UseShortNames and ChanceMax>1:
				ChanceMax=1
			Dictionary2.pop(0)
			Dictionary2.pop(0)
		except:
			pass
		for i in range(random.randint(ChanceMin,ChanceMax)):
			Name += random.choice(Dictionary2)
	Name += random.choice(Dictionary3)
	#suffix:
	if not UseShortNames:
		try:
			Suffixes = open("Generator/CultureGroups/"+DictionaryName+".suffix").readlines()
			SuffixChance = int(Suffixes[0])
			Suffixes.pop(0)
			if random.randint(0,100)<=SuffixChance and Recursion==0:
				Suffix = random.choice(Suffixes)
				Suffix = Suffix.replace('\n','')
				if Suffix[0] != '-' and Suffix[0] != ',' and Suffix[0] != '^':
					Name += " "
				Name = Name.replace('^','')
				Name += Suffix
		except:
			pass
	if Recursion==0:
		Name = Name.replace("$city$",GeneratePlaceName(DictionaryName,1))
		Name = Name.replace("$name$",GenerateName(DictionaryName,2))
	Name = Name.replace('\n','')
	return Name

#Generate a random name that is not equal to CultureName or taken
def GenerateFactionName(DictionaryName, CultureName):
	Dictionary1 = open("Generator/CultureGroups/"+DictionaryName+".names1").readlines()
	Dictionary2 = []
	try:
		Dictionary2 = open("Generator/CultureGroups/"+DictionaryName+".names2").readlines()
	except:
		pass
	Dictionary3 = open("Generator/CultureGroups/"+DictionaryName+".names3").readlines()
	#Generate a name
	Name = CultureName
	while Name == CultureName:
		Name = random.choice(Dictionary1)
		if len(Dictionary2)>0:
			ChanceMin=0
			ChanceMax=1
			try:
				ChanceMin=int(Dictionary2[0])
				ChanceMax=int(Dictionary2[1])
				Dictionary2.pop(0)
				Dictionary2.pop(0)
			except:
				pass
			for i in range(random.randint(ChanceMin,ChanceMax)):
				Name += random.choice(Dictionary2)	
		Name += random.choice(Dictionary3)	
		Name = string.replace(Name, '\n','')
	
	#check if name is taken
	for i in range(len(FactionNames)):
		if Name == FactionNames[i] or Name == CultureName:
			return GenerateFactionName(DictionaryName, CultureName)
	FactionNames.append(Name)
	return Name

"""
os.chdir("CultureGroups")
files = glob.glob("*.names1")
os.chdir("../../")
for f in files:
	f = f.replace(".names1","")
	print "\n----------------------------"
	print f.upper()+":"
	print "----------------------------"
	for i in range(30):
		print GenerateName(f,1)+" "+GenerateName(f,0)
"""