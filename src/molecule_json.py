import json

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
        #print(data)
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
            print(i)
            if mol.getName() == name:
                del self.molecules[i]
                break
    
    def sendToFile(self, fileName):
        with open(fileName, 'w') as fp:
            fp.write(self.toJSON())

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)
    
    def __str__(self):
       return self.toJSON()
    
"""test = Molecule()
test.setData('testing.json')
mol_lst = MoleculeList()

for i in range(5):
    mol_lst.addMolecule(test)
mol_lst.sendToFile("molecules_list.json")


test = Molecule()
mol_lst = MoleculeList()
mol_lst.setData('molecules_list.json')
mol_lst.removeMolecule('')
#mol_lst.addMolecule(test)
mol_lst.sendToFile("molecules_list.json")
#mol_lst.removeMolecule('')
#mol_lst.removeMolecule('')
#print(mol_lst)

"""