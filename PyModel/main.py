import collections
import pygraphviz as pgv

def kmers(s, k):

    res = []
    for c in range(0, len(s) - (k - 1) + 1):
        temp = s[c:c+k-1]
        res.append(temp)
    return res

def localDeBruijn(s, k):
    res = {}
    lstKmers = kmers(s, k)
    for r in range(0, len(lstKmers)-1):
        #v1, v2 = tuple(lstKmers[r:r+1])
        v1 = lstKmers[r]
        v2 = lstKmers[r+1]

        if res.get(v1) != None:
            if res[v1].get(v2) != None:
                e, c = res[v1][v2]
                res[v1][v2] = e + 1, c
            else:
                res[v1][v2] = 1, 1
        else:
            res[v1] = collections.OrderedDict([(v2, (1, 1))])
    return res

def findFirst():
    global graph

    children = []
    for key, child in graph.items():
        for keyCh, (edge, cover) in child.items():
            if keyCh not in children:
                children.append(keyCh)

    for key in graph.keys():
        if key not in children:
            return key

def eulerCycle(node):
    global graph
    global dna

    if dna == '':
        dna = node
    else:
        dna += node[-1:]

    if graph.get(node) != None:
        for key, (edge, cover) in graph[node].items():
            if edge != 0:
                graph[node][key] = edge - 1, cover
                eulerCycle(key)
                break; # не проходим по всем ребрам из данной вершины, а только по первой ненулевой
            else:
                del graph[node][key] # удаляем из графа нулевые вершины чтоб не проходить по ним вообще

#main
reads = open('reads.txt')
k = 8
graph = {}
dna = ''
first = ''

for line in reads:
    clearLine = line.strip()
    #print(clearLine)
    for key, child in localDeBruijn(clearLine, k).items():
        if graph.get(key) != None:
            for keyCh in child.keys():
                if graph[key].get(keyCh) != None:
                    e, c = graph[key][keyCh]
                    graph[key][keyCh] = e, c + 1
                else:
                    graph[key][keyCh] = child[keyCh]
        else:
            graph[key] = child


#print graph into .svg
#d = {'1':{'2':'[label = "a"]'}, '2':{'1':'g', '3':None}, '3':{'2':None}}
#G = pgv.AGraph(d, directed=True, ranksep='0.1')
G = pgv.AGraph(directed=True)
for k1, chDict in graph.items():
    for k2, value in chDict.items():
        e, c = value
        G.add_edge(k1, k2, label = k1 + k2[-1:] +' (' + str(e) + ', ' + str(c)+')')
G.draw('graph.svg', prog='dot')

#find DNA
first = findFirst()
#first = 'GAAGC'
eulerCycle(first)

syntheticDNA = open('syntheticDNA.txt').readline().strip()

if dna == syntheticDNA:
    print(dna)
    print('GOAL!')
else:
    if dna != None:
        print(syntheticDNA)
        print(dna + ' ' +str(len(dna)))
