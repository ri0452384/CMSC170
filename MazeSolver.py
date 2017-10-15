from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

maze=[]
originalmazetext=""


class Node():
    def __init__(self,ex,why,eff,gee,haych):
        self.x = ex
        self.y = why
        self.f = eff
        self.g = gee
        self.h = haych

    def __str__(self):
        return "<x:%s y:%s f:%s g:%s h:%s>" % (self.x, self.y, self.f,self.g, self.h)

    def __repr__(self):
        return "<x:%s y:%s f:%s g:%s h:%s>" % (self.x, self.y, self.f,self.g, self.h)


#returns coordinates(x,y) of the starting position
def get_start():
    y, x = len(maze), len(maze[0])
    for i in range(0, y):
        for j in range(0, x):
            if maze[i][j] == "P":
                return j, i

#returns coordinates(x,y) of the goal
def get_goal():
    x, y = len(maze), len(maze[0])
    for i in range(0, y):
        for j in range(0, x):
            if maze[i][j] == ".":
                return j, i

#returns the manhattan distance from current point to goal
def calculate_manhattan_heuristic(x1,y1):
    x2,y2 = get_goal()
    return abs(x2-x1)+abs(y2-y1)

#returns the direct distance as defined by MP
def calculate_direct_heuristic(x1,y1):
    x2,y2 = get_goal()
    return max(abs(x2-x1),abs(y2-y1))

#scans through the maze and returns what char is occupying tile x,y
def get_char_at(x,y):
    return maze[y][x]


#solves the maze via manhattan distance as the heuristic values
def solve_manhattan():
    openlist=[Node]
    closedlist=[Node]
    parent=[Node]

    x,y = get_start()
    heuristic = calculate_manhattan_heuristic(x,y)
    #starting Node is made the current because this will be added to the closed list
    #f=g+h, but g is 0, therefore f=h.
    current = Node(x,y,heuristic,0,heuristic)
    closedlist.append(current)
    print(current.x)
    print(current.y)
    print(get_char_at(current.x,current.y))
    print(closedlist)

def openfile():
    global originalmazetext
    global maze
    maze=[]
    originalmazetext =""
    filename = filedialog.askopenfilename( filetypes = ( ("Text file", "*.txt"),("All files", "*.*")))
    with open(filename) as file:
        content = file.readlines()
    for line in content:
        #line = line.replace("\n", "")
        #line = line.replace("\r", "")
        row = list(line)
        maze.append(row)
    print(maze)
    mazeoutput=""
    for line in maze:
        for character in line:
            mazeoutput+=character
    origlabel.config(text=mazeoutput)

def showhelp():
    messagebox.showinfo('help file goes here')
root = Tk()

#**************************UI**************** main window code goes  here
root.minsize(width=325,height=100)
#left frame here
mainframe = Frame(root,bg='#2B2B2B')
mainframe.pack()

textwidth=450
backgroundcolor='#2B2B2B'
fgcolor="#A9B7C6"

#labels here
origlabel = Label(mainframe,text="maze")
origlabel.configure(font=("Consolas", 12))
origlabel.pack()

manhattanbutton = Button(mainframe,text="manhattan distance",command=solve_manhattan)
manhattanbutton.pack()
"""directbutton = Button(mainframe,text="direct distance",command=solve_direct)
    directbutton.pack()
"""
#   main menu here

menu = Menu(root, tearoff=False)
root.title("A* Maze Solver version 1.0")
root.config(menu=menu)

#submenu code goes here
filemenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open...", command=openfile)

filemenu.add_command(label="Help",command=showhelp)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

#bottombar code here
bottombar = Frame(root,bg="white")
bottombar.pack(side=BOTTOM, fill=X)

root.mainloop()
