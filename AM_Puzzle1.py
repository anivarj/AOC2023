#AOC2023 Puzzle 1-1

#read file
file = r"C:\Users\AMICHAUD\OneDrive - Promega Corporation\Documents\GitHub\AOC2023\AM_1-1.txt"

#open file read into list, stripping any new line characters
with open(file, 'r') as f:
    lines = [line.strip() for line in f]

calval_list = [] #list for final calibration values

#for each string in the list, get the first and last integer and concatenate
for line in lines:
    nums = [i for i in list(line) if i.isdigit()] #make a list of all digits in the string
    calval_str = str(nums[0]) + str(nums[-1]) #grab the first and last digit and concatenate to 2 digits
    calval_int = int(calval_str) #turn 2-digit string into number
    calval_list.append(calval_int) #append to the calval list

sum1 = sum(calval_list) #sum all the calibration values

#Puzzle 1-2
#replace text numbers with digits and sum again
import re
number_dict = {'one': '1',
               'two': '2',
               'three': '3',
               'four': '4',
               'five': '5',
               'six': '6',
               'seven': '7',
               'eight': '8',
               'nine': '9'
               }
list2 = [] #list for the substituted strings

for line in lines: #for each line of the file
    linecopy = line #make a copy of the line
    for key, value in number_dict.items(): #iterate through dictionary
        if key in linecopy: #if a word is found in the string
            linecopy = re.sub(key, value, linecopy) #replace the string portion with the digit
    list2.append(linecopy) #add this substituted string to the new list 

    
calval_list2 = [] #list for the final 2-digit calibration numbers
for line in list2: #iterate through the corrected list
    nums2 = [i for i in list(line) if i.isdigit()] #make a list of all digits in the string
    calval_str2 = str(nums2[0]) + str(nums2[-1]) #grab the first and last digit and concatenate to 2 digits
    calval_int2 = int(calval_str2) #turn 2-digit string into number
    calval_list2.append(calval_int2) #append the number to the calval list

sum2 = sum(calval_list2) #sum all the calibration values 
#incorrect sum...where is the issue??