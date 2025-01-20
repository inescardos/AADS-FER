# Suffix Array vs Modified Prefix Trie

This repository implements a Suffix Array and Prefix Trie where strings are inverted before insertion.

## Code Structure
The Project is organized in 4 folders:
* datasets - contain the datasets used and a jupyter notebook with the code used to create each dataset
* experiments - contain the code to run the experiments
* structures - contain the implementation of the prefix trie and suffix array
* visualization - contain the code of the visualization interfaces developed with pygame


## Prefix Trie Interface
![image](https://hackmd.io/_uploads/S1CgGpswyl.png)
![image](https://hackmd.io/_uploads/H1lPzpowJx.png)
![image](https://hackmd.io/_uploads/r1CSGTjPyl.png)
![image](https://hackmd.io/_uploads/rkYtMpiw1x.png)

## Suffix Array Interface
![image](https://hackmd.io/_uploads/Skl2G6jvJx.png)
![image](https://hackmd.io/_uploads/Sk32z6ivke.png)
![image](https://hackmd.io/_uploads/ryOpz6jP1g.png)
![image](https://hackmd.io/_uploads/rJvCM6jDyx.png)
![image](https://hackmd.io/_uploads/rkAy76sDyg.png)


## Instructions to Run the Code

### 1. Clone the repository
Clone the repository using the following command:
```
git clone https://github.com/inescardos/AADS-FER
```

### 2. Install Python
Ensure Python 3.8 or higher is installed on your system. You can download Python from the [official website.](https://www.python.org/downloads/)

### 3. Create and activate a virtual environment
Set up and activate a virtual environment for the project:

```
  python -m venv venv
  source venv/bin/activate  # On Windows: .venv\Scripts\activate
  ```
  
### 4. Install the required libraries

```
pip install numpy 
pip install pygame
pip install time
pip install gc
pip install os
pip install pympler import
pip install memory_profiler
```

## Instructions to Run the Pygame Interface
To Run the Suffix Array interface run the command:

```
python -m visualization.suffixArray
```

To Run the Prefix Trie interface run the command:
```
python -m visualization.prefix_trie
```

## Instructions to Run the Experiments
To run the experiments for the suffix array use the command:

```
python -m experiments.suffixArray.<name of the test file>
```


To run the experiments for the prefix Trie use the command:
```
python -m experiments.prefixTrie.<name of the test file>
```

Note: Remember to comment the 'print' lines in the structures when running the experiments to maintain a cleaner and more understandable interface
