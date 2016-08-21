# -*- coding: UTF-8 -*-

# The Victoria II + AHD + HoD Random World Generator!
# by Jefferson Pinheiro
# Contact: ixiguis@gmail.com
# Version 1.4
# Custom graphics and most names dictionaries by Jackson Pinheiro
# Special thanks to: 
# - Taylor (Paradox forums) for his provinces adjacency loader.
# - fivex for finding out what was the bug with the generator and A House Divided.

# Free for non-commercial use:
# Creative Commons 3.0 Unported (CC BY-NC)
# http://creativecommons.org/licenses/by-nc/3.0/

import NameGen, GenUtils, sys, random, string, os, glob, time, math, shutil, time, datetime
from distutils import dir_util

#import psyco (optimization module), if available
try:
	import psyco
	psyco.full()
except:
	pass

if not "Generator" in os.getcwd():
	print("The Generator must be installed on the Generator subfolder!\nExample:")
	print("C:\\Victoria 2\\Generator\\")
	print("Note: it is case-sensitive (Victoria 2\\generator won't work)")
	input("Press Enter to exit.")
	sys.exit(1)
	
print("\nYou can customize some variables by editing the Settings.ini file.\n")

DEBUG_CULT_POS=0
DEBUG_TEXT=0

################### DEFINES ####################
# See Settings.ini for description on these variables
#General

Seed = GenUtils.GetParameter("Seed")
if Seed == 0:
	Seed = int(time.time())
random.seed(Seed)

UseShortNames = GenUtils.GetParameter("UseShortNames")
RandomizeProvinceNames = GenUtils.GetParameter("RandomizeProvinceNames")
FactionsToCreateMin = GenUtils.GetParameter("FactionsToCreateMin")
FactionsToCreateMax = GenUtils.GetParameter("FactionsToCreateMax")
PopsPerProvinceMin = GenUtils.GetParameter("PopsPerProvinceMin")
PopsPerProvinceMax = GenUtils.GetParameter("PopsPerProvinceMax")
CivilizedPercentMin = GenUtils.GetParameter("CivilizedPercentMin")
CivilizedPercentMax = GenUtils.GetParameter("CivilizedPercentMax")
CivilizedPercent = random.randint(CivilizedPercentMin,CivilizedPercentMax)
SlaveryPercentMin = GenUtils.GetParameter("SlaveryPercentMin")
SlaveryPercentMax = GenUtils.GetParameter("SlaveryPercentMax")
SlaveryPercent = random.randint(SlaveryPercentMin,SlaveryPercentMax)
ProvsPerRegionMin = GenUtils.GetParameter("ProvsPerRegionMin")
ProvsPerRegionMax = GenUtils.GetParameter("ProvsPerRegionMax")
#special factions
UnreleasedMin = GenUtils.GetParameter("UnreleasedMin")
UnreleasedMax = GenUtils.GetParameter("UnreleasedMax")
UnreleasedFactionsQty = random.randint(UnreleasedMin,UnreleasedMax)
ChinasMin = GenUtils.GetParameter("ChinasMin")
ChinasMax = GenUtils.GetParameter("ChinasMax")
Chinas = random.randint(ChinasMin,ChinasMax)
SuperpowersMin = GenUtils.GetParameter("SuperpowersMin")
SuperpowersMax = GenUtils.GetParameter("SuperpowersMax")
Superpowers = random.randint(SuperpowersMin,SuperpowersMax)
RussiasMin = GenUtils.GetParameter("RussiasMin")
RussiasMax = GenUtils.GetParameter("RussiasMax")
Russias = random.randint(RussiasMin,RussiasMax)
SecPowersMin = GenUtils.GetParameter("SecPowersMin")
SecPowersMax = GenUtils.GetParameter("SecPowersMax")
SecPowers = random.randint(SecPowersMin,SecPowersMax)
ChanceToEnlargeMin = GenUtils.GetParameter("ChanceToEnlargeMin")
ChanceToEnlargeMax = GenUtils.GetParameter("ChanceToEnlargeMax")
ChanceToEnlarge = random.randint(ChanceToEnlargeMin,ChanceToEnlargeMax)
#Extra provinces qty
UnreleasedProvsMin = GenUtils.GetParameter("UnreleasedProvsMin")
UnreleasedProvsMax = GenUtils.GetParameter("UnreleasedProvsMax")
ProvsPerFactionSmallMin = GenUtils.GetParameter("ProvsPerFactionSmallMin")
ProvsPerFactionSmallMax = GenUtils.GetParameter("ProvsPerFactionSmallMax")
ProvsPerFactionNormalMin = GenUtils.GetParameter("ProvsPerFactionNormalMin")
ProvsPerFactionNormalMax = GenUtils.GetParameter("ProvsPerFactionNormalMax")
ChinaProvsMin = GenUtils.GetParameter("ChinaProvsMin")
ChinaProvsMax = GenUtils.GetParameter("ChinaProvsMax")
SuperpowerProvsMin = GenUtils.GetParameter("SuperpowerProvsMin")
SuperpowerProvsMax = GenUtils.GetParameter("SuperpowerProvsMax")
RussiaProvsMin = GenUtils.GetParameter("RussiaProvsMin")
RussiaProvsMax = GenUtils.GetParameter("RussiaProvsMax")
SecPowerProvsMin = GenUtils.GetParameter("SecPowerProvsMin")
SecPowerProvsMax = GenUtils.GetParameter("SecPowerProvsMax")
#Population
GolbalPopulationMultiplier = GenUtils.GetParameter("GolbalPopulationMultiplier")
UnreleasedPopMultiplierMin = GenUtils.GetParameter("UnreleasedPopMultiplierMin")
UnreleasedPopMultiplierMax = GenUtils.GetParameter("UnreleasedPopMultiplierMax")
ChinaPopMultiplierMin = GenUtils.GetParameter("ChinaPopMultiplierMin")
ChinaPopMultiplierMax = GenUtils.GetParameter("ChinaPopMultiplierMax")
SuperpowerPopMultiplierMin = GenUtils.GetParameter("SuperpowerPopMultiplierMin")
SuperpowerPopMultiplierMax = GenUtils.GetParameter("SuperpowerPopMultiplierMax")
SecPowerPopMultiplierMin = GenUtils.GetParameter("SecPowerPopMultiplierMin")
SecPowerPopMultiplierMax = GenUtils.GetParameter("SecPowerPopMultiplierMax")
RussiaPopMultiplierMin = GenUtils.GetParameter("RussiaPopMultiplierMin")
RussiaPopMultiplierMax = GenUtils.GetParameter("RussiaPopMultiplierMax")
NonColonizedPopMultiplierMin = GenUtils.GetParameter("NonColonizedPopMultiplierMin")
NonColonizedPopMultiplierMax = GenUtils.GetParameter("NonColonizedPopMultiplierMax")
#Technology
Superpower2ndTierTechChance = GenUtils.GetParameter("Superpower2ndTierTechChance")
SecPower2ndTierTechChance = GenUtils.GetParameter("SecPower2ndTierTechChance")
#Factories
SuperpowerFactoriesMin = GenUtils.GetParameter("SuperpowerFactoriesMin")
SuperpowerFactoriesMax = GenUtils.GetParameter("SuperpowerFactoriesMax")
RussiaFactoriesMin = GenUtils.GetParameter("RussiaFactoriesMin")
RussiaFactoriesMax = GenUtils.GetParameter("RussiaFactoriesMax")
SecHasIndustryMin = GenUtils.GetParameter("SecHasIndustryMin")
SecHasIndustryMax = GenUtils.GetParameter("SecHasIndustryMax")
SecHasIndustry = random.randint(SecHasIndustryMin,SecHasIndustryMax)
SecPowerFactoriesMin = GenUtils.GetParameter("SecPowerFactoriesMin")
SecPowerFactoriesMax = GenUtils.GetParameter("SecPowerFactoriesMax")
#Cultures
CultureGroupsMin = GenUtils.GetParameter("CultureGroupsMin")
CultureGroupsMax = GenUtils.GetParameter("CultureGroupsMax")
UnifiableGroups = GenUtils.GetParameter("UnifiableGroups")
FillColonizedProvs = GenUtils.GetParameter("FillColonizedProvs")
UncolonizedGroups = GenUtils.GetParameter("UncolonizedGroups")
IdealUnificationProvinces = GenUtils.GetParameter("IdealUnificationProvinces")
IdealUncolonizedProvinces = GenUtils.GetParameter("IdealUncolonizedProvinces")
CulturesPerGroupMin = GenUtils.GetParameter("CulturesPerGroupMin")
CulturesPerGroupMax = GenUtils.GetParameter("CulturesPerGroupMax")
AcceptedCulturePresenceMinSameGrp = GenUtils.GetParameter("AcceptedCulturePresenceMinSameGrp")
AcceptedCulturePresenceMinOtherGrp = GenUtils.GetParameter("AcceptedCulturePresenceMinOtherGrp")
#liferating
ColonizedLRMin = GenUtils.GetParameter("ColonizedLRMin")
ColonizedLRMax = GenUtils.GetParameter("ColonizedLRMax")
NonColonizedLRMin = GenUtils.GetParameter("NonColonizedLRMin")
NonColonizedLRMax = GenUtils.GetParameter("NonColonizedLRMax")
#Cores
UnifiableRemoveCores = GenUtils.GetParameter("UnifiableRemoveCores")
AddCoresBasedOnCulture = GenUtils.GetParameter("AddCoresBasedOnCulture")
DontAssignCoreIfAccepted = GenUtils.GetParameter("DontAssignCoreIfAccepted")
RemoveCoresIfSameGrp = GenUtils.GetParameter("RemoveCoresIfSameGrp")
RemoveCoresIfOtherGrp = GenUtils.GetParameter("RemoveCoresIfOtherGrp")
#1.34
SwedensMin = GenUtils.GetParameter("SwedensMin")
SwedensMax = GenUtils.GetParameter("SwedensMax")
JapansMin = GenUtils.GetParameter("JapansMin")
JapansMax = GenUtils.GetParameter("JapansMax")
SwedenProvsMin = GenUtils.GetParameter("SwedenProvsMin")
SwedenProvsMax = GenUtils.GetParameter("SwedenProvsMax")
JapanProvsMin = GenUtils.GetParameter("JapanProvsMin")
JapanProvsMax = GenUtils.GetParameter("JapanProvsMax")
SwedenPopMultiplierMin = GenUtils.GetParameter("SwedenPopMultiplierMin")
SwedenPopMultiplierMax = GenUtils.GetParameter("SwedenPopMultiplierMax")
JapanPopMultiplierMin = GenUtils.GetParameter("JapanPopMultiplierMin")
JapanPopMultiplierMax = GenUtils.GetParameter("JapanPopMultiplierMax")

#how many % of each pop type will there be at game start
#distributions based on the original game
def Artisans():
	return random.uniform(0.01,0.1)
def Clergymen():
	return random.uniform(0.001,0.015)
def Bureaucrats():
	return random.uniform(0.000,0.005)
def Soldiers(Superpower):
	return random.uniform(0.003,0.015)
def Farmers():
	return random.uniform(0.6,0.9)
def Slaves():
	return random.uniform(0.05,0.3)
def Labourers():
	return random.uniform(0.4,0.9)
def Aristocrats():
	return random.uniform(0.001,0.025)
def Capitalists():
	if random.randint(0,100) > 60:
		return random.uniform(0.002,0.005)
	return random.uniform(0.001,0.004)
def Officers():
	return random.uniform(0.0,0.001)
def Craftsmen():
	#only spawns craftsmen in provinces that have factories
	return random.uniform(0.05,0.15)
	

#globals:
ModName = ""

Factions = []
UnreleasedFactions = []
SmallFactions = []
UnificationFactions = []

Cultures = []
CultureGroups = []
UnificationCultureGroups = []
UncolonizedGrps = []
CivilizedGrps = []
UncivilizedGrps = []

Tags = ["CON", "PRN", "AUX", "NUL", "REB"]
Regions = []
AllProvinces = []
ProvinceFiles = []
ColonizableProvinces = []
DictionariesChosen = [] #dictionaries picked, excludes extension (eg. "Portuguese", "OldNorse")

