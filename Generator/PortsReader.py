
PositionsTXT = open("../map/positions.txt",'r').readlines()
Out = open("Ports.txt",'w')

print "Be patient..."

for nr in range(1,2703):
	i=0
	while i<len(PositionsTXT):
		if PositionsTXT[i][0] != '\t' and PositionsTXT[i][0] != '#': #not an indented line or comment
			Data = PositionsTXT[i].strip(" \n\t").split('=')
			try:
				LineNr = int(Data[0])
				if LineNr == nr: #found province, check if has port
					while PositionsTXT[i] != "}\n":
						i+=1
						"""
						if PositionsTXT[i].find("unit") != -1:
							i += 2
							Data = PositionsTXT[i].strip(" \n\t").split('=')
							self.PosX = Data[1]
							i += 1
							Data = PositionsTXT[i].strip(" \n\t").split('=')
							self.PosY = Data[1]
						"""
						if PositionsTXT[i].find("naval_base") != -1 and PositionsTXT[i].find("#") == -1:
							#these provinces define a naval_base position but actually have no port, creating a fleet there causes a crash... took me hours to track this bug >:(
							NoPort = [1253, 373, 2091, 2141, 2044, 1047, 630, 417, 1301, 211, 39, 1406, 296]
							if not nr in NoPort:
								Out.write("\n"+str(nr))
								break
					i=len(PositionsTXT)
			except:
				pass
		i+=1
		
print "Done."