from __future__ import absolute_import
from os import listdir
import os.path as osp 

def Load_matrix(path):
	with open(path) as f:
		lines = f.read()
		lines = lines.split('\n')
		for i in range(len(lines)):
			lines[i] = lines[i].split(' ')
			for j in range(len(lines[i])):
				if (',' in lines[i][j]):
					lines[i][j] = lines[i][j].split(',')
					lines[i][j] = [int(x) for x in lines[i][j]]
				else:
					lines[i][j] = int(lines[i][j])
	return lines 

def Save_matrix(path,data):
	with open(path,'w') as f:
		for i in range(len(data)):
			line_ = [str(x) if type(x)==int else str(x[0])+','+str(x[1]) for x in data[i]]
			string = ' '.join(line_)
			if (i!=len(data)-1):
				string = string + '\n'
			f.write(string)