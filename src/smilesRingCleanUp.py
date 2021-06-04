
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

def cleanUp(smiles):
    smiles = smiles.split('.')
    print(smiles)
    f, s, t = smiles[0], smiles[1], smiles[2]
    print(f, s, t)
    number_lst = list(range(9,0,-1))
    bin_of_stacks = []
    for i in range(len(number_lst)):
        number_lst[i] = str(number_lst[i])
    
    for i in range(len(number_lst)):
        bin_of_stacks.append(Stack()) #[pos] 
    
    cnt_since_last = 1
    for n, i in (f):
        cnt_since_last += 1

    print(bin_of_stacks)

smiles = '(BBD)(C=C7)=CC=C7N(C6=CC=CC=C6)C3=CC=CC=C3.C(BBA)5=C4C(N=CC=N4)=C((BBD))S5.C(BBA)1=CC=C(/C=C(C#N)/C(O)=O)C=C1'

cleanUp(smiles)