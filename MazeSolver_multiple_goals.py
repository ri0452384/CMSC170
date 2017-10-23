"""
Maze Solver 1.0 for Multiple goal mazes
By: Ingles, Oculam, Yap
"""
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

maze=[]
originalmazetext=""
closed_list=[]
open_list=[]
goals=[]
start_x=0
start_y=0

class Node():
    parent = None
    f=0
    x=0
    y=0
    def __init__(self,ex,why,eff,gee,haych):
        self.x = int(ex)
        self.y = int(why)
        self.f = int(eff)
        self.g = int(gee)
        self.h = int(haych)
    def __copy__(self):
        copy = Node(self.x,self.y,self.f,self.g,self.h)
        copy.parent = self.parent
        return copy

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
    global goals
    return goals[0]

def set_all_goals():
    x0,y0=get_start()
    y, x = len(maze), len(maze[0])
    for i in range(0, y-1):
        for j in range(0, x-1):
            if maze[i][j] == ".":
                d=0
                goals.append([j,i,d])

#returns the manhattan distance from current point to goal
def calculate_manhattan_heuristic(x1,y1):
    x2,y2,d2 = get_goal()
    print("goal: ",x2,y2)
    return abs(x2-x1)+abs(y2-y1)

#returns the direct distance as defined by MP
def calculate_direct_heuristic(x1,y1):
    x2,y2,d2 = get_goal()
    print("goal: ", x2, y2)
    return max(abs(x2-x1),abs(y2-y1))

#scans through the maze and returns what char is occupying tile x,y
def get_char_at(x,y):
    return maze[y][x]

#writes a character to a specified coordinate on the maze file
def set_char_at(x,y,character):
    maze[y][x] = character

def get_node(position, character,g_value):
    global open_list
    global current
    global h_flag
    if (character != '%'):
        x1 = current.x
        y1 = current.y
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

        if h_flag == 'manhattan':
            h = calculate_manhattan_heuristic(x1, y1)
        elif h_flag == 'direct':
            h = calculate_direct_heuristic(x1, y1)
        else:
            print("error: heuristic undefined!")
        g_value = current.g + 1
        # f = g+h
        ans = Node(x1, y1, g_value + h, g_value, h)
        ans.x=x1
        ans.y=y1
        ans.parent = current.__copy__()
        print("node: %s, parent: %s"%(ans,current))
        return ans
    else:
        print("unpassable %s found!"%character)
        return None
"""helper method that checks whether the node is on the open list or not
    returns True if found, False otherwise
"""
def in_the_open_list(node):
    for element in open_list:
        if node.x == element.x and node.y == element.y:
            #if node has lower g cost, place this in the open list instead
            if node.g < element.g:
                open_list.append(node)
                open_list.remove(element)
            return True

        else:
            return False

def in_the_closed_list(node):
    for element in closed_list:
        if node.x == element.x and node.y == element.y:
            return True
    return False

def solve_manhattan():
    solve("manhattan")

def solve_direct():
    solve("direct")

def calculate_goals(h_flag):
    global goals
    global start_y
    global start_x
    if h_flag=='manhattan':
        print('manhattan_logic')
        for g in goals:
            x, y, distance = g
            g[2] = abs(g[0] - start_x) + abs(g[1] - start_y)
            x,y,distance = g
    elif h_flag == 'direct:':
        print('direct_logic')
        for g in goals:
            x, y, distance = g
            g[2] = max(abs(g[0] - start_x), abs(g[1] - start_y))
            x, y,distance = g
    goals = sorted(goals, key=lambda x : x[2], reverse=False)
    return goals

