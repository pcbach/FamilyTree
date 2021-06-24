from graphviz import Graph
import os
import pandas as pd
import unicodedata
os.environ["PATH"] += os.pathsep + 'D:/work/gia pha/Graphviz/bin'

class Tree:
	def __init__(self, idx, yPos, xPos, parent, data):
		self.idx = idx
		self.yPos = yPos
		self.xPos = xPos
		self.xMax = 0
		self.xMin = 1e9
		self.children = [] 
		self.parent = parent
		self.data = data
	def update(self, leftBound):
		for i in range(len(self.children)):
			#print(self.idx + " update " + self.children[i].idx + " with " + str(leftBound))
			leftBound = self.children[i].update(leftBound) + 1 
			#print(self.idx + " update " + self.children[i].idx + " result " + str(leftBound))
		if len(self.children) == 0:
			self.xPos = leftBound
			self.xMax = leftBound
			self.xMin = leftBound
			return leftBound
		else:
			xMin = 1e9
			xMax = -1e9
			#print(str(self.idx) + " " + str(self.xMax))
			for i in range(len(self.children)):
				xMin = min(xMin,self.children[i].xPos)
				xMax = max(xMax,self.children[i].xPos)
				self.xMax = max(self.xMax,self.children[i].xMax)
				self.xMin = min(self.xMin,self.children[i].xMin)
				print('###')
				print(self.idx)
				print(self.xMin)
				print(self.children[i].xMin)
				print('###')
			self.xPos = (xMin + xMax)/2
			#print(str(self.idx) + " " + str(self.xMax))
			return self.xMax
		
	def addChild(self, node):
		self.children.append(node)
		#self.update()
	def printInfo(self):
		print("I: " + str(self.idx))
		print("X: " + str(self.xPos))
		print("Y: " + str(self.yPos))
		print("Children: ",end = "")
		for i in range(len(self.children)):
			print(str(self.children[i].idx) + " ",end = "")

		print("\nParent: ",end = "")
		if(self.parent != None):
			print(self.parent.idx,end = "")
		else:
			print("root",end = "")
		print("\n")


df = pd.read_excel('giapha.xlsx',header = 2)
a = df.values.tolist()
count = 0

gen = 0
branch = 1
num = 2
maleNum = 3
idx = 4
midx = 5
tenTu = 6
tenHuy = 7
gender = 8
birth = 9
death = 10
age = 11
info = 12
sCnt = 13
sNum = 14
sidx = 15
sTenHuy = 16
sTenHieu = 17
sbirth = 18
sdeath = 19
sage = 20
schildmale = 21
schildfemale = 22
sinfo = 23

tree = []
tree.append(Tree("1.0.1",0,0,None,a[0]))
tree.append(Tree("1.0.1.1",1,0,tree[0],a[0]))
tree[0].addChild(tree[1])
tree[0].update(0)
#tree[0].printInfo()
#tree[1].printInfo()
genmax = [-1] * 50
for i in range(1,239):
	print(i)
	if str(a[i][branch]) == 'nan':
		continue

	idx_ = a[i][idx]
	xPos = genmax[int((a[i][gen]-1)*2)] + 1
	genmax[int((a[i][gen]-1)*2)] = xPos
	yPos = (a[i][gen]-1)*2
	midx_ = a[i][midx]
	for j in range(len(tree)):
		if(tree[j].idx == midx_):
			parent = tree[j]


	tree.append(Tree(idx_,yPos,xPos,parent,a[i]))
	parent.addChild(tree[len(tree)-1])

    #tree[0].update(0)
	spouse = tree[len(tree)-1]
	#print(a[i][sCnt])
	if a[i][sCnt] == 0:
		pass
	else:
		for j in range(int(a[i][sCnt])): 
			sidx_ = a[i+j][sidx]
			xPos = genmax[int((a[i][gen]-1)*2+1)] + 1
			genmax[int((a[i][gen]-1)*2+1)] = xPos
			yPos = (a[i][gen]-1)*2+1
			parent = spouse
			tree.append(Tree(sidx_,yPos,xPos,parent,a[i+j]))	
			parent.addChild(tree[len(tree)-1])

	#tree[0].update(0)
