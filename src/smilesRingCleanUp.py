class Stack:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[-1]
    def size(self):
        return len(self.items)
    def __str__(self):
        lst = '['
        for i in self.items:
            lst += '%s, ' % i
        lst += ']'
        return lst
    def __repr__(self):
        return self.__str__()

class BinaryTree:
    def __init__(self, rootObj):
        self.key = rootObj
        self.left = None
        self.right = None
    
    def insertLeft (self, newNode):
        if self.left == None:
            self.left = BinaryTree(newNode)
        else: # has left child already
            t = BinaryTree(newNode)
            # set original left child as the left child of the newNode
            t.left = self.left
            # newNode is the left child
            self.left = t

    def insertRight (self, newNode):
        if self.right == None:
            self.right = BinaryTree(newNode)
        else: # has left child already
            t = BinaryTree(newNode)
            # set original left child as the left child of the newNode
            t.right = self.right
            # newNode is the left child
            self.right = t
    
    def getRootVal (self):
        return self.key
    
    def setRootVal (self, obj):
        self.key = obj

    def getLeftChild (self):
        return self.left
    
    def getRightChild (self):
        return self.right
            

class BinaryHeap:
    def __init__(self):
        self.heapList = [[0,0]]
        self.currentSize = 0
    
    def insert(self, k): # k for key
        self.heapList.append(k)
        self.currentSize += 1
        self.percUp(self.currentSize) # percUp until in proper location
    
    def percUp(self, i): # i is the new node index
        while i//2 > 0:
            if self.heapList[i] < self.heapList[i//2]:
                self.heapList[i],self.heapList[i//2] = self.heapList[i//2], self.heapList[i]
            i = i // 2

    def delMin (self): # root is min value, but need to keep heap order property
        # 1. taking the last item in the list and move it to the root position
        # 2. pushing the new root node down the tree to its proper position
        rootVal = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize] # 1. rootVal replaced with last node
        self.heapList.pop() # remove last node
        self.currentSize -= 1
        self.percDown(1)
        return rootVal
    
    def minChild(self, i): # return index of the minChild
        if i*2 + 1 > self.currentSize:
            return i*2
        else:
            if self.heapList[i*2] < self.heapList[i*2+1]:
                # if leftChild less than rightChild
                return i*2
            else:
                return i*2+1


    def percDown (self, i): # i is index of percDown node
        while (i*2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i] > self.heapList[mc]:
                self.heapList[i], self.heapList[mc] = self.heapList[mc], self.heapList[i]
            i = mc

    def isEmpty(self):
        return self.currentSize == 0
    
    def size(self):
        return self.currentSize

def heapSort(lst, heap=True):
    sortedList = []
    if not heap:
        heapList = BinaryHeap()
        for i in lst:
            heapList.insert(i)
        lst = heapList
    while lst.currentSize > 0:
        sortedList.append(lst.delMin())
    return sortedList

def smilesReplace(smiles, ring_closure_lst, val_dict):
    
    for i in range(len(ring_closure_lst)):
        popped = ring_closure_lst.pop()
        pos, old_val = popped[0], popped[1]
        new_val = val_dict[old_val]
        if new_val >= 10:
            new_val = '%' + str(new_val)
        else:
            new_val = str(new_val)
        if int(old_val) >= 10:
            smiles = smiles[:pos] + str(val_dict[old_val]) + smiles[pos+1:]
        else:
            smiles = smiles[:pos] + str(val_dict[old_val]) + smiles[pos+1:]
    return smiles

def gen_number_lst():
    number_lst = list(range(9,0,-1))
    for i in range(len(number_lst)):
        str_num = str(number_lst[i])
        number_lst[i] = str_num        
    return number_lst

def gen_ring_closure(smiles):
    number_lst = gen_number_lst()    
    cnt_since_last = 1
    ring_closure_lst = []
    for n, i in enumerate(smiles):
        if i in number_lst:
            if cnt_since_last == 0:
                print("double digit here")
                cnt_since_last = 0
            else:
                ring_closure_lst.append([n, i])
                cnt_since_last = 0
        else:
            cnt_since_last += 1
    ring_closure_lst = sorted(ring_closure_lst, 
                            key=lambda x: x[0], 
                            reverse=False)
    return ring_closure_lst

def conversion_dictionary(ring_closure_lst, cnt):
    val_dict = {}
    for i in ring_closure_lst:
        key = i[1]
        if key not in val_dict:
            val_dict[key] = cnt
            cnt += 1
            print(cnt)
    return val_dict, cnt

def cleanUp(smiles, cnt=1):

    ring_closure_lst = gen_ring_closure(smiles)

    val_dict, cnt = conversion_dictionary(ring_closure_lst, cnt)

    smiles = smilesReplace(smiles, ring_closure_lst, val_dict)
    
    print(smiles)
    return smiles, cnt
    
def main(smiles, patterns=['BBA', 'BBD']):
    smiles = smiles.split('.')
    f, s, t = smiles[0], smiles[1], smiles[2]

    cnt = 1 
    f, cnt = cleanUp(f, cnt)
    print("CNT:",cnt)
    s, cnt = cleanUp(s, cnt)
    print("CNT:",cnt)
    t, cnt = cleanUp(t, cnt)
    print("CNT:",cnt)
    combined = "%s.%s.%s" % (f, s, t)
    print(combined)
    for i in patterns:
        if cnt >= 10:
            r = '%' + str(cnt)
        else:
            r = str(cnt)
        combined = combined.replace(i, r)
        cnt += 1
    print(combined)
"""

smiles = '(BBD)(C=C7)=CC=C7N(C6=CC=CC=C6)C3=CC=CC=C3.C(BBA)5=C4C(N=CC=N4)=C(BBD)S5.C(BBA)1=CC=C(/C=C(C#N)/C(O)=O)C=C1'
smiles = 'c7ccc(N(c6ccccc6)c6ccc(8)cc6)cc7.c5cnc4c(8)sc(9)c4n5.N#C/C(=C\c1ccc(9)cc1)C(=O)O'
main(smiles)
#         (8)(C=C1)=CC=C1N(C2=CC=CC=C2)C3=CC=CC=C3.C(7)4=C5C(N=CC=N5)=C(8)S4.C(7)6=CC=C(/C=C(C#N)/C(O)=O)C=C6

smiles_og = 'c1ccc(N(c2ccccc2)c2ccc(3)cc2)cc1.c4cnc5c(6)sc(7)c5n4.N#C/C(=C\c8ccc(9)cc8)C(=O)O'
unique = []
for i in range(len(smiles)):
    if smiles[i] != smiles_og[i]:
        print(smiles[i], smiles_og[i], 'not matching')
        if [smiles[i], smiles_og[i]] not in unique:
            unique.append([smiles[i], smiles_og[i]])
    else:
        print(smiles[i], smiles_og[i])

print(unique)
"""


sm1 = '(BBD)(C=C7)=CC=C7N(C6=CC=CC=C6)C3=CC=CC=C3'
sm2 = 'C(BBA)5=C4C(N=CC=N4)=C(BBD)S5'
sm3 = 'C(BBA)1=CC=C(/C=C(C#N)/C(O)=O)C=C1'