#solves the maze via manhattan distance as the heuristic values
def solve(heuristic_flag):
    global start_x
    global start_y
    global h_flag
    h_flag = heuristic_flag
    #opens the file
    openfile()
    global closed_list
    global open_list
    global current
    open_list = [Node]
    closed_list = [Node]
    # take note of all the goals and save it in a list
    set_all_goals()
    calculate_goals(heuristic_flag)
    x0, y0 = get_start()
    start_y = y0
    start_x = x0
    # WE WILL KEEP TRACK OF X AND Y
    g = 0
    sol_cost = 0
    expanded_nodes = 0
    frontier = 0
    goals = calculate_goals(h_flag)
    print(goals)
    if heuristic_flag=="manhattan":
        heuristic = calculate_manhattan_heuristic(x0,y0)
    elif heuristic_flag =="direct":
        heuristic = calculate_direct_heuristic(x0, y0)
    #starting Node is made the current because this will be added to the closed list
    current = Node(x0, y0, heuristic, g, heuristic)
    current_goal = goals[0]
    x2,y2,d2 = current_goal
    food_count = 0
    #f=g+h, but g is 0, therefore f=h
    while True:
        open_list.append(current)
        closed_list.append(current)
        sol_cost += 1
        if current.x == x2 and current.y == y2:
            print("goal found!", current, get_goal())
            food_count +=1
            set_char_at(x2,y2,(food_count).__str__())
            # todo: recalculate the goals, new_start = old_goal
            if(len(goals) > 0):
                x0, y0,d0 = goals.pop(0)
                start_x = x0
                start_y = y0
                goals = calculate_goals(h_flag)
                if (len(goals) == 0):
                    print("all goals found!")
                    break
                frontier += len(open_list)
                open_list = [Node]
                expanded_nodes += len(closed_list)
                closed_list = [Node]
                g = 0
                # take note of all the goals and save it in a list
                print(goals)
                if heuristic_flag == "manhattan":
                    heuristic = calculate_manhattan_heuristic(x0, y0)
                elif heuristic_flag == "direct":
                    heuristic = calculate_direct_heuristic(x0, y0)
                # starting Node is made the current because this will be added to the closed list
                current = Node(x0, y0, heuristic, g, heuristic)
                current_goal = goals[0]
                x2, y2,d2 = current_goal
                open_list.append(current)
                closed_list.append(current)
                sol_cost += 1
        open_list.remove(current)
        #get char to the left
        left = get_char_at(current.x-1,current.y)
        temp = get_node('l',left,g)
        if temp != None and not in_the_open_list(temp) and not in_the_closed_list(temp):
            open_list.append(temp)
        #get char to the right
        right = get_char_at(current.x+1, current.y)
        temp = get_node('r', right, g)
        if temp != None and not in_the_open_list(temp)and not in_the_closed_list(temp):
            open_list.append(temp)
        #get char above
        above = get_char_at(current.x, current.y-1)
        temp = get_node('a', above, g)
        if temp != None and not in_the_open_list(temp)and not in_the_closed_list(temp):
            open_list.append(temp)
        #get char below
        below = get_char_at(current.x, current.y+1)
        temp = get_node('b', below, g)
        if temp != None and not in_the_open_list(temp)and not in_the_closed_list(temp):
            open_list.append(temp)
        open_list = sorted(open_list, key=lambda x:x.f,reverse=False)
        current = open_list.pop(1)
    # #traceback the parent of every current Node until we get back to the starting tile
    # parent = []
    # set_char_at(current.x, current.y, 'G')
    # current = current.parent
    # while(current.x !=x0 or current.y != y0):
    #     parent.append(current)
    #     set_char_at(current.x,current.y,'*')
    #     current = current.parent
    solutioncost.config(text="solution cost: %s\nnodes expanded: %s\nfrontier: %s" % (sol_cost, expanded_nodes, frontier))
    draw_maze()

def draw_maze():
    mazeoutput=""
    for line in maze:
        for character in line:
            mazeoutput+=character
    origlabel.config(text=mazeoutput)

def openfile():
    global originalmazetext
    global maze
    maze=[]
    originalmazetext =""
    filename = filedialog.askopenfilename( filetypes = ( ("Text file", "*.txt"),("All files", "*.*")))
    with open(filename) as file:
        content = file.readlines()
    for line in content:
        row = list(line)
        maze.append(row)
    draw_maze()

def showhelp():
    messagebox.showinfo(title='A* Maze Solver Help',message='1. Click Direct/Manhattan distance button.\n2. Select the maze file\n3. It will open the file and solve the maze automatically.\n4. To solve another maze, close the window and relaunch the program.')

root = Tk()

#**************************UI**************** main window code goes  here
root.minsize(width=325,height=100)
#left frame here
mainframe = Frame(root,bg='#2B2B2B')
mainframe.pack()

textwidth=450
backgroundcolor='#2B2B2B'
fgcolor="#A9B7C6"
#buttons here
manhattanbutton = Button(mainframe,text="manhattan distance",command=solve_manhattan)
manhattanbutton.pack()
directbutton = Button(mainframe,text="direct distance",command=solve_direct)
directbutton.pack()

#labels here
origlabel = Label(mainframe,text="maze")
origlabel.configure(font=("Consolas", 12))
origlabel.pack()
solutioncost = Label(mainframe,text="solution cost\nnodes expanded:")
solutioncost.pack()


#   main menu here

menu = Menu(root, tearoff=False)
root.title("A* Maze Solver version 1.0")
root.config(menu=menu)

#submenu code goes here
filemenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Help",command=showhelp)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

#bottombar code here
bottombar = Frame(root,bg="white")
bottombar.pack(side=BOTTOM, fill=X)

root.mainloop()