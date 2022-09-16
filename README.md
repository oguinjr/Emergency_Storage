# Emergency Supply

### Video Demo: <URL HERE>

### Description

### Background

This program originated as the final project assignment for CS50P Introduction to Programming with Python. It is the first program I have written in any language and attempts to showcase the skills learned in class if not a few more inpired by rabbitholes on stackexchange. When brainstorming needs I have in my personal life, I first thought of my family and a reocurring interest iv'e had in creating emergency plans and water storage. Soon after my first Costco trip to purchase bulk food items I realised that shelf lives are often sooner than permanent storage would allow. And so it is neccessary when storing food to rotate items that are expiring into ones regular food supply. With so many dates to remember however, keeping track of 5 gallons of peanut butter can be difficult. certainly an excel spreadsheet would solve the problem but that wouldnt be much fun and hardly showcase my capacity beyond point and click. 

With this assignment I hope to track all items stored and have a better understanding of when items expire. 

Because this is my first creative attempt in programming I welcome criticism and advice. I do not want to think of this project as complete once the course ends but continue to improve upon it as my skill in the language increases. Unavoidably there will be code written that is completely rediculous and the least efficient route to its goal. I hope that more experienced programmers will point these errors out to me so that I can learn to be a more efficient programmer. 

#### actions

- store data about supply in csv file
- input entries of supply and update csv
- get total supply
- get days current supply should last
- get supply deficit
- get soonest expiration date
  
 ### Usage
  #### Start Program
  ...TODO...
  #### Select From Main Menu
  After starting the program 5 options will be presented in the form of a line starting with its choice number and a sentence describing the action to take.
  If ####"1" is selected, the program will display the current volume of water in storage in gallons.
  if "2" is selected
  

#### Topics Used From Class

- csv read write
- loops, conditionals, variables, functions, classes, lists, datetime objects

#### Topics Requiring Further Study

- csv writting without using dictionary, datetime manipulation

#### Methods

- datetime
- csv
- sys

#### Description

The main file project.py uses several conditional functions to store and retrieve information about food and water emergency supplies. Each line on the two csv files contains comma seperated descriptions of a unit of the real wold supply. 5 options are presented after running the main file "get supply total", "get next expiration", "add supply", "get breakdown", and "exit".
If statements direct to the respective functions. Following the user's completion of each request the program self references tha main() function so that the original options are available again. 
After opening the project.py file and choose a prompt, type the corresponding number or letter and press return. 
- If 1 was selected a printout will appear displaying total volume in storage. 
- If 2, the closest date a unit of food or water is expiring will be displayed along with days remaining before that date. 
- If 3, a promp corresponding to each collumn of the csv file will request that collumns information, for water these prompts will be, "type", "medium", "medium amount", and "expiration". For food they will be "type", "medium", "calories", "volume", "category", "number of servings", TODO ...
- If 4, a printout will display for "total"
"time"
"need"
"category"
TODO...




### Author

**Frank O'Guin**

GitHub: @oguinjr


