import csv
import argparse
import random
import os
from scipy import spatial
from sklearn.metrics import jaccard_similarity_score

def euclideanDistance():
	with open(args.f) as file:
		read = csv.DictReader(file, fieldnames=None)
		data = []
		for row in read:
			data.append(row)
	matrix = []
	column = read.fieldnames
	for x in enumerate(data):
		row = []
		for y in enumerate(data):
			col = 0
			if(x != y):
				for z in column:
					col +=(float(x[1][z]) - float(y[1][z]))**2
			col = col**0.5
			row.append(col)
		matrix.append(row)
	return(matrix)

def cosineDistance():
        with open(args.f) as file:
            read = csv.reader(file)
            data = []
            for row in read:
                data.append(row)
        matrix = []
        data.remove(data[0])   
        for x in enumerate(data):
                row = []
                for y in enumerate(data):
                        col = 0
                        if(x != y):
                                col = spatial.distance.cosine(list(map(float, x[1])), list(map(float, y[1])))
                        row.append(col)
                matrix.append(row)
        return(matrix)

def jaccardDistance():
	with open(args.f) as file:
		read = csv.reader(file)
		data = []
		for row in read:
			data.append(row)
	matrix = []
	data.remove(data[0])
	for x in enumerate(data):
		row = []
		for y in enumerate(data):
			col = 0
			if(x != y):
				col = jaccard_similarity_score(x[1], y[1])
			row.append(col)
		matrix.append(row)
	return(matrix)
  
def prim(graph, root):
	l1 = [int(root)]
	l1 = list(map(int, l1))
	amountVertex = len(graph)
	l2 = list(range(amountVertex))
	l2.remove(int(root))
	agm = []
	while(len(l2) != 0):
		edge = None
		result = [0, 0, 0]
		for i, x in enumerate(l1):
			for j, w in enumerate(graph):
				if((edge is None) or (w[x] < edge)) and (w[x] != 0) and (j not in l1):
					edge = w[x]
					result = [x, j, edge]
		l1.append(result[1])
		l2.remove(result[1])
		agm.append(result)
	return agm

def createClusters(graph, k):
	graphSorted = sorted(graph, key=lambda graph: graph[2], reverse=True)
	edges = graphSorted[k-1:]
	clusters = []
	amountVertex = len(graphSorted) + 1
	l2 = list(range(amountVertex))
	while(len(l2) != 0):
		print("passei aqui")
		l1 = [l2[0]]
		l2.remove(l1[0])
		clustersAux = []
		for i, n in enumerate(l1):
			for j, m in enumerate(edges):
				if(n == m[0]):
					clustersAux.append(m)
					l1.append(m[1])
					l2.remove(m[1])
					edges[j] = [None, None, None]
				if(n == m[1]):
					clustersAux.append(m)
					l1.append(m[0])
					l2.remove(m[0])
					edges[j] = [None, None, None]
			if(clustersAux == []):
				clustersAux.append([n, None, None])
		clusters.append(clustersAux)
	return clusters

def defineCluster(clusters, vert):
	for i, n in enumerate(clusters):
		for j, m in enumerate(n):
			if(vert == m[0] or vert == m[1]):
				clus = i
				return(clus)

def generateCSV(clusters):
	with open(args.f) as file:
		read = csv.reader(file)
		data = []
		for column in read:
			data.append(column)
		amountVertex = len(data) - 1 
		data[0].append('cluster')
	finalData = data[0]
	for i in range(amountVertex):
		clus = defineCluster(clusters, i)
		data[i+1].append(clus)
	with open('.cluster.'.join(args.f.split('.')), 'w', newline='') as file:
		write = csv.writer(file, delimiter=',')
		for row in data:
			write.writerow(row)
    
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Clustering Algorithm')
	parser.add_argument('-k', type=int, help='Number of clusters', required=True)
	parser.add_argument('-r', type=int, help='Root of the graph', required=False)
	parser.add_argument('-f', type=str, help='File .csv', required=True)
	parser.add_argument('-d', type=str, help='euclidean, cosine or jaccard', required=True)
	args = parser.parse_args()
	if(os.path.isfile(args.f)): 
		if(args.d == 'euclidean'):
			matrix = euclideanDistance()
		elif(args.d == 'cosine'):
			matrix = cosineDistance()
		elif(args.d == 'jaccard'):
			matrix = jaccardDistance()
		else:
			print()
			print('Wrong name! Choose between jaccard, euclidean or cosine.')
			quit()
		if((args.k >= 1) and(args.k <= len(matrix) - 1)):
			if(args.r is None):
				args.r = random.randrange(0, len(matrix) - 1)
				print()
				print('Root value not informed. Using random value:', args.r)
				agm = prim(matrix, args.r)
				clusters = createClusters(agm, args.k)
				generateCSV(clusters)
				print()
				print('Success!')
			else:
				if((args.r >= 0) and(args.r <= len(matrix) - 1)):
					agm = prim(matrix, args.r)
					clusters = createClusters(agm, args.k)
					generateCSV(clusters)
					print()
					print('Success!')
				else:
					print()
					print('Root value incorrect! Enter a value between 0 and', len(matrix) - 1)
		else:
			print()
			print('Number of clusters incorrect! Enter a value between 1 and', len(matrix) - 1)
	else:
		print()
		print('File not found!')