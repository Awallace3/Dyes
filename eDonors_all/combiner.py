
import os


# combined acceptor and backbone smiles string == COc1ccc(N(c2ccc(OC)cc2)c2ccc(-c3cccc4nsnc34)cc2)cc1
#all three combined together string == COc1ccc(N(c2ccc(OC)cc2)c2ccc(-c3ccc(-c4ccc(/C=C(\C#N)C(=O)O)cc4)c4nsnc34)cc2)cc1
#  backbone structure == c1ccc2nsnc2c1
# electronacceptor == COc1ccc(N(c2ccccc2)c2ccc(OC)cc2)cc1
# electrondonor == N#C/C(=C\c1ccccc1)C(=O)O
#electronacceptorsmiles = input('What is the electron acceptor smiles string? ')
backbone = input(path)
#electrondonesmiles = input('What is the electron donor smiles string? ')

backbone = list(backbone)
print(backbone)
fixedbackbone = []
for x in backbone:
    if x == '1':
        x = int(x)
        x = x + 1
        x = str(x)
        print(x)
        fixedbackbone.append(x)
    elif x == '2':
        x = int(x)
        x = x + 1
        x = str(x)
        fixedbackbone.append(x)
    elif x == '3':
        x = int(x)
        x = x + 1
        x = str(x)
        fixedbackbone.append(x)
    elif x == '4':
        x = int(x)
        x = x + 1
        x = str(x)
        fixedbackbone.append(x)
    elif x == '5':
        x = int(x)
        x = x + 1
        x = str(x)
        fixedbackbone.append(x)
    elif x == '6':
        x = int(x)
        x = x + 1
        x = str(x)
        fixedbackbone.append(x)
    elif x == '7':
        x = int(x)
        x = x + 1
        x = str(x)
        fixedbackbone.append(x)
    elif x == '8':
        x = int(x)
        x = x + 1
        x = str(x)
        fixedbackbone.append(x)
    else:
        fixedbackbone.append(x)



#print(fixedbackbone)
fixedbackbone = ''.join(fixedbackbone) 
print(fixedbackbone)


