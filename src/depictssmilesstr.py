from rdkit import Chem
from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem.Draw import MolDrawing, DrawingOptions
from rdkit.Chem import Draw
IPythonConsole.ipython_useSVG=False  #< set this to False if you want PNGs instead of SVGs
DrawingOptions.bondLineWidth=1.8
DrawingOptions.atomLabelFontSize=14
DrawingOptions.includeAtomNumbers=True
#def mol_with_atom_index(mol):
#    for atom in mol.GetAtoms():
#        atom.SetAtomMapNum(atom.GetIdx())
#    return mol
#smiles = 'C[NH3].[c]1ccccc1'
smiles= 'c7ccc(N(c6ccccc6)c6cc(C8)cc6)cc7.c5cnc4(C8)s(C9)c4n5.O=C(O)c1cc(C9)nc1'
mol = Chem.MolFromSmiles(smiles)
#smiles = input('What is your smiles string ')
mol = Chem.MolFromSmiles(smiles)
mol = Chem.AddHs(mol, addCoords=True)
Chem.Draw.DrawingOptions.MolToFile(mol,'molecule.png',size=(300, 300), kekulize=True, wedgeBonds=True)

#electrondonor = Chem.MolFromSmiles('c7ccc(N(c6ccccc6)c6ccccc6)cc7')
#backbone = Chem.MolFromSmiles('c5cnc4cscc4n5')
#electronacceptor =  Chem.MolFromSmiles('O=C(O)c1cccnc1')
#electrondonor = Chem.AddHs(electrondonor, addCoords=True)
#backbone = Chem.AddHs(backbone, addCoords=True)
#electronacceptor = Chem.AddHs(electronacceptor, addCoords=True)
#combo = Chem.CombineMols(electrondonor,backbone)
#combo = Chem.MolToSmiles(combo)
#Chem.Draw.MolToFile(mol,'molecule.png',size=(300, 300), kekulize=True, wedgeBonds=True)
#print(combo)
#edcombo = Chem.EditableMol(combo)


#h = Chem.MolToSmiles(combo)
#print(edcombo)

#edcombo.AddBond(5,10,order=Chem.rdchem.BondType.SINGLE)
#Chem.Draw.MolToFile(combo,'molecule.png',size=(300, 300), kekulize=True, wedgeBonds=True)






