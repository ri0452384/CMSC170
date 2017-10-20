from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

maze=[]
originalmazetext=""
closed_list=[]
open_list=[]

class Node():
    parent = None
    x=0
    y=0
    f=0
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

def get_node(node,position, character,g_value):
    if (character != '%'):
        x1,y1 = node.x, node.y
        value=0
        if position == 'l':
            x1 -= 1
        elif position == 'r':
            x1 += 1
        elif position == 'a':
            y1 -= 1
        elif position == 'b':
            y1 += 1
        else:
            print("direction not found")
        h = calculate_manhattan_heuristic(x1, y1)
        g_value += 1
        # f = g+h
        ans = Node(x1, y1, g_value + h, g_value, h)
        ans.parent = node
        return ans
    else:
        print("unpassable %s found!"%character)
        return None
#returns the node if the node was added, none otherwise
def check_open_list(node):
    global open_list
    for open_node in open_list:
        if node ==None:
            return None
        elif(node.x == open_node.x and node.y == open_node.y and node.g < open_node.g):
            print(node, open_node)
            open_list.append(node)
            open_list.remove(open_node)
            open_list = sorted(open_list,key=lambda x: x.f)
            return node
        else:
            open_list.append(node)
            open_list = sorted(open_list, key=lambda x: x.f)
            return node

#solves the maze via manhattan distance as the heuristic values
def solve_manhattan():
    global closed_list
    global open_list
    open_list = [Node]
    closed_list=[Node]
    parent=[Node]
    x,y = get_start()
    g=0
    heuristic = calculate_manhattan_heuristic(x,y)
    #starting Node is made the current because this will be added to the closed list
    current = Node(x, y, heuristic, g, heuristic)
    #f=g+h, but g is 0, therefore f=h.
    end_loop = False
    i=0
    while i < 5:
        open_list.append(current)
        closed_list.append(current)
        #get char to the left
        left = get_char_at(current.x-1,current.y)
        temp = get_node(current,'l',left,g)
        check_open_list(temp)
        #get char to the right
        right = get_char_at(current.x+1, current.y)
        temp = get_node(current, 'r', right, g)
        check_open_list(temp)
        #get char above
        above = get_char_at(current.x, current.y-1)
        temp = get_node(current, 'a', above, g)
        check_open_list(temp)
        #get char below
        below = get_char_at(current.x, current.y+1)
        temp = get_node(current, 'b', below, g)
        check_open_list(temp)
        print(current.x)
        print(current.y)
        print(closed_list)
        print(open_list)


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