#static:
Governments = ["absolute_monarchy", "democracy", "hms_government", "presidential_dictatorship" ]
NationalValues = [ "nv_order", "nv_liberty", "nv_equality" ]
upper_house_composition = [ "party_appointed", "appointed", "state_equal_weight", "population_equal_weight" ]
public_meetings = [ "no_meeting", "yes_meeting" ]
press_rights = [ "state_press", "censored_press", "free_press" ]
trade_unions = [ "no_trade_unions", "state_controlled", "non_socialist", "all_trade_unions" ]
voting_system = [ "first_past_the_post", "jefferson_method", "proportional_representation" ] 
political_parties = [ "underground_parties", "harassment", "gerrymandering", "non_secret_ballots", "secret_ballots" ]
wage_reform  = [ "no_minimum_wage", "trinket_wage"  ]
work_hours = ["no_work_hour_limit", "fourteen_hours"]
safety_regulations = ["no_safety", "trinket_safety"]
health_care = ["no_health_care", "trinket_health_care"]
unemployment_subsidies = ["no_subsidies", "trinket_subsidies" ]
pensions = ["no_pensions", "trinket_pensions" ]
school_reforms = ["no_schools"]
Factories = [ "furniture_factory", "paper_mill", "fabric_factory", "liquor_distillery", "glass_factory", "luxury_clothes_factory", "luxury_furniture_factory", "steel_factory", "regular_clothes_factory","explosives_factory","winery","cement_factory"] + ["small_arms_factory"]*10 + ["ammunition_factory"]*10 + ["canned_food_factory"]*10 + ["artillery_factory"]*5
#same distribution as the original
NaturalGoods = ["cattle"]*19 + ["coal"]*13 + ["coffee"]*5 + ["cotton"]*8 + ["dye"]*1 + ["grain"]*52 + ["iron"]*8 + ["opium"]*2 + ["fruit"]*19 + ["precious_metal"]*1 + ["wool"]*13 + ["silk"]*2 + ["sulphur"]*3 + ["tea"]*6 + ["timber"]*21 + ["tobacco"]*4 + ["tropical_wood"]*4
LaborerGoods = ["coal","timber", "copper" , "iron" , "lead" ,"sulphur" ,"tropical_wood" ]

PortsTXT = open("Ports.txt",'r').readlines()
AdjacenciesTXT = open("Adjacencies.txt",'r').readlines()
PositionsTXT = open("Positions.txt",'r').readlines()

class Culture:
	CultureName = "" #culture name
	CultureNameTag = ""
	CultureGroup = "" #culture group, taken from the *.names file
	CultureGroupTag = "" #culture group tag
	CultureColor = [] #culture color, RGB tuple
	Civilized = 0
	Religion = "" #culture's religion
	ReligionTag = ""
	TotalProvinces = 0 #how many provinces have this culture
	GraphicalCulture = ""
	Unifiable = 0 #boolean
	UnifiedFaction = 0 #Faction object
	Colonized = 0 #boolean
	def __init__(self, cult, grp, rel, civ):
		self.CultureName = cult
		self.CultureGroup = grp
		self.Religion = rel
		self.Colonized=1
		self.Civilized = civ
		self.CultureColor.append(random.randint(0,255))
		self.CultureColor.append(random.randint(0,255))
		self.CultureColor.append(random.randint(0,255))
		self.CultureGroupTag = GenUtils.remove_accents(grp)+"_grp_tag"
		self.CultureNameTag = GenUtils.remove_accents(cult)+"_tag"
		try:
			GCOptions = open("Generator/CultureGroups/"+grp+".gc",'r').readlines()
			self.GraphicalCulture = random.choice(GCOptions)
			self.GraphicalCulture = self.GraphicalCulture.replace('\n','')
		except:
			self.GraphicalCulture = "Generic"
		if not self.Civilized:
			try:
				GCOptions = open("Generator/CultureGroups/"+grp+".uncivgc",'r').readlines()
				self.GraphicalCulture = random.choice(GCOptions)
				self.GraphicalCulture = self.GraphicalCulture.replace('\n','')
			except:
				pass

class Province:
	ProvinceNumber = 0
	TradeGoods = ""
	Liferating = 0 #determined by its region
	HasShore = 0
	PosX = 0
	PosY = 0
	Owner = 0 #who owns the province (Faction object)
	Cores = [] #list of Factions
	Cultures = [] #Cultures on this province
	CultureAssigned=0 #1if this province's culture was assigned on first phase
	Neighbors = []
	PopMultiplier = [] #PopMultiplier, per-culture
	Colonial=0 #whether this province is someones colony
	RegionAssigned=0 #boolean
	def __init__(self, nr):
		self.ProvinceNumber = nr
		self.Owner=0
		self.Cores = []
		self.Cultures = []
		self.Neighbors = []
		self.PopMultiplier = []
		#discover if this prov has a port
		for Line in PortsTXT:
			if int(Line) == nr:
				self.HasShore=1
				break
		self.TradeGoods = random.choice(NaturalGoods)
		if self.HasShore == 1 and random.randint(0,100)<=22:
			self.TradeGoods = "fish"
	def EmptyNeighbors(self):
		sum=0
		for p in self.Neighbors:
			if p.Owner == 0 and  p.Cultures[0].Colonized:
				sum+= 1
		return sum
	def GetMajorCulture(self):
		return self.Cultures[0]
	def SomebodysCapital(self):
		for f in Factions:
			try:
				if f.ProvincesOwned[0] == self:
					return 1
			except:
				pass
		return 0
	def GetSameCultureNeighbors(self):
		#returns a list of provinces that share the same Culture
		#important: adjacencies list and cultures must have been loaded already
		Provs = [] #this will be returned
		Tested = [] #a list of provinces already tested
		Tested.append(self)
		i = 0
		while i < len(Tested):
			ThisProv = Tested[i]
			if ThisProv.Culture == self.Culture and ThisProv.Owner == 0:
				Provs.append(ThisProv)
			for p in ThisProv.Neighbors:
				if p.Culture == self.Culture and p.Owner == 0:
					Provs.append(p)
				if not p in Tested and p.Owner == 0:
					Tested.append(p)
			i+=1
		#remove duplicates
		Provs2 = []
		for p in Provs:
			if not p in Provs2:
				Provs2.append(p)
		#print(len(Provs2), len(Tested))
		return Provs2, Tested
			
				
		
class Region:
	RegionTag = "" #eg: USA_1
	Provinces = [] #which provinces form this region
	LifeRating = 0
	NumFactories=0 #how many factories are there in this region (shared among owners)
	def __init__(self, tag, provs, lr):
		self.RegionTag = tag
		self.Provinces = provs
		self.LifeRating = lr

class Faction:
	Name = "" #Faction's name
	ProvincesOwned = [] #Provinces this faction owns
	Culture = 0 #this faction's culture
	Prestige = 0 #prestige score
	AcceptedCultures = []
	PoliticalParties = []
	Colors = []
	Tag = "" #this faction's Vic2 tag
	Civilized = 0
	Slavery = "no"
	Government = "absolute_monarchy"
	Type = "" #type of nation: normal, super/seconday power, China, Russia... blank = normal
	PopMultiplier = 1.0
	ExtraProvinces = 0
	PortProvincesNr = [] #number of all provinces that HasShore owned by this faction
	HasIndustry=0
	NumFactories=0
	NumFactoriesToGive=0
	Literacy=0.0 #float
	def __init__(self):
		self.ProvincesOwned = []
		self.PortProvincesNr = []
		self.AcceptedCultures = []
		self.PoliticalParties = []
		self.HasIndustry = 0
		#self.PopMultiplier = random.paretovariate(2)
		self.PopMultiplier = random.expovariate(1.5)+0.2
		self.ExtraProvinces = random.randint(ProvsPerFactionNormalMin,ProvsPerFactionNormalMax)
		if random.randint(0,100)<=ChanceToEnlarge: #some nations had more provinces than avg. (e.g. Persia, Egypt) although not too powerful
			self.ExtraProvinces += random.randint(SecPowerProvsMin,SecPowerProvsMax)
			self.Type = "LargeButWeak"
		self.Colors = GenUtils.GetColors()
		self.Slavery = "no"
		if random.randint(0,100) <= SlaveryPercent:
			self.Slavery = "yes"
		self.Government = random.choice(Governments)
	def HasAnyPort(self):
		for p in self.ProvincesOwned:
			if p.HasShore:
				return 1
		return 0
	def GetRandomProv(self):
		return random.choice(self.ProvincesOwned).ProvinceNumber
	def GetRandomPort(self):
		if len(self.PortProvincesNr) == 0:
			for p in self.ProvincesOwned:
				if p.HasShore:
					self.PortProvincesNr.append(p.ProvinceNumber)
		return random.choice(self.PortProvincesNr)
	#returns the index to Cultures[] of the culture that has the most provinces in this faction
	def GetMajorCultureIndex(self):
		CulturesQty = [0]*len(Cultures)
		#sum up cultures qty per province
		for p in self.ProvincesOwned:
			Ind = GetCultureIndex(p.Cultures[0])
			if Ind != -1 and not p.Colonial:
				CulturesQty[Ind] += 1
		#find the major culture
		Major=-1
		MajorInd=-1
		for i in range(len(CulturesQty)):
			if Major < CulturesQty[i]:
				Major=CulturesQty[i]
				MajorInd=i
		return MajorInd
			
#returns Cult's index on  Cultures[]
def GetCultureIndex(Cult):
	for i in range(len(Cultures)):
		if Cultures[i] == Cult:
			return i
	return -1

#returns approximate distance between two provinces
def DistanceBetween(Prov1, Prov2):
	dx = abs(Prov1.PosX-Prov2.PosX)
	dy = abs(Prov1.PosY-Prov2.PosY)
	dx = int(dx)
	dy = int(dy)
	min=0
	max=0
	if dx < dy:
		min = dx;
		max = dy;
	else:
		min = dy;
		max = dx;
	return ((( max << 8 ) + ( max << 3 ) - ( max << 4 ) - ( max << 1 ) + ( min << 7 ) - ( min << 5 ) + ( min << 3 ) - ( min << 1 )) >> 8 )

def GetFaction(tag):
	for f in Factions:
		if f.Tag == tag:
			return f
	return 0
	
def GetProvince(tag):
	for p in AllProvinces:
		if p.ProvinceNumber == tag:
			return p
	return 0

def GetProvinceRegion(nr):
	for r in Regions:
		for p in r.Provinces:
			if p.ProvinceNumber==nr:
				return r
	return 0
	
def ReadProvincesData():
	global AllProvinces
	print("  Reading adjacencies...")
	i=0
	for p in AllProvinces:
		sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(i)/len(AllProvinces)*100.0))
		i+=1
		for Line in AdjacenciesTXT:
			Line = Line.split()
			if int(Line[0]) == p.ProvinceNumber:
				for j in range(1,len(Line)):
					p.Neighbors.append(GetProvince(int(Line[j])))
				break
	print("  Reading positions...")
	i=0
	for p in AllProvinces:
		sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(i)/len(AllProvinces)*100.0))
		i+=1
		for Line in PositionsTXT:
			Line = Line.split()
			if int(Line[0]) == p.ProvinceNumber:
				p.PosX = float(Line[1])
				p.PosY = float(Line[2])
				break
				
	AllProvinces = sorted(AllProvinces, key=lambda f: f.ProvinceNumber)

#returns the closest province to ThisProv that has >= EmptyNeighbors
def GetNearbyEmptyProv(ThisProv, EmptyNeighbors):
	ClosestDist=999999.0
	Closest=0
	for p in ColonizableProvinces:
		Dist = DistanceBetween(p, ThisProv)
		if ThisProv != p and p.Owner == 0 and p.EmptyNeighbors()>=EmptyNeighbors and Dist < ClosestDist:
			ClosestDist = Dist
			Closest = p
	if Closest == 0 and EmptyNeighbors>1:
		return GetNearbyEmptyProv(ThisProv,EmptyNeighbors-1)
	if Closest != 0:
		return Closest
	return 0

#returns the closest province to ThisProv where RegionAssigned==0, only if ThisProv is an island
def GetNearbyUnassignedProv(ThisProv):
	if len(ThisProv.Neighbors)>0:
		return 0
	ClosestDist=999999.0
	Closest=0
	for p in AllProvinces:
		Dist = DistanceBetween(p, ThisProv)
		if ThisProv != p and p.RegionAssigned == 0  and ThisProv.Cultures[0].CultureGroup == p.Cultures[0].CultureGroup and Dist < ClosestDist and len(p.Neighbors)==0:
			ClosestDist = Dist
			Closest = p
	if ClosestDist < 200.0:
		return Closest
	return 0
	
#returns the closest province to ThisProv that has the same culture
def GetNearbyProvSameCulture(ThisProv):
	ClosestDist=999999.0
	Closest=0
	for p in AllProvinces:
		Dist = DistanceBetween(p, ThisProv)
		if ThisProv != p and ThisProv.Cultures[0].CultureGroup == p.Cultures[0].CultureGroup and Dist < ClosestDist:
			ClosestDist = Dist
			Closest = p
	return Closest
	
