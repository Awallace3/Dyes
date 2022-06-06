import json


class PieceInfo:
    def __init__(self):
        self.localNamePiece = ''
        self.allowed = 0
        self.InChI_key = ''
        self.smiles = ''

    def setLocalName(self, localName):
        self.localName = localName

    def setAllowed(self, allowed):
        self.allowed = allowed

    def setInChI_key(self, InChI_key):
        self.InChI_key = InChI_key

    def setSmiles(self, smiles):
        self.smiles = smiles

    def giveData(self, data):
        self.localName = data['localName']
        self.allowed = data['allowed']
        self.InChI_key = data['InChI_key']
        self.smiles = data['smiles']

    def toJSON(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)


class AllowedList:
    def __init__(self):
        self.pieces = []

    def toJSON(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)

    def setData(self, fileName):
        with open(fileName, 'r') as json_file:
            data = json.load(json_file)
        self.molecules = data['allowed_list']

    """
    def updateMolecule(self, piece):
        size = len(self.pieces)
        found = False
        for i in range(size):
            pie = PieceInfo()
            pie.giveData(self.pieces[i])
            if piece.InChI_key == pie.InChI_key:
                #print('updating existing Molecule information in results.json')
                #self.molecules[i] = molecule

                #self.pieces[i] =
                found = True
                break

        if found == False:
            print('Creating new Molecule in results.json for %s' % molecule.getName())
            #self.addMolecule(mol)
            #mol = Molecule()
            self.addMolecule(molecule)
    """
