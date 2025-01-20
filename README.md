# Suffix Array vs Modified Prefix Trie

This repository implements a Suffix Array and Prefix Trie where strings are inverted before insertion.

## Code Structure
The Project is organized in 4 folders:
* datasets - contain the datasets used and a jupyter notebook with the code used to create each dataset
* experiments - contain the code to run the experiments
* structures - contain the implementation of the prefix trie and suffix array
* visualization - contain the code of the visualization interfaces developed with pygame


## Prefix Trie Interface
![image](https://github.com/user-attachments/assets/0038c8ff-a8a5-4947-9d8a-b7f31db27164)
![image](https://github.com/user-attachments/assets/d820be78-6849-4e71-a60c-c577e3d67ee3)
![image](https://github.com/user-attachments/assets/1a9ff24f-4947-4ff1-be43-e0ec4e74a14d)
![image](https://github.com/user-attachments/assets/35b11b95-5548-4924-a4c6-7a19188d837e)


## Suffix Array Interface
![image](https://github.com/user-attachments/assets/1252b2a6-3bff-4ab5-8893-d01021c728b3)
![image](https://github.com/user-attachments/assets/bfc6f6e8-1398-4b20-b080-67a5b72e3e4c)
![image](https://github.com/user-attachments/assets/a901ed67-656c-4ff3-8441-c2d85408b939)
![image](https://github.com/user-attachments/assets/fafbf9dc-0e5d-4dba-8fb9-fae6c5353c8c)
![image](https://github.com/user-attachments/assets/3b50b8cd-a76a-4ffd-8194-b1465cddaec0)


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