def GenerateTag(Name):
	#first try: Name[0:3]
	tag = Name[:3].upper()
	#check if tag exists
	Taken = 0
	for i in range(len(Tags)):
		if Tags[i] == tag:
			Taken = 1
	if Taken == 1:
		Taken = 0
		#second try: Name[size-3:size]
		tag = Name[len(Name)-3:len(Name)].upper()
		for i in range(len(Tags)):
			if Tags[i] == tag:
				Taken = 1
	if Taken == 1 or len(tag)<3 or tag.find(" ") != -1:
		#last try: random
		tag = random.choice(string.ascii_uppercase)
		tag += random.choice(string.ascii_uppercase)
		tag += random.choice(string.ascii_uppercase)
		for i in range(len(Tags)):
			if Tags[i] == tag:
				return GenerateTag(Name)
	#print("Tag for " +Name+ ": " + tag)
	Tags.append(tag)
	return tag

#######################################################
#returns the culture group that has the closest IdealUnificationProvinces as possible
def GetBestUnifiableCulture():
	#sum each culture groups provinces qty
	ProvsSum = []
	for c in Cultures:
		if not c.Unifiable and c.Colonized:
			x=[]
			x.append(c.CultureGroup)
			x.append(0)
			ProvsSum.append(x)
	for p in ColonizableProvinces:
		for s in ProvsSum:
			if p.Cultures[0].CultureGroup == s[0]:
				s[1]+=1
				break
	#find the best one
	ClosestNr=999999
	Closest=0
	for s in ProvsSum:
		if abs(s[1]-IdealUnificationProvinces) < ClosestNr:
			ClosestNr = abs(s[1]-IdealUnificationProvinces)
			Closest = s[0]
	return Closest
		
def CreateCommonCultures():
	File = open("mod/"+ModName+"/common/cultures.txt", "a+")
	File.write("\n\n")
	Written = [0]*len(Cultures)
	for i in range(len(Cultures)):
		sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(i)/len(Cultures)*100.0))
		if not Written[i]:
			File.write("\n"+Cultures[i].CultureGroupTag+" = {\n")
			GroupGraphicalCulture = Cultures[i].GraphicalCulture
			if "American1GC" in GroupGraphicalCulture:
				Portrait="nativeamerican"
			elif "Asian1GC" in GroupGraphicalCulture:
				Portrait="asian"
			elif "African1GC" in GroupGraphicalCulture:
				Portrait="african"
			elif "Arab1GC" in GroupGraphicalCulture:
				Portrait="arab"
			elif "UsGC" in GroupGraphicalCulture:
				Portrait="southamerican"
			elif "Europe2GC" in GroupGraphicalCulture:
				Portrait="russian"
			else:
				Portrait="european"
			File.write("\tleader = "+Portrait+"\n")
			File.write("\tunit = "+GroupGraphicalCulture+"\n")
			for j in range(len(Cultures)):
				if Cultures[j].CultureGroup == Cultures[i].CultureGroup:
					Written[j]=1
					File.write("\t"+Cultures[j].CultureNameTag+" = {\n")
					File.write("\t\tcolor = { "+str(random.randint(0,255))+" "+str(random.randint(0,255))+" "+str(random.randint(0,255))+" }\n")
					File.write("\t\tfirst_names = { ")
					for k in range(50):
						File.write("\""+NameGen.GenerateName(Cultures[i].CultureGroup, True)+"\" ")
					File.write("}\n\t\tlast_names = { ")
					for k in range(50):
						File.write("\""+NameGen.GenerateName(Cultures[i].CultureGroup, False)+"\" ")
					File.write("}\n\t}\n")
			if Cultures[i].Unifiable:
				File.write("\tunion = "+Cultures[i].UnifiedFaction.Tag+"\n")
			File.write("}\n")
	File.close()
#######################################################

def CreateReligionFile():
	RelFile = open("mod/"+ModName+"/common/religion.txt",'w')
	GrpsWritten = []
	for i in range(len(Cultures)):
		CurrGrp = Cultures[i].CultureGroup
		if CurrGrp in GrpsWritten:
			#already written this group
			CurrGrp = ""
		if CurrGrp != "":
			RelFile.write(CurrGrp+"Religion = {\n")
			for j in range(len(Cultures)):
				if Cultures[j].CultureGroup == CurrGrp:
					for o in range(16):
						Cultures[j].ReligionTag += random.choice(string.ascii_lowercase)
					RelFile.write("\t"+Cultures[j].ReligionTag+" = {\n")
					RelFile.write("\t\ticon = "+str(random.randint(1,14))+"\n")
					RelFile.write("\t\tcolor = { "+str(random.uniform(0,1))+" "+str(random.uniform(0,1))+" "+str(random.uniform(0,1))+" }\n")
					RelFile.write("\t}\n")
			GrpsWritten.append(CurrGrp)
			RelFile.write("}\n")

#######################################################
def CreateCommonCountries(ThisFaction):
	File = open("mod/"+ModName+"/common/countries/"+GenUtils.remove_accents(ThisFaction.Name)+".txt", "w")
	File.write("color = { "+str(ThisFaction.Colors[0][0])+" "+str(ThisFaction.Colors[0][1])+" "+str(ThisFaction.Colors[0][2])+" }\n")
	File.write("graphical_culture = "+ThisFaction.Culture.GraphicalCulture+"\n")
	#write political parties
	Parties = []
	try:
		Parties = open("Generator/CultureGroups/"+ThisFaction.Culture.CultureGroup+".pol","r").readlines()
	except:
		Parties = open("Generator/PoliticalParties.default","r").readlines()
	for i in Parties:
		#fill out ThisFaction.PoliticalParties
		if "name" in i:
			ThisFaction.PoliticalParties.append( i.replace(' ','').replace('\n','').replace('\t','').replace('\"','').split('=')[1] ) #ahhhh nothing like solving everything in one line
		#check if the previous political party is available in 1836
		if "start_date" in i:
			if int( i.replace(' ','').replace('\n','').replace('\t','').replace('\"','').split('=')[1].split('.')[0] ) > 1836:
				ThisFaction.PoliticalParties.pop()
		File.write(i)
	#write ships names
	File.write("\nunit_names = {\n")
	ShipTypes = [ "dreadnought", "ironclad", "manowar", "cruiser", "frigate", "monitor" ]
	for s in ShipTypes:
		File.write("\t"+s+" = {\n\t\t")
		for i in range(50):
			File.write("\""+NameGen.GeneratePlaceName(ThisFaction.Culture.CultureGroup,2)+"\" ")
		File.write("\n\t}\n")
	File.write("\n}\n")
#######################################################

def CreateFactionsConstraints():
	global Factions
	NumChinas = 0
	TotalConstraints=0
	while NumChinas < Chinas:
		i = random.randint(0,len(Factions)-1)
		f = Factions[i]
		if f.Type == "" and f.Slavery == "no":
			f.Type = "China"
			f.PopMultiplier = random.uniform(ChinaPopMultiplierMin,ChinaPopMultiplierMax)
			f.ExtraProvinces = random.randint(ChinaProvsMin,ChinaProvsMax)
			#move it to the front, so there will be enough regions to give this faction on distribution
			temp = Factions[TotalConstraints]
			Factions[TotalConstraints] = f
			Factions[i] = temp
			NumChinas += 1
			TotalConstraints+=1
	NumSuperpowers = 0
	while NumSuperpowers < Superpowers:
		i = random.randint(0,len(Factions)-1)
		f = Factions[i]
		if f.Type == "" and f.Slavery == "no":
			f.Type = "Superpower"
			f.Government = "hms_government"
			f.PopMultiplier = random.uniform(SuperpowerPopMultiplierMin,SuperpowerPopMultiplierMax)
			f.HasIndustry = 1
			f.NumFactoriesToGive = random.randint(SuperpowerFactoriesMin,SuperpowerFactoriesMax)
			f.ExtraProvinces = random.randint(SuperpowerProvsMin,SuperpowerProvsMax)
			temp = Factions[TotalConstraints]
			Factions[TotalConstraints] = f
			Factions[i] = temp
			NumSuperpowers += 1
			TotalConstraints += 1
	NumRussias = 0
	while NumRussias < Russias:
		i = random.randint(0,len(Factions)-1)
		f = Factions[i]
		if f.Type == "" and f.Slavery == "no":
			f.Type = "Russia"
			f.Government = "absolute_monarchy"
			f.HasIndustry = 0
			f.NumFactoriesToGive = random.randint(RussiaFactoriesMin,RussiaFactoriesMax)
			if f.NumFactoriesToGive>0:
				f.HasIndustry = 1
			f.PopMultiplier = random.uniform(RussiaPopMultiplierMin,RussiaPopMultiplierMax)
			f.ExtraProvinces = random.randint(RussiaProvsMin,RussiaProvsMax)
			temp = Factions[TotalConstraints]
			Factions[TotalConstraints] = f
			Factions[i] = temp
			NumRussias += 1
			TotalConstraints += 1
	NumSecPowers = 0
	NumSecIndus=0
	while NumSecPowers < SecPowers:
		i = random.randint(0,len(Factions)-1)
		f = Factions[i]
		if f.Type == "":
			f.Type = "SecPower"
			f.Government = random.choice(Governments)
			if NumSecIndus<SecHasIndustry:
				NumSecIndus+=1
				f.HasIndustry = 1
			f.ExtraProvinces = random.randint(SecPowerProvsMin,SecPowerProvsMax)
			f.PopMultiplier = random.uniform(SecPowerPopMultiplierMin,SecPowerPopMultiplierMax)
			if f.HasIndustry == 1:
				f.NumFactoriesToGive = random.randint(SecPowerFactoriesMin,SecPowerFactoriesMax)
			temp = Factions[TotalConstraints]
			Factions[TotalConstraints] = f
			Factions[i] = temp
			NumSecPowers += 1
			TotalConstraints += 1
	NumSwedens = 0	
	Swedens = random.randint(SwedensMin,SwedensMax)
	while NumSwedens < Swedens:
		i = random.randint(0,len(Factions)-1)
		f = Factions[i]
		if f.Type == "":
			f.Type = "Sweden"
			f.Government = random.choice(Governments)
			f.ExtraProvinces = random.randint(SwedenProvsMin,SwedenProvsMax)
			f.PopMultiplier = random.uniform(SwedenPopMultiplierMin,SwedenPopMultiplierMax)
			temp = Factions[TotalConstraints]
			Factions[TotalConstraints] = f
			Factions[i] = temp
			NumSwedens += 1
			TotalConstraints += 1
	NumJapans = 0
	Japans = random.randint(JapansMin,JapansMax)
	while NumJapans < Japans:
		i = random.randint(0,len(Factions)-1)
		f = Factions[i]
		if f.Type == "":
			f.Type = "Japan"
			f.Government = random.choice(Governments)
			f.ExtraProvinces = random.randint(JapanProvsMin,JapanProvsMax)
			f.PopMultiplier = random.uniform(JapanPopMultiplierMin,JapanPopMultiplierMax)
			temp = Factions[TotalConstraints]
			Factions[TotalConstraints] = f
			Factions[i] = temp
			NumJapans += 1
			TotalConstraints += 1
			
	#sort factions by ExtraProvinces
	Factions = sorted(Factions, key=lambda f: f.ExtraProvinces, reverse=True)

