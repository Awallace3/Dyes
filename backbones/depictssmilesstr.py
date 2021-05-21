from rdkit import Chem
#from rdkit import AllChem
from rdkit.Chem.Draw import IPythonConsole
#from rdkit.Chem import MolDrawing, Drawingoptions
IPythonConsole.ipython_useSVG=False  #< set this to False if you want PNGs instead of SVGs

#def mol_with_atom_index(mol):
#    for atom in mol.GetAtoms():
#        atom.SetAtomMapNum(atom.GetIdx())
#    return mol
smiles = input('What is your smiles string ')
mol = Chem.MolFromSmiles(smiles)
mol = Chem.AddHs(mol, addCoords=True) 
Chem.Draw.MolToFile(mol,'molecule.png',size=(300, 300), kekulize=True, wedgeBonds=True)


electronacceptor = '.'



