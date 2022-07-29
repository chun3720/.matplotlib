from CSR.Player import runCSR
from pathlib import Path
import os
import sys

path = os.getcwd()
parent_path = Path(path).parent

if str(parent_path) not in sys.path:
    sys.path.append(str(parent_path))

def main():
    runCSR()
    
    
if __name__ =="__main__":
    main()