#######################################################
def CreateHistoryCountries(ThisFaction):
	if len(ThisFaction.ProvincesOwned) == 0:
		return
	bCivilized=ThisFaction.Civilized
	bSuperpower = ThisFaction.Type == "Superpower"
	bSecPower = ThisFaction.Type == "SecPower" or ThisFaction.Type == "Russia" or ThisFaction.Type == "Sweden"
	if not os.path.exists("mod/"+ModName+"/history/countries/"):
		os.makedirs("mod/"+ModName+"/history/countries/")
	File = open("mod/"+ModName+"/history/countries/"+ThisFaction.Tag+" - "+GenUtils.remove_accents(ThisFaction.Name)+".txt", "w")
	File.write("capital = "+str(ThisFaction.ProvincesOwned[0].ProvinceNumber))
	File.write("\nprimary_culture = "+ThisFaction.Culture.CultureNameTag)
	for c in ThisFaction.AcceptedCultures:
		File.write("\nculture = "+c.CultureNameTag)
	File.write("\nreligion = "+ThisFaction.Culture.ReligionTag+"\n")
	if not bCivilized:
		ThisFaction.Government = "absolute_monarchy"
	Government = ThisFaction.Government
	File.write("government = "+Government+"\n")
	if bCivilized:
		File.write("plurality = "+str(random.randint(0,3))+"\n")
	else:
                File.write("plurality = 0\n")
	File.write("nationalvalue = "+random.choice(NationalValues)+"\n")
	
	if bSuperpower or bSecPower:
		Literacy = "%0.2f" % random.uniform(0.3,0.6)
	if bCivilized and ThisFaction.Type=="Small":
		Literacy = "%0.2f" % random.uniform(0.6,0.8)
	elif ThisFaction.Type == "Sweden":
		Literacy = "%0.2f" % random.uniform(0.7,0.8)
	elif ThisFaction.Type == "Japan":
		Literacy = "%0.2f" % random.uniform(0.35,0.45)
	elif bCivilized:
		Literacy = "%0.2f" % random.uniform(0.15,0.4)
	elif not bCivilized:
		Literacy = "%0.2f" % random.uniform(0.02,0.09)
	ThisFaction.Literacy = float(Literacy)
	File.write("literacy = "+Literacy+"\n")
	
	if ThisFaction.Civilized:
		File.write("\ncivilized = yes\n")
	else:
		File.write("\ncivilized = no\n")
	Prestige=0
	if bCivilized:
		Prestige += random.randint(0,5)
	if bSuperpower or ThisFaction.Type == "Russia":
		Prestige += random.randint(100,120)
	elif bSecPower:
		Prestige += random.randint(30,120)
	ThisFaction.Prestige = Prestige
	File.write("prestige = "+str( Prestige )+"\n\n")
	
	File.write("# Political Reforms\n")
	Slavery = ThisFaction.Slavery+"_slavery"
	File.write("slavery = "+Slavery+"\n")
	File.write("upper_house_composition = "+random.choice(upper_house_composition)+"\n")
	Voting = "none_voting"
	if Government == "democracy" or Government == "hms_government":
		if random.randint(0,100) > 30:
			Voting = "landed_voting"
		else:
			Voting = "universal_weighted_voting"		
	File.write("vote_franschise = "+Voting+"\n")
	if bCivilized: #may give some reforms
		File.write("public_meetings = "+random.choice(public_meetings)+"\n")
		File.write("press_rights = "+random.choice(press_rights)+"\n")
		File.write("trade_unions = "+random.choice(trade_unions)+"\n")
		File.write("voting_system = "+random.choice(voting_system)+"\n")
		File.write("political_parties = "+random.choice(political_parties)+"\n")
		
		File.write("\n# Social Reforms\n")
		File.write("wage_reform = "+random.choice(wage_reform)+"\n")
		File.write("work_hours = "+random.choice(work_hours)+"\n")
		File.write("safety_regulations = "+random.choice(safety_regulations)+"\n")
		File.write("health_care = "+random.choice(health_care)+"\n")
		File.write("unemployment_subsidies = "+random.choice(unemployment_subsidies)+"\n")
		File.write("pensions = "+random.choice(pensions)+"\n")
	else: #no reforms
		File.write("public_meetings = "+public_meetings[0]+"\n")
		File.write("press_rights = "+press_rights[0]+"\n")
		File.write("trade_unions = "+trade_unions[0]+"\n")
		File.write("voting_system = "+voting_system[0]+"\n")
		File.write("political_parties = "+political_parties[0]+"\n")
		
		File.write("\n# Social Reforms\n")
		File.write("wage_reform = "+wage_reform[0]+"\n")
		File.write("work_hours = "+work_hours[0]+"\n")
		File.write("safety_regulations = "+safety_regulations[0]+"\n")
		File.write("health_care = "+health_care[0]+"\n")
		File.write("unemployment_subsidies = "+unemployment_subsidies[0]+"\n")
		File.write("pensions = "+pensions[0]+"\n")
	File.write("school_reforms = "+school_reforms[0]+"\n")
	
	File.write("\n# Voting:\n")
	ChosenRulingParty = random.choice(ThisFaction.PoliticalParties)
	if Government == "presidential_dictatorship":
		for g in ThisFaction.PoliticalParties:
			if "react" in g:
				ChosenRulingParty = g
	File.write("ruling_party = "+ChosenRulingParty+"\n")
	File.write("last_election = "+str(random.randint(1830,1835))+"."+str(random.randint(1,12))+"."+str(random.randint(1,28))+"\n")
	File.write("upper_house = {\n")
	File.write("\tfascist = 0\n")
	File.write("\tanarcho_liberal  = 0\n")
	File.write("\tsocialist = 0\n")
	File.write("\tcommunist = 0\n")
	Liberal = random.randint(0,15)
	Reactionary = random.randint(0,10)
	File.write("\tliberal = "+str(Liberal)+"\n")
	File.write("\treactionary = "+str(Reactionary)+"\n")
	File.write("\tconservative = "+str(100-Liberal-Reactionary)+"\n")
	File.write("}\n")
	
	File.write("\n# Techs:\n")
	#military
	if bCivilized or random.randint(0,100)>40:
		File.write("post_napoleonic_thought = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("strategic_mobility = 1\n")
	if bCivilized or random.randint(0,100)>40:
		File.write("flintlock_rifles = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("muzzle_loaded_rifles = 1\n")
	if random.randint(0,100)>40 and bCivilized or bSuperpower or bSecPower:
		File.write("bronze_muzzle_loaded_artillery = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("iron_muzzle_loaded_artillery = 1\n")
	if random.randint(0,100)>40 and bCivilized or bSuperpower or bSecPower:
		File.write("military_staff_system = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("military_plans = 1\n")
	if random.randint(0,100)>50 and bCivilized or bSuperpower or bSecPower:
		File.write("army_command_principle = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("army_professionalism = 1\n")
		
	#navy
	File.write("post_nelsonian_thought = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("battleship_column_doctrine = 1\n")
	if random.randint(0,100)>50 and bCivilized or bSuperpower or bSecPower:
		File.write("clipper_design = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("steamers = 1\n")
		File.write("commerce_raiders = yes\n")
	if random.randint(0,100)>60 and bCivilized or bSuperpower or bSecPower:
		File.write("naval_design_bureaus = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("fire_control_systems = 1\n")
	if random.randint(0,100)>70 and bCivilized or bSuperpower or bSecPower:
		File.write("alphabetic_flag_signaling = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("naval_plans = 1\n")
	if random.randint(0,100)>60 and bCivilized or bSuperpower or bSecPower:
		File.write("the_command_principle = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("naval_professionalism = 1\n")
		
	#commerce
	if bCivilized or random.randint(0,100)>40 or bSuperpower:
		File.write("private_banks = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("stock_exchange = 1\n")
	if bCivilized or random.randint(0,100)>40 or bSuperpower:
		File.write("no_standard = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("ad_hoc_money_bill_printing = 1\n")
	if bCivilized or random.randint(0,100)>40 or bSuperpower:
		File.write("early_classical_theory_and_critique = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("late_classical_theory = 1\n")
	if bCivilized:
		File.write("freedom_of_trade = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("market_structure = 1\n")
	if random.randint(0,100)>50 and bCivilized or bSuperpower or bSecPower:
		File.write("guild_based_production = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("organized_factories = 1\n")
	
	#culture
	if bCivilized or random.randint(0,100)>40:
		File.write("classicism_n_early_romanticism = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("romanticism = 1\n")
	if bCivilized or random.randint(0,100)>40:
		File.write("late_enlightenment_philosophy = 1\n")
	if random.randint(0,100)>20 and bCivilized or bSuperpower or bSecPower:
		File.write("malthusian_thought = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("positivism = 1\n")
	if random.randint(0,100)>20 and bCivilized or bSuperpower or bSecPower:
		File.write("enlightenment_thought = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("ideological_thought = 1\n")
	if random.randint(0,100)>20 and bCivilized or bSuperpower or bSecPower:
		File.write("introspectionism = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("associationism = 1\n")
	
	#industry
	if bCivilized or random.randint(0,100)>40:
		File.write("water_wheel_power = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("practical_steam_engine = 1\n")
	if bCivilized or random.randint(0,100)>40:
		File.write("publishing_industry = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("mechanical_production = 1\n")
	if random.randint(0,100)>40 and bCivilized or bSuperpower or bSecPower:
		File.write("mechanized_mining = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("clean_coal = 1\n")
	if random.randint(0,100)>60 and bCivilized or bSuperpower or bSecPower:
		File.write("experimental_railroad = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("early_railroad = 1\n")
	if random.randint(0,100)>20 and bCivilized or bSuperpower or bSecPower:
		File.write("basic_chemistry = 1\n")
	if (bSuperpower and random.randint(0,100)<=Superpower2ndTierTechChance) or (bSecPower and random.randint(0,100)<=SecPower2ndTierTechChance):
		File.write("medicine = 1\n")
	
	if bCivilized:
		File.write("\nconsciousness  = "+str(random.randint(0,3))+"\n")
		File.write("nonstate_consciousness  = "+str(random.randint(0,2))+"\n\n")
	else:
		File.write("\nconsciousness  = "+str(random.randint(0,1))+"\n")
		File.write("nonstate_consciousness  = "+str(random.randint(0,0))+"\n\n")
		
	if ThisFaction.Type != "Unreleased":
		CreateOOB(ThisFaction)
		File.write("\noob = \""+ThisFaction.Tag+"_oob.txt\"\n")

#######################################################

#######################################################
def GetRandomDictionary():
	AvailableDicts = glob.glob("Generator/CultureGroups/*.names1")
	for i in range(len(AvailableDicts)): 
		#strip path and extension
		AvailableDicts[i] = AvailableDicts[i][AvailableDicts[i].find("\\")+1:AvailableDicts[i].find(".names1")]
	return random.choice(AvailableDicts)
	
def CreateModName():
	Prefixes = open("Generator/ModNamePrefixes.txt",'r').readlines()
	Things = open("Generator/ModNameThings.txt",'r').readlines()
	People = open("Generator/ModNamePeople.txt",'r').readlines()
	Adj = open("Generator/ModNameAdj.txt",'r').readlines()
	Things += People
	
	RandomDict = GetRandomDictionary()
	
	Name = random.choice(Prefixes)
	
	Name = Name.replace("$city$",NameGen.GeneratePlaceName(RandomDict,0))
	
	Name = Name.replace("$name$",NameGen.GenerateName(RandomDict,0))
	Name = Name.replace("$people$",random.choice(People))
	
	Name = Name.replace("$adj$",random.choice(Adj))
	Name = Name.replace("$adj2$",random.choice(Adj))
	
	Name = Name.replace("$thing$",random.choice(Things))
	Name = Name.replace("$thing2$",random.choice(Things))
	
	ThingPlural = random.choice(Things)
	if ThingPlural[len(ThingPlural)-2] == 's':
		ThingPlural += "es"
	else:
		ThingPlural += "s"
	Name = Name.replace("$things$",ThingPlural)
	ThingPlural = random.choice(Things)
	if ThingPlural[len(ThingPlural)-2] == 's':
		ThingPlural += "es"
	else:
		ThingPlural += "s"
	Name = Name.replace("$things2$",ThingPlural)
	
	Name = Name.replace('\n','')
		
	return Name

def Startup():
	global ModName
	
	#Now = datetime.datetime.now()
	#ModName = "RndWorld "+str(Now.year) +"_"+str(Now.month) +"_"+ str(Now.day) +" "+str(Now.hour)+"h "+str(Now.minute)+"min"
	ModName = "Rnd "
	ModName += CreateModName()
	
	os.chdir("mod")
	ModFolder = GenUtils.remove_accents(ModName)
	ModFolder = ModName.replace(' ','_')
	os.mkdir(ModFolder)
	
	print("Copying standard files...")
	os.chdir("../Generator")
	
	dir_util.copy_tree("standard", "../mod/"+ModFolder)
	
	os.chdir("../mod")
	ModFile = open(ModFolder+".mod",'w')
	ModFile.write("name = \""+ModName+"\"")
	ModFile.write("\npath = \"mod/"+ModFolder+"\"")
	ModFile.write("\nuserdir = \""+ModFolder+"\"")
	ModFile.write("\nreplace_path = \"history/pops/1836.1.1\"")
	os.chdir("../")
	if not os.path.exists("mod/"+ModFolder+"/localisation"):
		os.mkdir("mod/"+ModFolder+"/localisation/")
	File = open("mod/"+ModFolder+"/localisation/0random.csv",'w')
	File.write("GC_NAME;"+ModName[4:]+";;;;;;;;;;;;;x;;;;")
	
	ModName = ModFolder
	
	#not yet developed
	#GenUtils.CreateLoadingScreens(ModFolder)
	
	#initialize Tags vector with already used tags
	os.chdir("history/countries")
	List = glob.glob("*.txt")
	for i in List:
		Tags.append(i[:3])
	os.chdir("../../")
	
	#fill ProvinceFiles
	os.chdir("history/provinces")
	dirs = glob.glob("*")
	for dir in dirs:
		os.chdir(dir)
		files = glob.glob("*.txt")
		for f in files:
			ProvinceFiles.append(dir+"/"+f)
		os.chdir("../")
	os.chdir("../../")
		
#######################################################
def CreateOOB(ThisFaction):
	bCivilized = ThisFaction.Civilized
	bSuperpower = ThisFaction.Type == "Superpower"
	bSecPower = ThisFaction.Type == "SecPower" or ThisFaction.Type == "Russia" or ThisFaction.Type == "Sweden"
	bChina = ThisFaction.Type == "China"
	bRussia = ThisFaction.Type == "Russia"
	
	oob = open("mod/"+ModName+"/history/units/"+ThisFaction.Tag+"_oob.txt","w")
	
	TotalInf=1
	TotalCav=1
	TotalArt=1
	ArmiesToCreate=1
	if bCivilized:
		ArmiesToCreate += random.randint(1,2)
	if bSuperpower:
		ArmiesToCreate += random.randint(8,8)
	if bSecPower:
		ArmiesToCreate += random.randint(4,6)
	if bChina:
		ArmiesToCreate += random.randint(13,13)
	if bRussia:
		ArmiesToCreate += random.randint(10,10)
		
	for j in range(ArmiesToCreate):	
		Units = 0
		if bCivilized:
			Units += random.randint(0,2)
		else:
			Units += random.randint(0,1)
		if bSuperpower:
			Units += random.randint(1,5)
		if bSecPower:
			Units += random.randint(0,1)
		if bChina:
			Units += random.randint(5,10)
		if Units>0:
			oob.write("\narmy = {\n")
			oob.write("\tname = \""+str(j+1)+". Division\"\n")
			oob.write("\tlocation = "+str(ThisFaction.GetRandomProv())+"\n")
			#add infantry
			for i in range(Units):
				oob.write("\tregiment = {\n")
				oob.write("\t\tname = \""+str(TotalInf)+". Infantry\"\n")
				if bCivilized:
					oob.write("\t\ttype = infantry\n")
				else:
					oob.write("\t\ttype = irregular\n")
				oob.write("\t\thome = "+str(random.choice(ThisFaction.ProvincesOwned).ProvinceNumber)+"\n")
				TotalInf+=1
				oob.write("\t}\n")
			if bCivilized:
				#add cavalry
				Cav = 0
				if bSuperpower:
					Cav += random.randint(0,2)
				else:
					Cav += random.randint(0,1)
				for i in range(Cav):
					oob.write("\tregiment = {\n")
					oob.write("\t\tname = \""+str(TotalCav)+". Cavalry\"\n")
					oob.write("\t\ttype = cavalry\n")
					oob.write("\t\thome = "+str(random.choice(ThisFaction.ProvincesOwned).ProvinceNumber)+"\n")
					TotalCav+=1
					oob.write("\t}\n")
				#add artillery
				Artil = 0
				if bSuperpower:
					Artil += random.randint(0,2)
				else:
					Artil += random.randint(0,1)
				for i in range(Artil):
					oob.write("\tregiment = {\n")
					oob.write("\t\tname = \""+str(TotalArt)+". Artillery\"\n")
					oob.write("\t\ttype = artillery\n")
					oob.write("\t\thome = "+str(random.choice(ThisFaction.ProvincesOwned).ProvinceNumber)+"\n")
					TotalArt+=1
					oob.write("\t}\n")
			oob.write("}\n")

	#add ships
	Fleets=1
	FleetsToCreate=0
	if random.randint(0,100)>=10:
		FleetsToCreate=1
	if bCivilized and random.randint(0,100)<=50:
		FleetsToCreate+=1
	if bSuperpower:
		FleetsToCreate+= random.randint(8,8)
	if bRussia:
		FleetsToCreate+= random.randint(5,5)
	if bSecPower:
		FleetsToCreate += random.randint(0,2)
		if ThisFaction.HasIndustry:
			FleetsToCreate += random.randint(4,4)
	if bChina:
		FleetsToCreate+=1
		
	if ThisFaction.HasAnyPort() and FleetsToCreate>0:
		Prefix = ""
		if ThisFaction.Government == "hms_government" or ThisFaction.Government == "absolute_monarchy":
			Prefix = "HMS "
		for j in range(FleetsToCreate):
			oob.write("\nnavy = {\n")
			oob.write("\tname = \""+str(Fleets)+". Fleet\"\n")
			Fleets+=1
			oob.write("\tlocation = "+str(ThisFaction.GetRandomPort())+"\n")
			Manowars=0
			if bSuperpower:
				Manowars = random.randint(6,10)
			if bRussia:
				Manowars = random.randint(3,6)
			if bSecPower:
				Manowars = random.randint(0,2)
			if bChina:
				Manowars = random.randint(0,2)
			for i in range(Manowars):
				oob.write("\tship = {\n")
				oob.write("\t\tname = \""+Prefix+NameGen.GeneratePlaceName(ThisFaction.Culture.CultureGroup)+"\"\n")
				oob.write("\t\ttype = manowar\n")
				oob.write("\t}\n")
			Frigates=0
			if bSuperpower:
				Frigates = random.randint(5,10)
			if bSecPower:
				Frigates = random.randint(0,2)
			if bRussia:
				Frigates = random.randint(0,6)
			if bChina:
				Frigates = random.randint(0,5)
			for i in range(Frigates):
				oob.write("\tship = {\n")
				oob.write("\t\tname = \""+Prefix+NameGen.GeneratePlaceName(ThisFaction.Culture.CultureGroup)+"\"\n")
				oob.write("\t\ttype = frigate\n")
				oob.write("\t}\n")
			Transp=1
			if bSuperpower:
				Transp = random.randint(5,10)
			if bSecPower:
				Transp = random.randint(1,6)
			if bChina:
				Transp = random.randint(1,3)
			for i in range(Transp): #transport
				oob.write("\tship = {\n")
				oob.write("\t\tname = \""+str(i+1)+". Transport Flotilla\"\n")
				oob.write("\t\ttype = clipper_transport\n")
				oob.write("\t}\n")
			oob.write("}\n")

	
#returns the path (string) to province p, e.g. "mod/ModName/history/provinces/asia/23 - Blah.txt"
#p is a string, e.g. "23"
def FindProvinceFile(p):
	for f in ProvinceFiles:
		a = f.find("/")
		g = f[a+1:]
		b = g.find(" ")
		if g[:b] == p:
			return "mod/"+ModName+"/history/provinces/"+f
	
#######################################################
def ChangeProvinceOwnership(p):
	ProvinceFile = open(FindProvinceFile(str(p.ProvinceNumber)),'w')
	#life rating
	ProvinceFile.write("trade_goods = "+p.TradeGoods+"\n")
	p.Liferating = GetProvinceRegion(p.ProvinceNumber).LifeRating
	ProvinceFile.write("life_rating = "+str(p.Liferating)+"\n")
	#owner and controller:
	if p.Owner != 0:
		ProvinceFile.write("owner = "+p.Owner.Tag+"\n")
		ProvinceFile.write("controller = "+p.Owner.Tag+"\n")
	#cores:
	for Core in p.Cores:
		ProvinceFile.write("add_core = "+Core.Tag+"\n")
	#colonial?
	if p.Colonial:
		ProvinceFile.write("colonial = 2\n")
				
#######################################################

#######################################################
def CreateFactory(ThisProvince):
#	os.chdir("mod/"+ModName+"/history/provinces")
#	for File in ProvinceFiles:
#		FileNumber = File[File.find("/")+1:]
#		FileNumber = File[:File.find("-")-1]
#		print(FileNumber)
#		FileNumber = int(FileNumber)
#		if FileNumber == ThisProvince.ProvinceNumber:
#			ProvinceFile = open(File, "a+")
	ProvinceFile = open(FindProvinceFile(str(ThisProvince.ProvinceNumber)),'a+')
	FacType = random.choice(Factories)
	if ThisProvince.HasShore == 1 and random.randint(0,100)<=10:
		FacType = "clipper_shipyard"
	if ThisProvince.TradeGoods == "timber" and random.randint(0,100)<=30:
		FacType = "lumber_mill"
	ProvinceFile.write("\nstate_building = {\n\tlevel = 1\n\tbuilding = ")
	ProvinceFile.write(FacType)
	ProvinceFile.write("\n\tupgrade = yes\n}\n")
	#print("Created a "+FacType+" factory on "+str(ThisProvince.ProvinceNumber))

#######################################################

#######################################################
def CreatePops():
	if not os.path.exists("mod/"+ModName+"/history/pops/1836.1.1"):
		os.makedirs("mod/"+ModName+"/history/pops/1836.1.1")
	File = open("mod/"+ModName+"/history/pops/1836.1.1/pops.txt","w")
	for ThisProvince in AllProvinces:
		ThisRegion = GetProvinceRegion(ThisProvince.ProvinceNumber)
		ThisFaction=0
		Rel = ThisProvince.Cultures[0].ReligionTag
		bSuperpower=0
		bSecPower=0
		bSlavery=0
		bIndus=0
		PopMultiplier=1.0
		PercentCapitalists = 0.0
		File.write("\n"+str(ThisProvince.ProvinceNumber)+" = {")
		try:
			ThisFaction = ThisProvince.Owner
			PopMultiplier = ThisFaction.PopMultiplier
			if ThisProvince.Owner.Slavery == "yes":
				bSlavery=1
			if ThisFaction.Type == "Superpower":
				PercentCapitalists = Capitalists()
			elif ThisFaction.Type == "SecPower" and ThisFaction.HasIndustry:
				PercentCapitalists = Capitalists()
			else:
				PercentCapitalists = 0.0
			if ThisFaction.Civilized == 0:
				PercentCapitalists = 0.0
			if ThisFaction.Type == "Superpower":
				bSuperpower=1
			if ThisFaction.Type == "SecPower" or ThisFaction.Type == "Russia" or ThisFaction.Type == "Sweden":
				bSecPower=1
			if ThisFaction.HasIndustry:
				bIndus=1
		except: #not colonized
			PercentCapitalists = 0.0
			
		
		BaseProvincePopulation = random.randint(PopsPerProvinceMin, PopsPerProvinceMax)*GolbalPopulationMultiplier
		ProvCulture = ""
		for i in range(len(ThisProvince.Cultures)):
			ProvCulture = ThisProvince.Cultures[i].CultureNameTag
			try:
				ProvincePopulation = BaseProvincePopulation * ThisProvince.Owner.PopMultiplier
			except: #not colonized
				ProvincePopulation = BaseProvincePopulation*random.uniform(NonColonizedPopMultiplierMin,NonColonizedPopMultiplierMax)
			ProvincePopulation = int(ProvincePopulation)
			if bSlavery and i==0:
				File.write("\n\tslaves = {\n\t\tculture = "+ProvCulture+"\n\t\treligion = "+Rel+"\n\t\tsize = "+str(int(Slaves()*ProvincePopulation))+"\n\t}")
			File.write("\n\tartisans = {\n\t\tculture = "+ProvCulture+"\n\t\treligion = "+Rel+"\n\t\tsize = "+str(int(Artisans()*ProvincePopulation))+"\n\t}")
			File.write("\n\tclergymen = {\n\t\tculture = "+ProvCulture+"\n\t\treligion = "+Rel+"\n\t\tsize = "+str(int(Clergymen()*ProvincePopulation))+"\n\t}")
			File.write("\n\tbureaucrats = {\n\t\tculture = "+ProvCulture+"\n\t\treligion = "+Rel+"\n\t\tsize = "+str(int(Bureaucrats()*ProvincePopulation))+"\n\t}")
			File.write("\n\tsoldiers = {\n\t\tculture = "+ProvCulture+"\n\t\treligion = "+Rel+"\n\t\tsize = "+str(int(Soldiers(bSuperpower)*ProvincePopulation))+"\n\t}")
			
			if ThisProvince.TradeGoods in LaborerGoods:
				File.write("\n\tlabourers = {\n\t\tculture = "+ProvCulture+"\n\t\treligion = "+Rel+"\n\t\tsize = "+str(int(Labourers()*ProvincePopulation))+"\n\t}")
			else:
				File.write("\n\tfarmers = {\n\t\tculture = "+ProvCulture+"\n\t\treligion = "+Rel+"\n\t\tsize = "+str(int(Farmers()*ProvincePopulation))+"\n\t}")
			
			File.write("\n\taristocrats = {\n\t\tculture = "+ProvCulture+"\n\t\treligion = "+Rel+"\n\t\tsize = "+str(int(Aristocrats()*ProvincePopulation))+"\n\t}")
			if PercentCapitalists > 0.0 and i==0:
				try:
					if ThisFaction.NumFactories<ThisFaction.NumFactoriesToGive and ThisRegion.NumFactories<random.randint(1,3):
						NrCraftsmen=0
						NrCraftsmen = int(Craftsmen()*ProvincePopulation)
						ThisFaction.NumFactories+=1
						ThisRegion.NumFactories += 1
						CreateFactory(ThisProvince)
						File.write("\n\tcraftsmen = {\n\t\tculture = "+ProvCulture+"\n\t\treligion = "+Rel+"\n\t\tsize = "+str(NrCraftsmen)+"\n\t}")
						File.write("\n\tcapitalists = {\n\t\tculture = "+ProvCulture+"\n\t\treligion = "+Rel+"\n\t\tsize = "+str(int(PercentCapitalists*ProvincePopulation))+"\n\t}")
				except:
					print(ThisProvince.ProvinceNumber)
			File.write("\n\tofficers = {\n\t\tculture = "+ProvCulture+"\n\t\treligion = "+Rel+"\n\t\tsize = "+str(int(Officers()*ProvincePopulation))+"\n\t}\n")				
		File.write("}\n")
#######################################################
def GetClosestProvinceWithoutCulture(Prov):
	ClosestDist = 999999.0
	Closest = 0
	for p in AllProvinces:
		Dist = DistanceBetween(p,Prov)
		if Prov != p and Dist < ClosestDist and len(p.Cultures)==0:
			ClosestDist = Dist
			Closest = p
	return Closest
	
#returns the closest culture to ThisProv
def GetClosestCulture(ThisProv):
	ClosestDist = 999999.0
	Closest = 0
	for p in AllProvinces:
		Dist = DistanceBetween(p,ThisProv)
		if ThisProv != p and Dist < ClosestDist and p.CultureAssigned:
			ClosestDist = Dist
			Closest = p
	return Closest.Cultures[0]

def GetNeighborCulture(ThisProv):
	for p in ThisProv.Neighbors:
		if len(p.Cultures)!=0:
			return p.Cultures[0]
	return 0

#returns the best place for this culture to start spreading
def GetBestOrigin(Cult):
	#attempt to get a province that is close to another culture of the same group
	for p in AllProvinces:
		if len(p.Cultures)>0:
			if p.Cultures[0].CultureGroup == Cult.CultureGroup:
				return GetClosestProvinceWithoutCulture(p)
	#if not foud, return a random empty province
	p = random.choice(AllProvinces)
	while len(p.Cultures) != 0:
		p = random.choice(AllProvinces)
	return p
	
#picks culture groups that have the closest IdealUncolonizedProvinces as possible, and changes their Colonized=0
def PickUncolonizedCultures():
	Total = UncolonizedGroups
	if Total > len(DictionariesChosen)-1: #-1 because at least one culture group must be colonizable
		Total = len(DictionariesChosen)-1
	for i in range(Total):
		#sum each culture groups provinces qty
		ProvsSum = []
		for c in Cultures:
			if not c.Unifiable and c.Colonized:
				x=[]
				x.append(c.CultureGroup)
				x.append(0)
				ProvsSum.append(x)
		for p in AllProvinces:
			for s in ProvsSum:
				if p.Cultures[0].CultureGroup == s[0]:
					s[1]+=1
					break
		#find the best one
		ClosestNr=999999
		Closest=0
		for s in ProvsSum:
			if abs(s[1]-IdealUncolonizedProvinces) < ClosestNr:
				ClosestNr = abs(s[1]-IdealUncolonizedProvinces)
				#print(s[1])
				Closest = s[0]
		#found the best culture group, update now
		for c in Cultures:
			if c.CultureGroup == Closest:
				c.Colonized=0
		UncolonizedGrps.append(Closest)
		
				
#attempts to distribute cultures so they are in about the same area
def DistributeCultures():
	print("  Phase 1/2...")
	ProvsPerCulture = (len(AllProvinces)/len(Cultures))# - 1 #-1 to prevent rounding errors
	j=0
	for c in Cultures:
		#pick a random province from which this culture will spread out
		Given=0
		OriginProv = GetBestOrigin(c)
		p = OriginProv
		p.Cultures.append(c)
		p.CultureAssigned=1
		CulturesProvs = []
		CulturesProvs.append(p)
		for p in CulturesProvs:
			sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(Given+(j*ProvsPerCulture))/len(AllProvinces)*100.0))
			for neighbor in p.Neighbors:
				try:
					if len(neighbor.Cultures) == 0 and Given<ProvsPerCulture:
						neighbor.Cultures.append(c)
						neighbor.CultureAssigned=1
						CulturesProvs.append(neighbor)
						Given+=1
				except:
					print("The file map/region.txt seems to be corrupt. Please copy the map/region.txt file from another Vic2 installation into this one and try again.")
					input("Press enter to exit.")
					return

		j+=1
	print("  Phase 2/2...")
	j=0
	for p in AllProvinces:
		sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(j)/len(AllProvinces)*100.0))
		if len(p.Cultures)==0:
			p.Cultures.append(GetClosestCulture(p))
			p.CultureAssigned=0
		j+=1
		
	#pick the best uncolonized culture groups
	PickUncolonizedCultures()
	
	#update colonizable provinces list
	for p in AllProvinces:
		if p.Cultures[0].Colonized:
			ColonizableProvinces.append(p)
			
	if DEBUG_CULT_POS:
		for p in AllProvinces:
			for i in range(len(Cultures)):
				if Cultures[i] == p.Cultures[0]:
					Factions[i].Name = Cultures[i].CultureGroup+" "+Cultures[i].CultureName
					Factions[i].Culture = Cultures[i]
					Factions[i].Tag = GenerateTag(GenUtils.remove_accents(Factions[i].Name))
					Factions[i].ProvincesOwned.append(p)
					p.Owner = Factions[i]
					p.Cores.append(Factions[i])
#######################################################
def RandomizeRegions():
	global Regions
	print("  Phase 1/2...")
	i=0
	for p in AllProvinces:
			sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(i)/len(AllProvinces)*100.0))
			i+=1
			if p.RegionAssigned==0:
				Provs = []
				ProvsGiven = []
				ProvsGiven.append(p)
				Given=0
				LifeRating=0
				ExtraProvsQty = random.randint(ProvsPerRegionMin,ProvsPerRegionMax)
				while Given<ExtraProvsQty:
					for p in ProvsGiven:
						if not p.RegionAssigned and Given<ExtraProvsQty and ProvsGiven[0].Cultures[0].CultureGroup == p.Cultures[0].CultureGroup:
							p.RegionAssigned = 1
							Provs.append(p)
							Given+=1				
						for neighbor in p.Neighbors:
							if not neighbor.RegionAssigned and Given<ExtraProvsQty and ProvsGiven[0].Cultures[0].CultureGroup == neighbor.Cultures[0].CultureGroup:
								neighbor.RegionAssigned = 1
								ProvsGiven.append(neighbor)
								Provs.append(neighbor)
								Given+=1
					if Given<ExtraProvsQty:
						ProvsGiven = []
						p = GetNearbyUnassignedProv(Provs[0])
						if p == 0:
							break #no more nearby provinces
						ProvsGiven.append(p)
				if Provs[0].GetMajorCulture().Colonized:
					LifeRating = random.randint(ColonizedLRMin,ColonizedLRMax)
				else:
					LifeRating = random.randint(NonColonizedLRMin,NonColonizedLRMax)
				ThisRegion = Region("RND_"+str(Provs[0].ProvinceNumber),Provs, LifeRating)
				Regions.append(ThisRegion)
				
	print("  Phase 2/2...")
	#clean up 1-province regions
	ChangedAny=1
	while ChangedAny:
		i=0
		ChangedAny=0
		for r in Regions:
			i+=1
			sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(i)/len(Regions)*100.0))
			if len(r.Provinces) < ProvsPerRegionMin:
				p = GetNearbyProvSameCulture(r.Provinces[0])
				if p != 0:
					#find to which region 'p' belongs
					for r2 in Regions:
						if p in r2.Provinces:
							r2.Provinces.append(r.Provinces[0])
					r.Provinces.pop(0)
					if len(r.Provinces) == 0:
						Regions.remove(r)
						ChangedAny=1
	if not os.path.exists("mod/"+ModName+"/map"):
		os.mkdir("mod/"+ModName+"/map/")
	f = open("mod/"+ModName+"/map/region.txt",'w')
	for r in Regions:
		f.write("RND_"+str(r.Provinces[0].ProvinceNumber)+" = {")
		for p in r.Provinces:
			f.write(" "+str(p.ProvinceNumber))
		f.write(" }\n")
	f.close()

#######################################################
#returns how many empty (Owner == 0) provinces this Culture has
def GetEmptyProvinces(Cult):
	a=0
	for p in AllProvinces:
		if p.Cultures[0] == Cult and p.Owner == 0:
			a+=1
	return a
	
#returns a list of provinces of the culture that has the most empty provinces
#def GetMostEmptyProvinces():
#	for c in AllCultures:
	
#finds the best province to be this factions capital
def GetBestCapital(Faction):
	Options = []
	#Unreleased factions: any occupied province
	if Faction.Type == "Unreleased":
		for p in ColonizableProvinces:
			if p.Owner != 0:
				Options.append(p)
				
	#Unifiable factions: any province that p.Culture == Faction.Culture
	elif Faction.Type == "Unifiable":
		for p in ColonizableProvinces:
			if p.GetMajorCulture() == Faction.Culture:
				Options.append(p)
				
	#Small factions: any province where p.Culture.CultureGroup is in UnificationCultureGroups and not taken
	elif Faction.Type == "Small":
		for p in ColonizableProvinces:
			if p.GetMajorCulture().CultureGroup in UnificationCultureGroups and p.Owner == 0:
				Options.append(p)
	
	#Superpower/Russias: any civilized and empty province, and not in UnificationCultureGroups, also try to get one with several empty neighbors
	elif Faction.Type == "Superpower" or Faction.Type == "Russia":
		ClampMax=6
		while len(Options)==0 and ClampMax>0:
			for p in ColonizableProvinces:
				if p.GetMajorCulture().Civilized and p.Owner == 0 and not p.GetMajorCulture().CultureGroup in UnificationCultureGroups and p.EmptyNeighbors() >= GenUtils.clamp(Faction.ExtraProvinces,0,ClampMax):
					Options.append(p)
			ClampMax-=1
	
	#SecPower: any civilized and empty province
	elif Faction.Type == "SecPower" or Faction.Type == "Sweden":
		ClampMax=6
		while len(Options)==0 and ClampMax>0:
			for p in ColonizableProvinces:
				if p.GetMajorCulture().Civilized and p.Owner == 0 and p.EmptyNeighbors() >= GenUtils.clamp(Faction.ExtraProvinces,0,ClampMax):
					Options.append(p)
			ClampMax-=1
				
	#China: any non civilized and empty province, and not in UnificationCultureGroups
	elif Faction.Type == "China" or Faction.Type == "Japan":
		ClampMax=6
		while len(Options)==0 and ClampMax>0:
			for p in ColonizableProvinces:
				if not p.GetMajorCulture().Civilized and p.Owner == 0 and not p.GetMajorCulture().CultureGroup in UnificationCultureGroups and p.EmptyNeighbors() >= GenUtils.clamp(Faction.ExtraProvinces,0,ClampMax):
					Options.append(p)
			ClampMax-=1
	#all others: just check if not owned
	else:
		ClampMax=6
		while len(Options)==0 and ClampMax>0:
			for p in ColonizableProvinces:
				if p.Owner == 0 and p.Owner == 0 and p.EmptyNeighbors() >= GenUtils.clamp(Faction.ExtraProvinces,0,ClampMax):
					Options.append(p)
			ClampMax-=1
				
	# Options list is filled, return a random province from it
	if len(Options) == 0:
		return 0
	return random.choice(Options)
	
#distributes provinces to non-Unrealeased factions
def DistributeProvinces(GPsOnly):
	if DEBUG_CULT_POS:
		return
	for i in range(len(Factions)):
		t = Factions[i].Type
		if (GPsOnly and (t == "Superpower" or t=="SecPower" or t=="Russia" or t=="China" or t=="Japan" or t=="Sweden")) or (not GPsOnly and (t=="" or t=="LargeButWeak")):
			sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(i)/len(Factions)*100.0))
			p = GetBestCapital(Factions[i])
			if p != 0:
				ProvsGiven = []
				ProvsGiven.append(p)
				Given=0
				SpreadingOut=0 #will become 1 when this faction spreads out
				ExtraProvsQty = Factions[i].ExtraProvinces
				while Given<ExtraProvsQty:
					for p in ProvsGiven:
						if p.Owner == 0 and Given<ExtraProvsQty:
							p.Owner = Factions[i]
							Factions[i].ProvincesOwned.append(p)
							if SpreadingOut and p.Cultures[0].CultureGroup != Factions[i].ProvincesOwned[0].Cultures[0].CultureGroup:
								p.Colonial = 1
							else:
								p.Cores.append(Factions[i])
							Given+=1				
						for neighbor in p.Neighbors:
							if neighbor.Owner == 0 and Given<ExtraProvsQty and neighbor.Cultures[0].Colonized:
								neighbor.Owner = Factions[i]
								if SpreadingOut and p.Cultures[0].CultureGroup != Factions[i].ProvincesOwned[0].Cultures[0].CultureGroup:
									p.Colonial = 1
								else:
									neighbor.Cores.append(Factions[i])
								Factions[i].ProvincesOwned.append(neighbor)
								ProvsGiven.append(neighbor)
								Given+=1
					#if couldn't assign all required provinces, means the current continent/isle is filled up
					#spread out to somewhere close
					if Given<ExtraProvsQty:
						ProvsGiven = []
						p = GetNearbyEmptyProv(Factions[i].ProvincesOwned[0],GenUtils.clamp(ExtraProvsQty-Given,0,5))
						if p == 0:
							break #no more nearby provinces
						ProvsGiven.append(p)
						SpreadingOut=1

				#fill remaining faction data
				#if Factions[i].Type == "China": #if China, get the culture from its capital, to prevent it being civilized
				Factions[i].Culture = Factions[i].ProvincesOwned[0].Cultures[0]
				#else:
				#	Factions[i].Culture = Cultures[Factions[i].GetMajorCultureIndex()]
				Factions[i].Name = NameGen.GenerateFactionName(Factions[i].Culture.CultureGroup, Factions[i].Culture.CultureName)
				Factions[i].Tag = GenerateTag(GenUtils.remove_accents(Factions[i].Name))
			#else:
			#	print("    Warning: could not find an adequate capital for faction "+str(i)+" (Type: "+Factions[i].Type+"), this faction won't be created.")

def CreateUnreleasedFactions():
	for i in range(len(UnreleasedFactions)):
		sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(i)/len(UnreleasedFactions)*100.0))
		p = GetBestCapital(UnreleasedFactions[i])
		ProvsGiven = []
		ProvsGiven.append(p)
		Given=0
		ExtraProvsQty = UnreleasedFactions[i].ExtraProvinces
		for p in ProvsGiven:
			if p.Owner != 0 and Given<ExtraProvsQty:
				p.Cores.append(UnreleasedFactions[i])
				UnreleasedFactions[i].ProvincesOwned.append(p)
				Given+=1				
			for neighbor in p.Neighbors:
				if neighbor.Owner != 0 and Given<ExtraProvsQty and neighbor.Cultures[0] == p.Cultures[0]:
					neighbor.Cores.append(UnreleasedFactions[i])
					UnreleasedFactions[i].ProvincesOwned.append(neighbor)
					ProvsGiven.append(neighbor)
					Given+=1

		#fill remaining faction data
		UnreleasedFactions[i].Culture = UnreleasedFactions[i].ProvincesOwned[0].Cultures[0]
		UnreleasedFactions[i].Name = NameGen.GenerateFactionName(UnreleasedFactions[i].Culture.CultureGroup, UnreleasedFactions[i].Culture.CultureName)
		UnreleasedFactions[i].Tag = GenerateTag(GenUtils.remove_accents(UnreleasedFactions[i].Name))

def CreateUnificationFactions():
	global UnifiableGroups
	if UnifiableGroups>len(DictionariesChosen) - UncolonizedGroups:
		UnifiableGroups = len(DictionariesChosen) - UncolonizedGroups
	for i in range(UnifiableGroups):
		#get the best culture group
		Grp = GetBestUnifiableCulture()
		if Grp == 0:
			print("    Warning: could not assign all Unifiable factions.")
			return
		#create faction stub
		ThisFaction = Faction()
		ThisFaction.Type = "Unifiable"
		ThisFaction.Civilized = 1
		UnificationFactions.append(ThisFaction)
		UnificationCultureGroups.append(Grp)
		Cult = 0
		for c in Cultures:
			if c.CultureGroup == Grp:
				c.Unifiable = 1
				c.UnifiedFaction=UnificationFactions[i]
				Cult = c
				
		#fill remaining faction data
		UnificationFactions[i].Culture = Cult
		UnificationFactions[i].Name = NameGen.GenerateFactionName(UnificationFactions[i].Culture.CultureGroup, UnificationFactions[i].Culture.CultureName)
		UnificationFactions[i].Tag = GenerateTag(GenUtils.remove_accents(UnificationFactions[i].Name))
		
		p = GetBestCapital(UnificationFactions[i])
		UnificationFactions[i].ProvincesOwned.append(p)
		for p in ColonizableProvinces:
			if UnificationFactions[i].Culture.CultureGroup == p.Cultures[0].CultureGroup:
				p.Cores.append(UnificationFactions[i])

#fills unifiable territories with small factions
def CreateSmallFactions():
	while True:
		#create faction stub
		ThisFaction = Faction()
		ThisFaction.Type = "Small"
		p = GetBestCapital(ThisFaction)
		#check if we still need to create small factions
		if p == 0:
			return
		ThisFaction.Culture = p.GetMajorCulture()
		ThisFaction.ExtraProvinces = random.randint(ProvsPerFactionSmallMin,ProvsPerFactionSmallMax)
		
		SmallFactions.append(ThisFaction)
		ProvsGiven = []
		ProvsGiven.append(p)
		Given=0
		ExtraProvsQty = ThisFaction.ExtraProvinces
		for p in ProvsGiven:
			if p.Owner == 0 and Given<ExtraProvsQty and p.GetMajorCulture() == ThisFaction.Culture:
				p.Owner = ThisFaction
				p.Cores.append(ThisFaction)
				ThisFaction.ProvincesOwned.append(p)
				Given+=1
			for neighbor in p.Neighbors:
				if neighbor.Owner == 0 and Given<ExtraProvsQty and neighbor.GetMajorCulture() == p.GetMajorCulture() and neighbor.GetMajorCulture().Colonized:
					neighbor.Owner = ThisFaction
					neighbor.Cores.append(ThisFaction)
					ThisFaction.ProvincesOwned.append(neighbor)
					ProvsGiven.append(neighbor)
					Given+=1

		#fill remaining faction data
		ThisFaction.Name = NameGen.GenerateFactionName(ThisFaction.Culture.CultureGroup, ThisFaction.Culture.CultureName)
		ThisFaction.Tag = GenerateTag(GenUtils.remove_accents(ThisFaction.Name))		

#returns the faction closest to this province, that is not Small
def GetClosestFaction(ThisProv):
	ClosestDist=999999.0
	Closest=0
	for p in ColonizableProvinces:
		Dist = DistanceBetween(p, ThisProv)
		if ThisProv != p and p.Owner != 0 and Dist < ClosestDist:
			if p.Owner.Type != "Small":
				ClosestDist = Dist
				Closest = p
	return Closest.Owner

#returns the faction closest to this province,  whose owner's culture is Cult
def GetClosestFactionByCulture(ThisProv):
	ClosestDist=999999.0
	Closest=0
	for p in ColonizableProvinces:
		Dist = DistanceBetween(p, ThisProv)
		if ThisProv != p and p.Owner != 0 and Dist < ClosestDist and p.Owner.Culture == ThisProv.GetMajorCulture():
			ClosestDist = Dist
			Closest = p
	if Closest != 0:
		return Closest.Owner
	return 0
	
#gives ownership to colonizable provinces, if they arent owned
def FillGaps():
	i=0
	for p in ColonizableProvinces:
		sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(i)/len(ColonizableProvinces)*100.0))
		if p.Owner == 0:
			f = GetClosestFaction(p)
			p.Owner = f
			p.Cores.append(f)
			f.ProvincesOwned.append(p)
		i+=1
		
def WriteCountryFiles():
	File = open("mod/"+ModName+"/common/countries.txt", "a+")
	i=0
	Facs = Factions+UnreleasedFactions+UnificationFactions+SmallFactions
	for f in Facs:
		sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(i)/len(Facs)*100.0))
		i+=1
		if f.Tag != "":
			f.Civilized = f.Culture.Civilized
			#append faction on common/countries.txt
			File.write("\n"+f.Tag+"\t\t= \"countries/"+GenUtils.remove_accents(f.Name)+".txt\"")

			#create common/countries/*.txt file
			CreateCommonCountries(f)
			
			#create history/countries/*.txt and history/units/*.txt files
			CreateHistoryCountries(f)
		
#######################################################
#removes cores on a given province, when it is unifiable and its owner's culture is not the unifiable faction's culture
def RemoveForeignCoresOnUnifiable():
	for p in ColonizableProvinces:
		try:
			if p.Cores[0].Type == "Unifiable":
				if len(p.Cores)>1 and p.Cores[0].Culture.CultureGroup != p.Owner.Culture.CultureGroup:
					f = p.Cores[0]
					p.Cores = []
					p.Cores.append(f)
		except:
			pass

#figures out if accepted cultures should be added to a faction
def AssignAcceptedCultures():
	for f in Factions:
		CultSum = [0.0]*len(Cultures)
		for p in f.ProvincesOwned:
			if f in p.Cores: #only check if province is in this faction's cores
				i = GetCultureIndex(p.GetMajorCulture())
				if i != -1:
					CultSum[i] += 1.0
		MainCultureIndex = GetCultureIndex(f.Culture)
		#print("Current culture: "+Cultures[MainCultureIndex].CultureName)
		if len(f.ProvincesOwned)>0:
			for i in range(len(Cultures)):
				if i != MainCultureIndex:
					if Cultures[i].CultureGroup == Cultures[MainCultureIndex].CultureGroup and CultSum[i]/CultSum[MainCultureIndex] >= AcceptedCulturePresenceMinSameGrp/100.0:
						f.AcceptedCultures.append(Cultures[i])
						#print("Same grp, "+str(CultSum[i])+" / "+str(CultSum[MainCultureIndex])+" = "+str(CultSum[i]/CultSum[MainCultureIndex])+" - "+Cultures[i].CultureName)
					elif CultSum[i]/CultSum[MainCultureIndex] >= AcceptedCulturePresenceMinOtherGrp/100.0:
						#print("Other grp, "+str(CultSum[i])+" / "+str(CultSum[MainCultureIndex])+" = "+str(CultSum[i]/CultSum[MainCultureIndex])+" - "+Cultures[i].CultureName)
						f.AcceptedCultures.append(Cultures[i])
			
#for each faction, run through its owned provinces. If p.culture != f.culture, then p receives a core from a neighbor where its neighbor.Cultures[0] == p.Cultures[0].
def CheckCores():
	i=0
	for f in Factions:
		sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(i)/len(Factions)*100.0))
		i+=1
		#print("This culture is "+f.Culture.CultureName)
		for p in f.ProvincesOwned:
			ShouldChange=0
			if DontAssignCoreIfAccepted and p.GetMajorCulture() != f.Culture and not p.GetMajorCulture() in f.AcceptedCultures:
				ShouldChange=1
			elif not DontAssignCoreIfAccepted and p.GetMajorCulture() != f.Culture:
				ShouldChange=1
			if ShouldChange:
				RightfulOwner = GetClosestFactionByCulture(p)
				if RightfulOwner != 0:
					#print("Adding core to province "+str(p.ProvinceNumber)+", old owner: "+f.Name+" new owner: "+RightfulOwner.Name, " culture: "+p.GetMajorCulture().CultureName+RightfulOwner.Culture.CultureName)
					p.Cores.append(RightfulOwner)
					if f in p.Cores:
						if RemoveCoresIfSameGrp and p.GetMajorCulture().CultureGroup == f.Culture.CultureGroup:
							p.Cores.remove(f)
						elif RemoveCoresIfOtherGrp and p.GetMajorCulture().CultureGroup != f.Culture.CultureGroup:
							p.Cores.remove(f)

def WriteSummary():
	f = open("mod/"+ModName+" Summary.txt",'w')
	f.write("Summary for the world generated with seed "+str(Seed)+".")

	f.write("\n\nCivilized cultures: ")
	for c in CivilizedGrps:
		f.write(c+"; ")
		
	f.write("\n\nUncivilized cultures: ")
	for c in UncivilizedGrps:
		f.write(c+"; ")
		
	f.write("\n\nUnifiable cultures: ")
	for c in UnificationCultureGroups:
		f.write(c+"; ")
			
	f.write("\n\nNon colonized cultures: ")
	for c in UncolonizedGrps:
		f.write(c+"; ")
		
	f.write("\n\nStarting factions: "+str(len(Factions+SmallFactions))+" ("+str(len(SmallFactions))+" of which are small), releasable factions: "+str(len(UnreleasedFactions))+", factions total: "+str(len(Factions+UnreleasedFactions+UnificationFactions+SmallFactions)))
		
	f.write("\n\n======================================================")
	f.write("\n\tFactions")
	f.write("\n======================================================")
		
	for Faction in Factions+SmallFactions:
		Civ = "no"
		if Faction.Civilized:
			Civ="yes"
		Unif = "no"
		try:
			if Faction.Culture.Unifiable:
				Unif="yes"
		except:
			print(Faction.Name, Faction.Type)
		Type = "Normal"
		if Faction.Type != "":
			Type = Faction.Type
		PopMult = "%0.2f" % Faction.PopMultiplier
		Lit = "%0.2f" % Faction.Literacy
			
		f.write("\n\nFaction: "+Faction.Name+" ("+Faction.Culture.CultureGroup+"), type: "+Type+", provinces: "+str(len(Faction.ProvincesOwned))+", prestige: "+str(Faction.Prestige)+", factories: "+str(Faction.NumFactories))
		f.write("\nPopulation multiplier: "+PopMult+", civilized: "+Civ+", slavery: "+Faction.Slavery+", unifiable: "+Unif+", literacy: "+Lit)
		f.write("\nCulture: "+Faction.Culture.CultureName+" ("+Faction.Culture.CultureGroup+")")
		if len(Faction.AcceptedCultures)>0:
			f.write(", accepted cultures: ")
			for c in Faction.AcceptedCultures:
				f.write(c.CultureName+" ("+c.CultureGroup+"); ")
			
	f.write("\n\n======================================================")
	f.write("\n\tSettings.ini transcription")
	f.write("\n======================================================\n\n")
	sett = open("Generator/Settings.ini",'r').readlines()
	for l in sett:
		f.write(l)
		
	f.close()


def Main():

	os.chdir("../")
	Startup()

	#Create the cultures
	print("Creating cultures...")
	#create culture groups
	AvailableDicts = glob.glob("Generator/CultureGroups/*.names1")
	for i in range(len(AvailableDicts)): 
		#strip path and extension
		AvailableDicts[i] = AvailableDicts[i][AvailableDicts[i].find("\\")+1:AvailableDicts[i].find(".names1")]
	GrpsToCreate=random.randint(CultureGroupsMin,CultureGroupsMax)
	if GrpsToCreate > len(AvailableDicts) or GrpsToCreate == 0:
		GrpsToCreate = len(AvailableDicts)
	TotalGrps=0
	while TotalGrps<GrpsToCreate:
		ThisGrp = random.choice(AvailableDicts)
		GrpCivilized = 0
		if random.randint(0,100) <= CivilizedPercent:
			GrpCivilized = 1
		if not ThisGrp in DictionariesChosen:
			TotalGrps += 1
			if GrpCivilized:
				CivilizedGrps.append(ThisGrp)
			else:
				UncivilizedGrps.append(ThisGrp)
			DictionariesChosen.append(ThisGrp)
			for i in range(random.randint(CulturesPerGroupMin,CulturesPerGroupMax)):
				CultName = NameGen.GenerateFactionName(ThisGrp, "")
				Religion = NameGen.GenerateFactionName(ThisGrp, "")+"ism"
				cult = Culture(CultName, ThisGrp, Religion, GrpCivilized)
				Cultures.append(cult)
	#modify common/religion.txt
	CreateReligionFile()
	
	#Create factions stubs
	FactionsToCreate = random.randint(FactionsToCreateMin, FactionsToCreateMax)
	for i in range(FactionsToCreate+UnreleasedFactionsQty):
		ThisFaction = Faction()
		if i>FactionsToCreate:
			ThisFaction.Type = "Unreleased"
			ThisFaction.ExtraProvinces = random.randint(UnreleasedProvsMin,UnreleasedProvsMax)
			ThisFaction.PopMultiplier = random.uniform(UnreleasedPopMultiplierMin,UnreleasedPopMultiplierMax)
			UnreleasedFactions.append(ThisFaction)
		else:
			Factions.append(ThisFaction)
		
	#modify some factions characteristics according to the settings
	CreateFactionsConstraints()

	#parse region.txt
	print("Randomizing provinces... ")
	File = open("map/region.txt",'r')
	for i in File:
		if len(i)>5:
			Line = i.replace('{','').replace('}','').replace('=','')
			Line = Line[:Line.find('#')].split()
			if len(Line)>0:
				RegionTag = Line[0]
				ProvincesString = Line[1:len(Line)]
				RegionsProvinces = []
				for j in ProvincesString:
					ThisProvince = Province(int(j))
					AllProvinces.append(ThisProvince)
	
	#read provinces positions and adjacencies
	ReadProvincesData()

	print("Distributing cultures...")
	DistributeCultures()

	print("Randomizing regions...")
	RandomizeRegions()
	
	print("Creating unifiable factions...")
	CreateUnificationFactions()
	
	print("Distributing great powers provinces...")
	DistributeProvinces(1)
	
	print("Distributing others provinces...")
	DistributeProvinces(0)
	
	print("Creating small factions...")
	CreateSmallFactions()
	
	print("Creating unreleased factions...")
	CreateUnreleasedFactions()
	
	if FillColonizedProvs:
		print("Filling gaps...")
		FillGaps()
	
	if UnifiableRemoveCores:
		print("Removing foreign cores on unifiable territories...")
		RemoveForeignCoresOnUnifiable()

	if AcceptedCulturePresenceMinSameGrp>0 or AcceptedCulturePresenceMinOtherGrp>0:
		print("Assigning accepted cultures...")
		AssignAcceptedCultures()
		
	if AddCoresBasedOnCulture:
		print("Adding cores for rightful owners...")
		CheckCores()
		
	print("Updating factions...")
	WriteCountryFiles()
	
	#Write common/cultures.txt file
	print("Generating names...")
	CreateCommonCultures()
	
	
	#modify history/provinces:
	print("Updating history/provinces...")
	i=0
	for p in AllProvinces:
		sys.stdout.write("%0.2f%%\b\b\b\b\b\b\b" % (float(i)/len(AllProvinces)*100.0))
		i+=1
		ChangeProvinceOwnership(p)
			
	#create localisation file
	print("Creating localisation files...")
	File = open("mod/"+ModName+"/localisation/0random.csv",'a+')
	for ThisFaction in Factions+UnreleasedFactions+UnificationFactions+SmallFactions:
		Name = ThisFaction.Name
		if DEBUG_CULT_POS and ThisFaction.Culture!=0:
			Name = ThisFaction.Culture.CultureGroup
		elif DEBUG_TEXT and ThisFaction.Culture!=0:
			Name = ThisFaction.Tag+"_"+ThisFaction.Type+"_"+str(ThisFaction.ExtraProvinces)+"_"+ThisFaction.Culture.CultureGroup
		elif ThisFaction.Type == "Superpower":
			Name = "The "+Name+" Kingdom"
		elif ThisFaction.Type == "Russia":
			Suffix = [" Empire"]
			Name += random.choice(Suffix)
		elif ThisFaction.Type == "China":
			Suffix = [" Dynasty", " Khanate"]
			Name += random.choice(Suffix)
		elif ThisFaction.Type == "SecPower" or ThisFaction.Type == "Sweden":
			Suffix = open("Generator/SecPowerSuffixes.txt",'r').readlines()
			Chance = int(Suffix[0])
			Suffix.pop(0)
			if random.randint(0,100) < Chance:
				Name += " "+random.choice(Suffix).replace('\n','')
		File.write(ThisFaction.Tag+";"+Name+";;;;;;;;;;;;;x;;;;;;;;;;;;;;\n")
	File.close()
	File = open("mod/"+ModName+"/localisation/0random.csv",'a+')
	for ThisFaction in Factions+UnreleasedFactions+UnificationFactions+SmallFactions:
		if ThisFaction.Name != "":
			if ThisFaction.Name[len(ThisFaction.Name)-1] == 'a' or ThisFaction.Name[len(ThisFaction.Name)-1] == 'e': 
				File.write(ThisFaction.Tag+"_ADJ;"+ThisFaction.Name+"n;;;;;;;;;;;;;x;;;;;;;;;;;;;;\n")
			elif ThisFaction.Name[len(ThisFaction.Name)-1] == 'o':
				File.write(ThisFaction.Tag+"_ADJ;"+ThisFaction.Name[:len(ThisFaction.Name)-2]+"an;;;;;;;;;;;;;x;;;;;;;;;;;;;;\n")
			elif ThisFaction.Name[len(ThisFaction.Name)-1] == 'i' or ThisFaction.Name[len(ThisFaction.Name)-1] == 'u' or ThisFaction.Name[len(ThisFaction.Name)-1] == 'y':
				File.write(ThisFaction.Tag+"_ADJ;"+ThisFaction.Name+"an;;;;;;;;;;;;;x;;;;;;;;;;;;;;\n")
			else:
				File.write(ThisFaction.Tag+"_ADJ;"+ThisFaction.Name+"ian;;;;;;;;;;;;;x;;;;;;;;;;;;;;\n")
	for ThisRegion in Regions:
		# Region name
		ThisCulture = ThisRegion.Provinces[0].GetMajorCulture()
		if DEBUG_TEXT:
			File.write(ThisRegion.RegionTag+";"+ThisRegion.RegionTag+"_"+ThisCulture.CultureGroup+";;;;;;;;;;;;;x\n")
		else:
			File.write(ThisRegion.RegionTag+";"+NameGen.GeneratePlaceName(ThisCulture.CultureGroup,0,UseShortNames)+";;;;;;;;;;;;;x\n")		
		#Province names
		for ThisProvince in ThisRegion.Provinces:
			ThisCulture = ThisProvince.GetMajorCulture()
			if DEBUG_TEXT:
				File.write("PROV"+str(ThisProvince.ProvinceNumber)+";"+str(ThisProvince.ProvinceNumber)+"_"+ThisCulture.CultureGroup+";;;;;;;;;;;;;x\n")
			elif RandomizeProvinceNames:
				File.write("PROV"+str(ThisProvince.ProvinceNumber)+";"+NameGen.GeneratePlaceName(ThisCulture.CultureGroup,0,UseShortNames)+";;;;;;;;;;;;;x\n")
	WrittenCultGrps = []
	for ThisCulture in Cultures:
		if not ThisCulture.CultureGroupTag in WrittenCultGrps:
			WrittenCultGrps.append(ThisCulture.CultureGroupTag)
			File.write(ThisCulture.CultureGroupTag+";"+NameGen.GeneratePlaceName(ThisCulture.CultureGroup)+";;;;;;;;;;;;;x\n")			
		File.write(ThisCulture.CultureNameTag+";"+ThisCulture.CultureName+";;;;;;;;;;;;;x\n")
		File.write(ThisCulture.ReligionTag+";"+ThisCulture.Religion+";;;;;;;;;;;;;x\n")
	
	
	print("Creating flags...")
	File = open("mod/"+ModName+"/common/country_colors.txt","w")
	for ThisFaction in Factions+UnreleasedFactions+UnificationFactions+SmallFactions:
		File.write(ThisFaction.Tag+" = {\n")
		File.write("\tcolor1 = { "+str(ThisFaction.Colors[0][0])+" "+str(ThisFaction.Colors[0][1])+" "+str(ThisFaction.Colors[0][2])+" }\n")
		File.write("\tcolor2 = { "+str(ThisFaction.Colors[1][0])+" "+str(ThisFaction.Colors[1][1])+" "+str(ThisFaction.Colors[1][2])+" }\n")
		File.write("\tcolor3 = { "+str(ThisFaction.Colors[2][0])+" "+str(ThisFaction.Colors[2][1])+" "+str(ThisFaction.Colors[2][2])+" }\n}\n\n")		
		#create flag
		GenUtils.CreateFlag(ThisFaction.Tag, ThisFaction.Colors[0], ThisFaction.Colors[1], ThisFaction.Colors[2], ModName)
	#rebel flag
	GenUtils.CreateFlag("REB", (30,30,30), (random.randint(0,255),random.randint(0,255),random.randint(0,255)), (30,30,30), ModName )
	
	#populate the world
	print("Creating pops...")
	CreatePops()
	
	WriteSummary()
	
	print("\nDone! See \""+os.getcwd()+"\\mod\\"+ModName+" Summary.txt\" for details on the generated world.")
	print("\nStart the launcher and check the mod \""+ModName+"\" to play.")
	input("\nPress Enter to continue")
	
Main()

	
	