tree[0].update(0)


f = open("file.html", "w", encoding="utf-8")
f.write(
"""<!DOCTYPE html>
<html>
<head>
	<title> Gia Phả Họ Phạm </title>
	<style>
	</style>
<head>
<body style = "margin: 0 ;padding: 0 ;">
	<div id="container" style = \"position: relative;\">
	<div style="white-space:nowrap;font-size:300px;position:absolute;top:0px;left:1px;" > Gia Phả Họ Phạm </div>
		<div style="white-space:pre;text-align: center;position:absolute;top:310px;left:1px;height:120px;width:800px;font-size:25px"> Người ta nguồn gốc từ đâu 
Có tổ tiên trước rồi sau có mình
Muốn biết ai sinh thành mà có
Phải xem gia phả mới rõ phân minh !
		</div>
		 <div style="position:absolute;white-space: pre-wrap;top:450px;left:1px;width:800px;font-size:25px">	Nguyên tổ tiên ta từ trước ở làng Rĩ-xá huyện Kim Bảng, tỉnh Hà Nam (nay là tỉnh Nam Hà) đến Nội Xá (tức Vạn Thắng) sinh cơ lập nghiệp truyền đến chúng ta ngày nay. Nay là thôn Vạn Thắng, xã Vạn Thái, huyện Ứng Hoà, tỉnh Hà Tây. 
	Gia phả trước kia đều có cả, nhưng chẳng may giặc Pháp sang xâm lăng, đốt phá làng mạc năm 1952 nên cháy mất. Để sau này cho con cháu biết rõ nguồn gốc ông cha ta nên ngày 3-11-1972 dương lịch tức là ngày 28-9 năm Nhâm Tý (Âm lịch). Ông cụ Phạm Quý Triêm là cháu 11 đời soạn và ông Phạm Trọng Tấn là cháu 12 đời ghi chép thành văn bản.
	Để tránh rách nát, thất lạc, được sự nhất trí cụa Họ vào ngày 13-2-1992 tức 10-1-Tân Mùi, Phạm Hồng Chính là cháu 13 đời chép lại theo quyển gia phả gốc mà 2 ông Phạm Quý Triêm và Phạm Trọng Tấn đã soạn thảo. Thêm vào đó, có bổ sung các đời sau.
	Sau 28 năm, ngày 16-12-2020 tức ngày 3-11-Canh Tý, để cập nhật gia phả, Phạm Chí Bách là cháu 14 đời chép lại quyển gia phả mà ông Phạm Hồng Chính chép lại.
	Trong quá trình ghi chép laị, để tránh "tam sao thất bản" người chép lại đã chép đúng nguyên bản chỉ sửa lại những câu, chữ trong gia phả gốc mà thôi.
	Và họ coi đây là Gia Phả Gốc.

	</div>
	</div>	
""")
font = 25
height = font*2.5
width = height*4.5
pad = 30
leftPad = pad/2
topPad = pad/2
tMax = 0
lMax = 0
coeff1 = 0.4
coeff2 = 1.2

