
PositionsTXT = open("../map/positions.txt",'r').readlines()
Out = open("Positions.txt",'w')

print "Be patient..."

import psyco
psyco.full()

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
						PosX=0
						PosY=0
						if "text_position" in PositionsTXT[i] or "unit" in PositionsTXT[i] or "building_construction" in PositionsTXT[i]:
							i += 2
							Data = PositionsTXT[i].strip(" \n\t").split('=')
							PosX = Data[1]
							i += 1
							Data = PositionsTXT[i].strip(" \n\t").split('=')
							PosY = Data[1]
							Out.write(str(nr)+" "+PosX+" "+PosY+"\n")
							#print nr,PosX,PosY
							break
					#i=len(PositionsTXT)
			except:
				pass
		i+=1
		
print "Done."