import json

class Excitation:
    def __init__(self): #intializing the class
        self.exc = '' # Excitation number 
        self.method_basis_set = ''
        self.nm = 0
        self.osci = 0 
        self.orbital_Numbers = []
    
    def setExc(self, exc): # setter function
        self.exc = exc
    def setNm(self, nm): # setter function
        self.nm = nm
    def setOsci(self, osci):
        self.osci = osci
    def setOrbital_Numbers(self,orbital_Numbers):
        self.orbital_Numbers = orbital_Numbers
    def setMethod_basis_set(self, method_basisSet):
        self.method_basis_set = method_basisSet
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def __str__(self):
       return self.toJSON()

class Molecule:
    def __init__(self):
        self.name = ''
        self.LUMO = 0
        self.HOMO = 0
        self.excitations = []
        self.SMILES = ''
        self.generalSMILES = ''
        self.parts = ''
        self.localName = ''

    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def setLUMO(self, energy):
        self.LUMO = energy
    
    def setHOMO(self, energy):
        self.HOMO = energy
    
    def setExictations(self, energy_osc):
        self.excitations = energy_osc
    
    def setSMILES(self, smiles):
        self.SMILES = smiles
        
    def setGeneralSMILES(self, smiles):
        self.generalSMILES = smiles

    def setParts(self, parts):
        self.parts = parts

    def setLocalName(self, localName):
        self.localName = localName
    
    def sendToFile(self, name):
        with open(name, 'w') as fp:
            fp.write(self.toJSON())

    def giveData(self, data):
        self.name = data["name"]
        self.LUMO = data["LUMO"]
        self.HOMO = data["HOMO"]
        self.excitations = data["excitations"]
        self.SMILES = data["SMILES"]
        self.generalSMILES = data["generalSMILES"]
        self.parts = data["parts"]
        self.localName = data["localName"]

    def setData(self, fileName):
        with open(fileName, 'r') as json_file:
            data = json.load(json_file)
            
        self.name = data["name"]
        self.LUMO = data["LUMO"]
        self.HOMO = data["HOMO"]
        self.excitations = data["excitations"]
        self.SMILES = data["SMILES"]
        self.generalSMILES = data["generalSMILES"]
        self.parts = data["parts"]
        self.localName = data["localName"]
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def __str__(self):
       return self.toJSON()

class MoleculeList():
    def __init__(self):
        self.molecules = []
    
    def addMolecule(self, molecule):
        self.molecules.append(molecule)
    
    def setData(self, fileName):
        with open(fileName, 'r') as json_file:
            data = json.load(json_file)
        self.molecules = data['molecules']

    
    
    def removeMolecule(self, name):
        for i in range(len(self.molecules)):
            mol = Molecule()
            mol.giveData(self.molecules[i])
            print("\nDELETED:", i)
            if mol.getName() == name:
                del self.molecules[i]
                break
    
    def checkMolecule(self, smiles):
        found = False
        for n, i in enumerate(self.molecules):
            mol = Molecule()
            mol.giveData(i)
            print(mol.SMILES, smiles)
            if mol.SMILES == smiles:
                found = True
        return found 

    def updateMolecule(self, molecule):
        size = len(self.molecules)
        found = False
        for i in range(size):
            mol = Molecule()
            #print(self.molecules[i])
            #print(type(i))
            #print(len(self.molecules))
            #print(i.getName())
            mol.giveData(self.molecules[i])
            if mol.name == molecule.name:
                #print('updating existing Molecule information in results.json')
                self.molecules[i] = molecule
                found = True
                break

        if found == False:
            print('Creating new Molecule in results.json for %s' % molecule.getName())
            #self.addMolecule(mol)
            #mol = Molecule()
            self.addMolecule(molecule)
        '''
        for n, i in enumerate(self.molecules):
            mol = Molecule()
            #print(type(i))
            #print(len(self.molecules))
            #print(i.getName())
            mol.giveData(i)
            if mol.name == molecule.name:
                print('updating existing Molecule information in results.json')
                self.molecules[n] = molecule
            else:
                print('Creating new Molecule in results.json')
                self.addMolecule(mol)
                #self.addMolecule(i)
        '''
    def sendToFile(self, fileName):
        with open(fileName, 'w') as fp:
            fp.write(self.toJSON())

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)
    
    def __str__(self):
       return self.toJSON()
    