for i in range(len(tree)):
	

	if tree[i].yPos%2 == 0:
		name = ''
		if str(tree[i].data[tenHuy]) != 'nan':
			name = str(tree[i].data[tenHuy])
		else:
			name = "Kh\u00F4ng r\u00F5"
		if str(tree[i].data[tenTu]) != 'nan':
			name = name + '\n T\u1EF1 ' + str(tree[i].data[tenTu])
		if name == '':
			name = "Kh\u00F4ng r\u00F5"


		left = (width + pad)*tree[i].xPos
		right = (width + pad)*tree[i].xPos
		for j in range(len(tree[i].children)):
			left = min(left,(width + pad)*tree[i].children[j].xPos)
			right = max(right,(width + pad)*tree[i].children[j].xPos)
		if len(tree[i].children) == 0:
			h = str(height + pad * 0.5 )
		else:
			h = str(height * 2 + pad * (1.5 - coeff1) )
		w = str(right - left + width + pad*0.5)
		lMax = max(lMax,left-0.25*pad + leftPad + width)
		tMax = max(tMax,(height + pad)*tree[i].yPos-0.25*pad + topPad + height - pad*coeff1*(tree[i].yPos)/2 + pad*coeff2*(tree[i].yPos)/2 )

		f.write("""		<div style = \"border-width:1px;position: absolute;top:""" + str((height + pad)*tree[i].yPos-0.25*pad + topPad - pad*coeff1*(tree[i].yPos)/2 + pad*coeff2*(tree[i].yPos)/2) + """px;left:""" + str(left-0.25*pad + leftPad + width/2) + """px; width: """ + w + """px;height: """ + h + """px;border-style:dashed;\"></div>\n""")
		
		#name
		nameTop = str((height + pad)*tree[i].yPos + topPad - pad*coeff1*(tree[i].yPos)/2 + pad*coeff2*(tree[i].yPos)/2)
		nameLeft = str((width + pad)*tree[i].xPos + leftPad + width/2)
		nameWidth = str(width)
		nameHeight = str(height)
		nameContent = name

		f.write("""		<div id = \"""" + str(tree[i].idx) + """name\" onclick="myFunction('""" + str(tree[i].idx) + """')\" style = \"cursor:pointer;border-width:3px;background: white;text-align: center;  white-space: pre;position: absolute;top:""" + nameTop + """px;left:""" + nameLeft + """px; width: """ + nameWidth + """px;height: """ + nameHeight + """px;border-style:solid;font-size: """ + str(font) + """px;\"> """ + nameContent + """ </div>\n""")
		#f.write("""		<div id = \"""" + str(tree[i].idx) + """info\" onclick="myFunction('""" + str(tree[i].idx) + """')\" style = \"display: none;position: absolute;top:""" + str((height + pad)*tree[i].yPos + topPad - pad*coeff1*(tree[i].yPos)/2 + pad*coeff2*(tree[i].yPos)/2) + """px;left:""" + str((width + pad)*tree[i].xPos + leftPad) + """px; width: """ + str(width) + """px;height: """ + str(height) + """px; border-style:solid;font-size: """ + str(font) + """px;\"> """ + str(tree[i].xMax) + " " + str(tree[i].xMin) + """ </div>\n""")
	
	else:
		name = ''
		if str(tree[i].data[sTenHuy]) != 'nan':
			name = name + str(tree[i].data[sTenHuy])
		else:
			name = "Kh\u00F4ng r\u00F5"
		if str(tree[i].data[sTenHieu]) != 'nan':
			name = name + '\n Hi\u1EC7u ' + str(tree[i].data[sTenHieu])
		if name == '':
			name = "Kh\u00F4ng r\u00F5"
		lMax = max(lMax,(width + pad)*tree[i].xPos + leftPad+ width)
		tMax = max(tMax,(height + pad)*tree[i].yPos + topPad + height - pad*coeff1*(tree[i].yPos)/2 + pad*coeff2*(tree[i].yPos)/2 )


		#name
		nameTop = str((height + pad)*tree[i].yPos + topPad - pad*coeff1*(tree[i].yPos+1)/2 + pad*coeff2*(tree[i].yPos-1)/2)
		nameLeft = str((width + pad)*tree[i].xPos + leftPad + width/2)
		nameWidth = str(width)
		nameHeight = str(height)
		nameContent = name



		f.write("""		<div id = \"""" + str(tree[i].idx) + """name\" onclick="myFunction('""" + str(tree[i].idx) + """')\" style = \"cursor:pointer;border-width:3px;background: white;text-align: center;  white-space: pre;position: absolute;top:""" + nameTop + """px;left:""" + nameLeft + """px; width: """ + nameWidth + """px;height: """ + nameHeight + """px;border-style:solid;font-size: """ + str(font) + """px;\"> """ + nameContent + """ </div>\n""")
		#f.write("""		<div id = \"""" + str(tree[i].idx) + """info\" onclick="myFunction('""" + str(tree[i].idx) + """')\" style = "display: none;position: absolute;top:""" + infoTop  + """px;left:""" + infoLeft + """px; width: """ + infoWidth + """px;height: """ + infoHeight + """px;border-style:solid;font-size: """ + str(font) + """px;\"> """ + infoContent + """ </div>\n""")


