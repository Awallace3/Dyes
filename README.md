# Dyes

## About us

We are computational chemists that created this program at the University of
Mississippi. The goal of our project is to create and predict the properties of
exotic molecular dyes for dye sensitized solar cells. The Benchmark folder
contains our training set and the JSON folder has the all of our data. If you
would like to use this program for your research please email
`tsantaloci@gmail.com`.

## How The Code Works

This program performs four tasks:

- (Build) Combines SMILES strings and creates gaussian input files with there corresponding coordinates.
- (Manage) Submits Jobs and resubmits jobs on the Mississippi Center Supercomputer account which runs on an PBS workload manager
- (Gather) Gathers data from Gaussian output files and places them into JSON files to determine the best candidates.
- (Analysis) Perform analysis on generated JSON files to find trends, improve
  computational predictions, and determine best candidates for experimental
  testing.

### Steps

Select what task you would like to perform `Build`, `Manage`, `Gather`, or `Analysis`

<!-- (We need to figure out where to put these options) -->

#### Build

1. input SMILES strings (copied from ChemDraw):

   - `python3 inputs_v2.py`
   - _Follow inputs_v2.py instructions and SMILE strings will go in either the eAcceptor, backbone or eDonor directory_

2. submit final.py script!
   - SMILES strings will be combined and input files will be placed in the results directory.
3. `python3 final.py`

#### Manage

`qsub_queue` will keep track of what jobs need to be submitted to the cluster next

1. `python3 final.py`

#### Gather

Parses output files to generate JSON and .pkl files

1. `python3 final.py`

#### Analysis

Create figures and score computed structures

1. Relevant functions are in `src/gather_results.py`

### Combinatorial Approach

![Example](https://github.com/Awallace3/Dyes/blob/main/Example_image.png)

### Examples

![Example Structures](https://github.com/Awallace3/Dyes/blob/main/Example_Structs.png)

### Selecting the Specific Type

This code is designed for four types of Dye Sensitized Solar Cells:

- Single Donor 𝝅-conjugated dye sensitized solar cell (D-𝝅-A)
- Double Donor 𝝅-conjugated dye sensitized solar cell (D-D-𝝅-A)
- Triple Donor 𝝅-conjugated dye sensitized solar cell (D-D-D-𝝅-A)
- Donor Acceptor Donor dye sensitized solar cell (D-A-D)

## Dependencies

| Package      | Version  |
| ------------ | -------- |
| matplotlib   | 3.3.3    |
| networkx     | 3.0      |
| numba        | 0.55.1   |
| numpy        | 1.19.4   |
| pandas       | 1.2.3    |
| rdkit        | 2022.9.5 |
| requests     | 2.28.2   |
| scikit_learn | 1.2.2    |
| scipy        | 1.6.1    |

For a simple installation of packages, run `conda create --name <env> --file requirements.txt`

### System Package Requirements

- [OpenBabel](https://openbabel.org/docs/dev/Installation/install.html)- Creates the SMILE strings and converts them to Cartesian Coordinates (Mandatory)
- [ChemDraw](https://perkinelmerinformatics.com/products/research/chemdraw) - The user inputs chemdraw generated SMILE strings (Recommended for substructure generation)

## Future Ideas

These are future ideas for the project. If anyone would like to do them feel free to contact us and we are willing to help. Everyone in this project has split up but I think someday atleast one of us will come back to it.

- Update scoring for high voltage dye sensitized solar cells
- Setting up code for porphyrin solar cell molecules
- Benchmark study on porphyrin solar cells to create a scoring methodology
- Setting up code for perovskite solar cell molecules
- Benchmark study on perovskite solar cell molecules to create a scoring methodology
- Explore the possibility of finding new catalysts
- Setting up code for the ruthenium dye database that already exists
