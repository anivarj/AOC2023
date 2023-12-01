#AOC2023 Puzzle 1-1

#read file
file = r"C:\Users\AMICHAUD\OneDrive - Promega Corporation\Documents\GitHub\AOC2023\AM_1-1.txt"

#open file read into list, stripping any new line characters
with open(file, 'r') as f:
    lines = [line.strip() for line in f]

calval_list = [] #list for calibration values

#for each string in the list
for line in lines:
    nums = [i for i in list(line) if i.isdigit()] #make a list of all digits in the string
    calval_str = str(nums[0]) + str(nums[-1]) #grab the first and last digit and concatenate to 2 digits
    calval_int = int(calval_str) #turn 2-digit string into number
    calval_list.append(calval_int) #append to the calval list

sum = sum(calval_list) #sum all the calibration values