for i in range(len(tree)):
	

	if tree[i].yPos%2 == 0:

		#info
		infoTop = str((height + pad)*tree[i].yPos + topPad - pad*coeff1*(tree[i].yPos)/2 + pad*coeff2*(tree[i].yPos)/2)
		infoLeft = str((width + pad)*tree[i].xPos + leftPad )
		infoWidth = str(width*2.5)
		infoHeight = str(height*2.5) 

		infoContent = "Ph\u1EA1m Qu\u00FD C\u00F4ng" if str(tree[i].data[gender])=='Nam' else ""
		infoContent += " Hu\u00FD " if (str(tree[i].data[gender])=='Nam' and str(tree[i].data[tenHuy])!='nan') else "" 
		infoContent += (str(tree[i].data[tenHuy])) if str(tree[i].data[tenHuy])!='nan' else ""
		infoContent += (" T\u1EF1 " + str(tree[i].data[tenTu])) if str(tree[i].data[tenTu])!='nan' else ""
		infoContent += ("\n Sinh: " + str(tree[i].data[birth])) if str(tree[i].data[birth])!='nan' else ""
		infoContent += ("\n M\u1EA5t: " + str(tree[i].data[death]) ) if str(tree[i].data[death])!='nan' else ""
		infoContent += ("\n Th\u1ECD: " + str(tree[i].data[age]) ) if str(tree[i].data[age])!='nan' else ""
		infoContent += ("\n " + str(tree[i].data[info]) ) if str(tree[i].data[info])!='nan' else ""
		

		#infoContent = " Ten: " + str(tree[i].data[tenHuy]) + "\n Tu: " + str(tree[i].data[tenTu]) + "\n Sinh: " + str(tree[i].data[birth]) + "\n Mat: " + str(tree[i].data[death]) + "\n Tho: " + str(tree[i].data[age]) 

		#f.write("""		<div id = \"""" + str(tree[i].idx) + """name\" onclick="myFunction('""" + str(tree[i].idx) + """')\" style = \"cursor:pointer;border-width:3px;background: white;text-align: center;  white-space: pre;position: absolute;top:""" + str((height + pad)*tree[i].yPos + topPad - pad*coeff1*(tree[i].yPos)/2 + pad*coeff2*(tree[i].yPos)/2) + """px;left:""" + str((width + pad)*tree[i].xPos + leftPad) + """px; width: """ + str(width) + """px;height: """ + str(height) + """px;border-style:solid;font-size: """ + str(font) + """px;\"> """ + str(tree[i].xMax) + " " + str(tree[i].xMin) + """ </div>\n""")
		f.write("""		<div id = \"""" + str(tree[i].idx) + """info\" onclick="myFunction('""" + str(tree[i].idx) + """')\" style = \"cursor:pointer;border-width:3px;background: white;text-align: center;  white-space: pre;display: none;position: absolute;top:""" + infoTop + """px;left:""" + infoLeft + """px; width: """ + infoWidth + """px;height: """ + infoHeight + """px; border-style:solid;font-size: """ + str(font) + """px;\"> """ + infoContent + """ </div>\n""")
	
	else:
		
		#info
		infoTop = str((height + pad)*tree[i].yPos + topPad - pad*coeff1*(tree[i].yPos+1)/2 + pad*coeff2*(tree[i].yPos-1)/2)
		infoLeft = str((width + pad)*tree[i].xPos + leftPad )
		infoWidth = str(width*2.5)
		infoHeight = str(height*2.5)
		infoContent = ""
		infoContent += (str(tree[i].data[sTenHuy])) if str(tree[i].data[sTenHuy])!='nan' else ""
		infoContent += (" Hi\u1EC7u " + str(tree[i].data[sTenHieu])) if str(tree[i].data[sTenHieu])!='nan' else ""
		infoContent += ("\n Sinh: " + str(tree[i].data[sbirth])) if str(tree[i].data[sbirth])!='nan' else ""
		infoContent += ("\n M\u1EA5t: " + str(tree[i].data[sdeath])) if str(tree[i].data[sdeath])!='nan' else ""
		infoContent += ("\n Th\u1ECD: " + str(tree[i].data[sage])) if str(tree[i].data[sage])!='nan' else ""
		infoContent += ("\n " + str(tree[i].data[sinfo]) ) if str(tree[i].data[sinfo])!='nan' else ""
		#infoContent += ("\n Sinh duoc ") if (int(tree[i].data[schildmale])>0 or int(tree[i].data[schildfemale])>0) else ("\n Khong co con")
		#infoContent += (str(int(tree[i].data[schildmale])) + " con trai ") if int(tree[i].data[schildmale])>0 else ""
		#infoContent += (str(int(tree[i].data[schildfemale])) + " con gai ") if int(tree[i].data[schildfemale])>0 else ""
		#for j in range(len(tree[i].children)):
		#f.write("""		<div id = \"""" + str(tree[i].idx) + """name\" onclick="myFunction('""" + str(tree[i].idx) + """')\" style = \"cursor:pointer;border-width:3px;background: white;text-align: center;  white-space: pre;position: absolute;top:""" + nameTop + """px;left:""" + nameLeft + """px; width: """ + nameWidth + """px;height: """ + nameHeight + """px;border-style:solid;font-size: """ + str(font) + """px;\"> """ + nameContent + """ </div>\n""")
		f.write("""		<div id = \"""" + str(tree[i].idx) + """info\" onclick="myFunction('""" + str(tree[i].idx) + """')\" style = "cursor:pointer;border-width:3px;background: white;text-align: center;  white-space: pre;display: none;position: absolute;top:""" + infoTop  + """px;left:""" + infoLeft + """px; width: """ + infoWidth + """px;height: """ + infoHeight + """px;border-style:solid;font-size: """ + str(font) + """px;\"> """ + infoContent + """ </div>\n""")




	
