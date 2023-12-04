import re
import pandas as pd

file = r'C:\Users\AMICHAUD\OneDrive - Promega Corporation\Documents\GitHub\AOC2023\AM_2-1.txt'

with open(file, 'r') as f:
    lines = [line.strip() for line in f]

block_dict = {"red": 12, "green": 13, "blue": 14} #criteria for max blocks

#sort games into dict
def get_game_info(lines): 
    games_dict = {} #final dictionary of all games
    
    for line in lines:
        game = line.split(":")[0] #split the game off from the line
        rounds_list = line.split(":")[1] #take the other half of the line for rounds
        gamenumber = game.split(" ")[1] #get the game number
        rounds_sep = rounds_list.split(";") #make a list of individual rounds to the game
        counter = 1
        rounddict = {} #dictionary for rounds
        
        for round in rounds_sep: #for each round of a game...
            round_number = counter
            colors = round.split(",") #split the single round into colors
            colordict = {} #dictionary for the colors in a round
            
            for color in colors: #for each color in the round...
                amount = re.findall('\d+',color) #find the digit
                blockcolor = [c for c in block_dict.keys() if c in color] #find the color based on dictionary keys. this is old but i don't feel like changing it.
                colordict[blockcolor[0]] = amount[0] #extract the block color and number of blocks from the lists
            rounddict[str(round_number)] = colordict #make dictionary entry in the round dictionary
            counter+= 1 #advance counter 1 to generate the next round number for the dict key
        
        games_dict[gamenumber] = rounddict #add the game entry to the game dictionary
    return(games_dict)

#takes dictionary and turns into multi-level dataframe
def dict_to_df(dict): 
    df = pd.DataFrame.from_dict(games_dict, orient="index").stack().to_frame() #create df from dict
    df = pd.DataFrame(df[0].values.tolist(), index=df.index) #  to break out the lists of rounds into columns
    df = df.fillna(0) #fill any missing colors marked as "NaN" with 0
    df.index.names = ['Game Number', 'Round Number'] #rename the indices 
    df = df.reset_index() #reset the index and turn Game Number and Round Number into columns
    df = df.astype(int) #set dtype
    return(df)

#main 
games_dict = get_game_info(lines) #make the dictionary
df = dict_to_df(games_dict) #make the dataframe
impossiblegames = df[(df[("green")] >13) | (df[("red")] > 12) |(df[("blue")] > 14)] #list all the impossible games
impossiblenumbers = set(impossiblegames["Game Number"]) #get the game numbers (set to get unique values)
leftovers = df[~df['Game Number'].isin(impossiblenumbers)] #make df of all the leftovers once false games excluded
leftovernumbers = set(leftovers["Game Number"]) #make a set of the leftover game numbers
total = sum(leftovernumbers) #sum game numbers

##### 2-2
import numpy as np

df.replace(0, np.nan, inplace=True) #replace 0's with NAN

reds = df.loc[:,["Game Number", "red"]] #slice reds
greens = df.loc[:,["Game Number", "green"]] #slice greens
blues = df.loc[:,["Game Number", "blue"]] #slice blues

minreds = reds.groupby(["Game Number"]).max() #get the max red for each game
mingreens = greens.groupby(["Game Number"]).max() #get the max green for each game
minblues = blues.groupby(["Game Number"]).max() #get the max blue for each game

merged = minreds.merge(mingreens, on = "Game Number").merge(minblues, on = "Game Number") #merge the three colors
merged["Power"] = merged.red * merged.green * merged.blue #multiply each game's colors to get power
total = merged["Power"].sum() #sum the power column