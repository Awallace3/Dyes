# Dyes

## About us 

We are computational chemists that created this program at the University of Mississippi. The goal of our project is to create and predict the properties of exotic molecular dyes for dye sensitized solar cells. The Benchmark folder contains our training set and the JSON folder has the all of our data. If you would like to use this program for your research please email `tsantaloci@gmail.com`. 


## How The Code Works
<p align="center">
  <img src="https://github.com/Awallace3/Dyes/tree/main/src/Example_image.png" width="350" title="Example image" \>
</p>

![image description or alt text](https://github.com/Awallace3/Dyes/tree/main/src/Example_image.png)

### Selecting the Specific Type
-- This code is limited to four types of Dye Sensitized Solar Cells:
* Single Donor 𝝅-conjugated dye sensitized solar cell (D-𝝅-A)
* Double Donor 𝝅-conjugated dye sensitized solar cell (D-D-𝝅-A)
* Triple Donor 𝝅-conjugated dye sensitized solar cell (D-D-D-𝝅-A)
* Donor Acceptor Donor dye sensitized solar cell (D-A-D)


## Dependencies

* matplotlib==3.3.3
* networkx==3.0
* numba==0.55.1
* numpy==1.19.4
* pandas==1.2.3
* rdkit==2022.9.5
* requests==2.28.2
* scikit_learn==1.2.2
* scipy==1.6.1

The user can use `pip install package_name` to create correct depencencies.

## External Dependencies 

* OpenBabel- Creates the SMILE strings and converts them to Cartesian Coordinates


## Future Ideas

-- These are future ideas for the project. If anyone would like to do them feel free to contact us and we are willing to help. Everyone in this project has split up but I think someday atleast one of us will come back to it.

* Update scoring for high voltage dye sensitized solar cells
* Setting up code for porphyrin solar cell molecules
* Benchmark study on porphyrin solar cells to create a scoring methodology
* Setting up code for perovskite solar cell molecules
* Benchmark study on perovskite solar cell molecules to create a scoring methodology 
* Explore the possibility of finding new catalysts 
* Setting up code for the ruthenium dye database that already exists