f.write(
"""		<canvas id="myCanvas" width=""" + str(lMax) + """ height=""" + str(tMax) + """>Your browser does not support the HTML5 canvas tag.</canvas>
	</div>
</body>
<script>
	function myFunction(id) {
	  	var x = document.getElementById(id.concat("info"));
	  	console.log(id.concat("info"))
	  	if (x.style.display === "none") {
	    	x.style.display = "block";
	  	} else {
	    	x.style.display = "none";
	  	}
	}
	var c = document.getElementById("myCanvas");
	var ctx = c.getContext("2d");
	
""")
for i in range(len(tree)):
	if tree[i].yPos%2 == 1:
		x = (width + pad)*(tree[i].xPos + 0.5) + width/2
		y = (height + pad)*(tree[i].yPos + 0.5) - pad*coeff1*(tree[i].yPos+1)/2 + pad*coeff2*(tree[i].yPos-1)/2 
		for j in range(len(tree[i].children)):
			x_ = (width + pad)*(tree[i].children[j].xPos + 0.5) + width/2
			y_ = (height + pad)*(tree[i].children[j].yPos + 0.5) - pad*coeff1*(tree[i].children[j].yPos)/2 + pad*coeff2*(tree[i].children[j].yPos)/2
			f.write("""
ctx.moveTo(""" + str(x) + """,""" + str(y) + """);
ctx.lineTo(""" + str(x) + """,""" + str((y+y_)/2) + """);
ctx.lineTo(""" + str(x_) + """,""" + str((y+y_)/2) + """);
ctx.lineTo(""" + str(x_) + """,""" + str(y_) + """);""")

#ctx.moveTo(0, 0);
#ctx.lineTo(2000, 1000);
#ctx.moveTo(10, 10);
#ctx.lineTo(2010, 1010);
		



f.write("""
	ctx.strokeStyle = 'rgba(0, 0, 0, 0.6)';
	ctx.lineWidth = 3;
	ctx.stroke();
</script>
</html>
""")
