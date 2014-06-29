
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
            res[v1] = {v2: (1, 1)}
    return res



def eulerCycle(node):
    global graph
    global dna

    if dna == '':
        dna = node
    else:
        dna += node[-1:]

    if graph.get(node) != None:
        for key, (edge, cover) in graph[node].items():
            if cover != 0:
                graph[node][key] = edge - 1, cover
                eulerCycle(key)

    return

reads = open('dna-reads.txt')
k = 3
graph = {}
dna = ''

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

eulerCycle('TA')
print(dna)
