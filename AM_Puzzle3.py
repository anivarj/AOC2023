import pandas as pd
import numpy as np
import re

file = r'C:\Users\AMICHAUD\OneDrive - Promega Corporation\Documents\GitHub\AOC2023\AM_3-1.txt'

with open(file, 'r') as f:
    lines = [line.strip() for line in f]
    lines_sub = [re.sub("[^0-9.]", "*", line) for line in lines] #replace all symbols with *
    lines_sub2 = [re.sub(r"(*)", r"\1,", line) for line in lines_sub] #add comma after all characters
    
df = pd.DataFrame(lines_sub2, columns = ["import"]) #create dataframe
df= df["import"].str.split(",", expand=True) #expand each comma delineated bunch into a cell

#### I GIVE UP ######