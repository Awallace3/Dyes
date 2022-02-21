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

class Excitation_exc(Excitation):
    def __init__(self): #intializing the class
        super().__init__()
        Excitation.__init__(self)
        self.HOMO = 0
        self.LUMO = 0

    def setHOMO(self, HOMO): # setter function
        self.HOMO = HOMO
    def setLUMO(self, LUMO):
        self.LUMO = LUMO

    def giveOldData(self, data):
        # print("DATA:", data)
        self.exc = data['exc']
        self.method_basis_set = data['method_basis_set']
        self.nm = data['nm']
        self.osci = data['osci']
        self.orbital_Numbers = data['orbital_Numbers']
        self.LUMO = 0
        self.HOMO = 0

    def getEXC(self):
        print(self.HOMO, self.LUMO)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)
    def toDict(self):
        return vars(self)
    """
    def giveData(self, data):

        self.exc = data["exc"]
    """

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

    def appendExcitations(self, excitation_objs_lst):
        for i in excitation_objs_lst:
            self.excitations.append(i)

    def setSMILES(self, smiles):
        self.SMILES = smiles

    def setGeneralSMILES(self, smiles):
        self.generalSMILES = smiles
    def toDict(self):
        return vars(self)

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

class Molecule_exc():
    def __init__(self):
        self.name = ''
        self.excitations = []
        self.SMILES = ''
        self.generalSMILES = ''
        self.parts = ''
        self.localName = ''

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name


    def setExictations(self, energy_osc):
        self.excitations = energy_osc

    def appendExcitations(self, excitation_objs_lst):
        for i in excitation_objs_lst:
            self.excitations.append(i)

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
        if isinstance(data, dict):
            self.name = data["name"]
            self.excitations = data["excitations"]
            self.SMILES = data["SMILES"]
            self.generalSMILES = data["generalSMILES"]
            self.parts = data["parts"]
            self.localName = data["localName"]
        else:
            print('uh oh')

    def setData(self, fileName):
        with open(fileName, 'r') as json_file:
            data = json.load(json_file)

        self.name = data["name"]
        self.excitations = data["excitations"]
        self.SMILES = data["SMILES"]
        self.generalSMILES = data["generalSMILES"]
        self.parts = data["parts"]
        self.localName = data["localName"]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def toDict(self):
        return vars(self)
    def __str__(self):
       return self.toJSON()

class Molecule_exc_BM(Molecule_exc):
    def __init__(self):
        super().__init__()
        self.exp = 0


    def setExp(self, exp):
        self.exp = exp

    def giveData(self, data):
        self.exp = data["exp"]
        self.name = data["name"]
        self.excitations = data["excitations"]
        self.SMILES = data["SMILES"]
        self.generalSMILES = data["generalSMILES"]
        self.parts = data["parts"]
        self.localName = data["localName"]


    def setData(self, fileName):
        with open(fileName, 'r') as json_file:
            data = json.load(json_file)

        if 'exp' in data:
            self.exp = data["exp"]
        else:
            self.exp = 0

        self.name = data["name"]
        self.excitations = data["excitations"]
        self.SMILES = data["SMILES"]
        self.generalSMILES = data["generalSMILES"]
        self.parts = data["parts"]
        self.localName = data["localName"]



class Molecule_BM(Molecule):
    def __init__(self):
        super().__init__()
        Molecule.__init__(self)
        self.exp = 0

    def setExp(self, exp):
        self.exp = exp

    def giveData(self, data):

        self.exp = data["exp"]
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

        if 'exp' in data:
            self.exp = data["exp"]
        else:
            self.exp = 0

        self.name = data["name"]
        self.LUMO = data["LUMO"]
        self.HOMO = data["HOMO"]
        self.excitations = data["excitations"]
        self.SMILES = data["SMILES"]
        self.generalSMILES = data["generalSMILES"]
        self.parts = data["parts"]
        self.localName = data["localName"]



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
            #print(mol.SMILES, smiles)
            if mol.SMILES == smiles:
                found = True
        return found
    """
    def checkExc(self):
        for i in self.molecules:
            mol = Molecule()
            mol.giveData(i)
    """


    def updateMolecule(self, molecule, exc_json=False):
        size = len(self.molecules)
        found = False
        for i in range(size):
            if exc_json:
                mol = Molecule_exc()
            else:
                mol = Molecule()
            if isinstance(self.molecules[i], dict):
                mol.giveData(self.molecules[i])
            if mol.name == molecule.name:
                self.molecules[i] = molecule
                # print('updating...')
                # print(len(self.molecules))
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



class MoleculeList_exc():
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
            #print(mol.SMILES, smiles)
            if mol.SMILES == smiles:
                found = True
        return found
    """
    def checkExc(self):
        for i in self.molecules:
            mol = Molecule()
            mol.giveData(i)
    """


    def updateMolecule(self, molecule, exc_json=False):
        # print(molecule)
        size = len(self.molecules)
        found = False
        for i in range(size):
            if exc_json:
                mol = Molecule_exc()
                mol.giveData(self.molecules[i])

                if mol.name == molecule.name:
                    # print('before toDict:', molecule.name)
                    self.molecules[i] = molecule.toDict()
                    # print("updated position", self.molecules[i])
                    # print(mol.toDict())
                    # print('updating...')
                    # print(len(self.molecules))
                    found = True
                    break

            else:
                mol = Molecule()
                if isinstance(self.molecules[i], dict):
                    mol.giveData(self.molecules[i])
                if mol.name == molecule.name:
                    self.molecules[i] = molecule
                    # print('updating...')
                    # print(len(self.molecules))
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
        print('The excited state information is being written')
        with open(fileName, 'w') as fp:
            #print(fp)
            fp.write(self.toJSON())

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def __str__(self):
       return self.toJSON()
