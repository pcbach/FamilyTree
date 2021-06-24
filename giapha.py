from graphviz import Graph
import os
import pandas as pd
import unicodedata
os.environ["PATH"] += os.pathsep + 'D:/work/gia pha/Graphviz/bin'


df = pd.read_excel('giapha.xlsx',header = 2, skipfooter = 225)

a = df.values.tolist()


dot = Graph(comment='Gia Pha')
gen = 0
branch = 1
num = 2
maleNum = 3
code = 4
mCode = 5
tenTu = 6
tenHuy = 7
sCnt = 12
sNum = 13
sCode = 14
sTenHuy = 15
sTenHieu = 16

dot.format = 'png'

sub = [None] * 236

sub[0] = Graph('cluster_'+str(0))
sub[0].node(str(a[0][code]), "Kh\u00F4ng r\u00F5 \n T\u1EF1 " + str(a[0][tenTu]), shape='box', color = 'blue')
sub[0].node(str(a[0][sCode]), "Kh\u00F4ng r\u00F5 \n Hi\u1EC7u " + str(a[0][sTenHieu]), color = 'red')
sub[0].edge(str(a[0][code]), str(a[0][sCode]), color='invis')

dot.subgraph(sub[0])
print(len(a))

for i in range(1, 42):
	if str(a[i][sCnt]) == 'nan':
		continue

	sub[i] = Graph('cluster_'+str(i))
	sub[i].attr(rank='same')
	ten = ''
	if str(a[i][tenHuy]) != 'nan':
		ten = str(a[i][tenHuy])
	else:
		ten = "Kh\u00F4ng r\u00F5"
	if str(a[i][tenTu]) != 'nan':
		ten = ten + '\n T\u1EF1 ' +str(a[i][tenTu])
	if ten == '':
		ten = "Kh\u00F4ng r\u00F5"
	
	if a[i][maleNum] == 0:
		sub[i].node(str(a[i][code]), ten, shape='box', color = 'red')
	else:
		sub[i].node(str(a[i][code]), ten, shape='box', color = 'blue')


	#print(a[i][sCnt])
	if a[i][sCnt] == 0:
		pass
	else:
		for j in range(int(a[i][sCnt])):
			sTen = ''
			if str(a[i+j][sTenHuy]) != 'nan':
				sTen = sTen + str(a[i+j][sTenHuy])
			else:
				sTen = "Kh\u00F4ng r\u00F5"
			if str(a[i+j][sTenHieu]) != 'nan':
				sTen = sTen + '\n Hi\u1EC7u ' + str(a[i+j][sTenHieu])
			if sTen == '':
				sTen = "Kh\u00F4ng r\u00F5"

			if a[i][maleNum] == 0:
				sub[i].node(str(a[i+j][sCode]), sTen, color = 'blue')
			else:
				sub[i].node(str(a[i+j][sCode]), sTen, color = 'red')	

			sub[i].edge(str(a[i][code]), str(a[i+j][sCode]), color='invis')
	dot.subgraph(sub[i])
	dot.edge(str(a[i][mCode]), str(a[i][code]))



dot.render('test-output/giapha', view=True)  