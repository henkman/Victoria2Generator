try:
	import Image, colorsys, random, glob, os
except:
	print "Python PIL is not installed! \nGet it from http://www.pythonware.com/products/pil/\nCurrently, it is only available for 32-bit Python 2.5, 2.6 and 2.7. \nAborting."
	raw_input("Press Enter to exit")
	exit()
	
from ImageDraw import Draw
from PIL import Image

def clamp(x, minimum,maximum):
    return max(minimum, min(x, maximum))
	
def remove_accents(stra):
	try:
		nkfd_form = unicodedata.normalize('NFKD', unicode(stra))
		return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])
	except:
		allowed = 'a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,Q,W,E,R,T,Y,U,I,O,P,A,S,D,F,G,H,J,K,L,Z,X,C,V,B,N,M, '.split(',')
		return ''.join([item for item in stra if item in allowed])
	
#returns 3 RGB tuples
def GetColors():
	Colors = []
	Hues = []
	
	Types = ["ValueGradient", "SatGradient", "HueGradient", "TwoTone"]
	Type = random.choice(Types)
	
	if Type is "HueGradient":
		#start with a random hue
		hue = random.uniform(0.0, 1.0)
		Hues.append(hue)
		for i in range(3):
			hue = (Hues[i] + random.uniform(0.9,1.1)*0.3333) % 1.0 #get another color away from the previous
			Hues.append(hue)
			#pick a random color
			saturation = random.uniform(0.4, 0.8)
			value = random.uniform(0.3,0.8)
			#convert HSV to RGB
			rgb = colorsys.hsv_to_rgb(hue, saturation, value)
			#convert float tuple[0.0-1.0] to byte tuple[0-255]
			rgb = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
			Colors.append(rgb)
			
	elif Type is "SatGradient":
		hue = random.uniform(0.0, 1.0)
		Hues.append(hue)
		for i in range(3):
			hue = Hues[0]
			saturation = 1-i*0.5
			value = random.uniform(0.6,0.8)
			if i==2:
				value=0.9
			rgb = colorsys.hsv_to_rgb(hue, saturation, value)
			rgb = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
			Colors.append(rgb)
	
	elif Type is "ValueGradient":
		hue = random.uniform(0.0, 1.0)
		Hues.append(hue)
		for i in range(3):
			hue = Hues[0]
			value = 1-i*0.5
			saturation = random.uniform(0.6,0.8)
			rgb = colorsys.hsv_to_rgb(hue, saturation, value)
			rgb = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
			Colors.append(rgb)
			
	elif Type is "TwoTone":
		hue = random.uniform(0.0, 1.0)
		Hues.append(hue)
		for i in range(3):
			hue = (Hues[i] + random.uniform(0.9,1.1)*0.5) % 1.0
			Hues.append(hue)
			value = random.uniform(0.6,0.8)
			saturation = random.uniform(0.4,0.8)
			if i==2:
				if random.randint(0,100)<50:
					value = 0.0
				else:
					saturation = 0.0
					value = 0.9
			rgb = colorsys.hsv_to_rgb(hue, saturation, value)
			rgb = (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
			Colors.append(rgb)
	
	return Colors
	
##################################################################################
##################################################################################
##################################################################################

#generates a flag and creates the TGA files on gfx/flags/
def CreateFlag(name, Color1, Color2, Color3, ModName):
	Colors = [Color1, Color2, Color3]
	im = Image.new("RGB", (93,64), Color1)
	draw = Draw(im)
	
	#define contrasting color
	Contrast = (233,233,233)
	c1hsv = colorsys.rgb_to_hsv(Color1[0]/255.0, Color1[1]/255.0, Color1[2]/255.0)
	if c1hsv[1] < 0.8 and c1hsv[2] > 0.7:
		Contrast = (20,20,20)
		
	#draw flag background
	choices = ["Horiz2", "Horiz3", "Vert2","Vert3", "Stripes", "X", "Cross", "TwoLines"]+["Plain"]*6
	Details = [""]
	choice = random.choice(choices)
	if choice is "Plain": #one color background, will add a detail
		Details = ["Circle", "Drawing", "HorizLine", "LeftRectangle", "Losangle", "OneTriangle", "TwoTriangles", "BigTriangle"]
		Colors = [Color2, Color3]
	elif choice == "Horiz2": # two-tone, horizontal
		if random.randint(0,100)<50:
			draw.rectangle((0, 32, 93, 64), fill=(Color3))
			Colors = [Color2]
		else:
			draw.rectangle((0, 32, 93, 64), fill=(Color2))
			Colors = [Color3]
		Details = [""]*4+["HorizLine"]+["LeftRectangle"]+["OneTriangle"]+["TwoTriangles"]+["Drawing"]
	elif choice == "Vert2": #two-tone, vertical
		if random.randint(0,100)<50:
			draw.rectangle((46, 0, 93, 64), fill=(Color2))
			Colors = [Color3]
		else:
			draw.rectangle((46, 0, 93, 64), fill=(Color3))
			Colors = [Color2]
		Details = [""]*4+["HorizLine"]
	elif choice == "Vert3": #three-tone, vertical
		if random.randint(0,100)<33:
			draw.rectangle((31, 0, 61, 64), fill=(Color2))
			draw.rectangle((62, 0, 93, 64), fill=(Color3))
		elif random.randint(0,100)<50:
			draw.rectangle((31, 0, 61, 64), fill=(Color3))
		else:
			draw.rectangle((31, 0, 61, 64), fill=(Color3))
			draw.rectangle((62, 0, 93, 64), fill=(Color2))
		Details = [""]*4+["Drawing"]*2
	elif choice == "Horiz3": #three-tone, horizontal
		if random.randint(0,100)<33:
			draw.rectangle((0, 21, 93, 42), fill=(Color2))
			draw.rectangle((0, 43, 93, 64), fill=(Color3))
		elif random.randint(0,100)<50:
			draw.rectangle((0, 21, 93, 43), fill=(Color3))
		else:
			draw.rectangle((0, 21, 93, 42), fill=(Color3))
			draw.rectangle((0, 43, 93, 64), fill=(Color2))
		Details = [""]*4+["Drawing"]*2
	elif choice == "X": #X
		draw.line((0, 0,93,64), width=8, fill=(Contrast))
		draw.line((0, 64,93,0), width=8, fill=(Contrast))
		Colors = [Color2,Color3]
	elif choice == "Cross": #cross
		if random.randint(0,100)<50: #centered
			draw.line((46, 0,46,64), width=8, fill=(Contrast))
			draw.line((0, 32,93,32), width=8, fill=(Contrast))
			Colors = [Color2,Color3]
		else: #a little to the left
			draw.line((32, 0,32,64), width=8, fill=(Contrast))
			draw.line((0, 32,93,32), width=8, fill=(Contrast))
	elif choice == "Stripes": #stripes
		draw.rectangle((0, 0,93,8), fill=(Contrast))
		draw.rectangle((0, 16,93,24), fill=(Contrast))
		draw.rectangle((0, 32,93,40),  fill=(Contrast))
		draw.rectangle((0, 48,93,56),  fill=(Contrast))
		Details = [""]*4+["OneTriangle"]
		Colors = [Color2]
	elif choice == "TwoLines":
		draw.line((23, 0,23,64), width=12, fill=(Contrast))
		draw.line((69, 0,69,64), width=12, fill=(Contrast))
		Colors = [Color2,Color3]
		Details = [""]*4+["Drawing"]
	
	#draw flag detail
	choice = random.choice(Details)
	if choice is "Circle":
		draw.ellipse((25, 12,70,52), fill=(Contrast))
		if random.randint(0,100)<90:
			choice = "Drawing"
	elif choice is "Losangle":
		draw.polygon((10,32, 46,59, 83,32, 46,5), fill=(Color3))
		choice = "Drawing"
	elif choice is "OneTriangle":
		if random.randint(0,100)<50:
			draw.polygon((0,0, 0,64, 46,32), fill=(random.choice(Colors))) #up to the middle
		else:
			draw.polygon((0,0, 0,64, 32,32), fill=(random.choice(Colors))) #smaller
	elif choice is "TwoTriangles":
		Color = random.choice(Colors)
		draw.polygon((0,0, 0,64, 46,32), fill=(Color))
		draw.polygon((93,0, 93,64, 46,32), fill=(Color))
	elif choice is "BigTriangle":
		draw.polygon((0,0, 93,0, 0,64), fill=(random.choice(Colors)))
	elif choice is "HorizLine":
		draw.line((0, 32,93,32), width=18, fill=(random.choice(Colors)))
	elif choice is "LeftRectangle":
		draw.rectangle((0, 0, 30, 64), fill=(random.choice(Colors)))

	im.save("mod/"+ModName+"/gfx/flags/"+name+".tga", "TGA")
	im.save("mod/"+ModName+"/gfx/flags/"+name+"_nodraw.tga", "TGA")
	im2 = Image.open("mod/"+ModName+"/gfx/flags/"+name+".tga")
	if choice is "Drawing":
		Stamps = glob.glob("Generator/FlagsRes/mon*.png")
		stamp = Image.open(random.choice(Stamps))
		im2.paste(stamp,(24,10), stamp)
		im2.save("mod/"+ModName+"/gfx/flags/"+name+".tga", "TGA")
		im2.save("mod/"+ModName+"/gfx/flags/"+name+"_republic.tga", "TGA")
		im2.save("mod/"+ModName+"/gfx/flags/"+name+"_monarchy.tga", "TGA")
	else:
		im.save("mod/"+ModName+"/gfx/flags/"+name+".tga", "TGA")
		im.save("mod/"+ModName+"/gfx/flags/"+name+"_republic.tga", "TGA")
		im.save("mod/"+ModName+"/gfx/flags/"+name+"_monarchy.tga", "TGA")
	del draw
	
	#save the files
	#communist flag:
	Stamps = glob.glob("Generator/FlagsRes/comm*.png")
	comm = Image.open(random.choice(Stamps))
	im3 = Image.open("mod/"+ModName+"/gfx/flags/"+name+"_nodraw.tga")
	im3.paste(comm,(24,10), comm)
	im3.save("mod/"+ModName+"/gfx/flags/"+name+"_communist.tga", "TGA")
	#fascist flag:
	Stamps = glob.glob("Generator/FlagsRes/fasc*.png")
	fasc = Image.open(random.choice(Stamps))
	im4 = Image.open("mod/"+ModName+"/gfx/flags/"+name+"_nodraw.tga")
	im4.paste(fasc,(24,10), fasc)
	im4.save("mod/"+ModName+"/gfx/flags/"+name+"_fascist.tga", "TGA")
	
	#delete temp file
	os.remove("mod/"+ModName+"/gfx/flags/"+name+"_nodraw.tga")
	
##################################################################################
##################################################################################
##################################################################################
def CreateLoadingScreens(ModFolder):
	ImageList = glob.glob("Generator/LoadingScrRes/bg*.jpg")
	
	Current = 1
	while Current < 8:
		im = Image.open(random.choice(ImageList))
			
		#generic stamps list
		Stamps = glob.glob("Generator/LoadingScrRes/Generic*.tga")
		#specific stamps list
		Words = ModFolder.split('_')
		for Word in Words:
			Stamps += glob.glob("Generator/LoadingScrRes/"+Word+"*.tga")
		#load stamp
		
		offset = 0
		for i in range(4):
			if random.randint(0,100)<50:
				stamp = Image.open(random.choice(Stamps))
				X = random.randint(127+i*150,150+i*150)
				Y = random.randint(320,400)
				im.paste(stamp,(X,Y), stamp)
			
		im.save("mod/"+ModFolder+"/gfx/loadingscreens/load_"+str(Current)+".bmp", "BMP")
		
		os.system("Generator\\nvdxt.exe -file \"mod\\"+ModFolder+"\\gfx\\loadingscreens\\load_"+str(Current)+".bmp\" -dxt3 -nomipmap -output  \"mod\\"+ModFolder+"\\gfx\\loadingscreens\\load_"+str(Current)+".dds\" > nul")
		#delete temp file
		#os.remove("mod/"+ModFolder+"/gfx/loadingscreens/load_"+str(Current)+".png")
		Current += 1
	

##################################################################################
##################################################################################
##################################################################################

#returns a parameter from Settings.ini as integer or float; if not found, raises an error
def GetParameter(name):
	Settings = open("Settings.ini",'r')
	for Line in Settings:
		Content = Line[:Line.find('#')].replace(' ','') #strip comments and white spaces
		Content = Content.split('=')
		if Content[0] == name:
			if '.' in Content[1]:
				return float(Content[1])
			return int(Content[1])
	print "Error: could not find property \""+name+" on Settings.ini. You probably mispelled it."
	raw_input("Press Enter to exit.")
	raise NameError('ParamNotFound')
