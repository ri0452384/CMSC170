from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import math

class Node():
    x = 0.0
    y = 0.0
    centroid_id = -1
    distance = 0.0;
    def __init__(self,ex,why):
        self.x = ex
        self.y = why
        self.distance = 0.0;

    def __copy__(self):
        copy = Node(self.x,self.y,self.distance)
        return copy

    def __str__(self):
        return "%s, %s" % (self.x, self.y)

    def __repr__(self):
        return "%s, %s" % (self.x, self.y)


class Group():
    members = [Node]
    head = Node(0.0,0.0)

    def __copy__(self):
        copy = Group(self.members,self.head)
        return copy

    def __str__(self):
        return "<centroid:%s, %s>" % (self.head.__str__(),self.members.__str__())

    def __repr__(self):
        return "<centroid:%s, %s>" % (self.head.__str__(),self.members.__str__())

points = [Node]
k=3
classes = []
filename=None
means = []   #means of clusters


#open function
def openfile():
    global content
    global filename
    global points
    filename = filedialog.askopenfilename( filetypes = ( ("Text file", "kmdata1.txt"),("All files", "*.*")))
    with open(filename) as file:
        for i in range(1,300):
            one_line = file.readline().split(" ")
            x = float(one_line[1])
            y = float(one_line[2])
            node = Node(x,y)
            points.append(node)
        file.close()


def classify(points,centroids):
    global k
    global classes
    for i in range(k):
        g = [Node]
        classes.append(g)
    for p in points:
        distances = []
        for c in centroids:
            distance = math.sqrt((p.x - c.x)**2.0+(p.y - c.y)**2.0)
            distances.append(distance)
        classification = distances.index(min(distances))
        p.centroid_id = classification
        p.distance = min(distances)
        classes[classification].append(p)
    return classes

def k_means(points,centroids,max_iteration):
    global classes
    current_j = 0
    previous_j = 0
    for iteration in range(max_iteration):
        print(iteration)
        #classify all points according to closest centroid
        classes = classify(points,centroids)
        #update centroids:
        for i in range(0,3):
            sum_x = 0.0
            sum_y = 0.0
            average_x = 0.0
            average_y = 0.0
            for point in classes[i]:
                sum_x += point.x
                sum_y += point.y
            print(len(classes[i])-1)
            average_x = sum_x/(len(classes[i])-1)
            average_y = sum_y/(len(classes[i])-1)
            centroids[i].x = average_x
            centroids[i].y = average_y
        #computing for J:
        total=0.0
        count = 0.0
        for p in points:
            total += p.distance
            count += 1.0
        current_j = total / count
        difference_j = current_j - previous_j
        previous_j = current_j
        #write current centroid assignments to _ca file:
        with open('iter'+(iteration+1).__str__()+'_ca.txt',"w+") as file:
            to_write = ''
            for p in points:
                to_write += p.centroid_id.__str__()+"\n"
            file.write(to_write)
            file.close()
        with open('iter'+(iteration+1).__str__()+'_cm.txt',"w+") as file:
            to_write = ''
            for c in centroids:
                to_write += c.__str__()+"\n"
            to_write += "J = "+current_j.__str__() + "\n"
            to_write += "dJ = "+difference_j.__str__() + "\n"
            file.write(to_write)
            file.close()

def solve():
    iterations = 10
    initial_centroids = Node(3.0, 3.0), Node(6.0, 2.0), Node(8.0, 5.0)
    k_means(points,initial_centroids,iterations)

#help file
def showhelp():
    messagebox.showinfo(title='K-Means Help',message='(1) Open a file using File> Open...\n (2) Click calculate button.')

root = Tk()
root.minsize(width=325,height=100)
#left frame here
mainframe = Frame(root,bg='#2B2B2B')
mainframe.pack()

textwidth=450
backgroundcolor='#2B2B2B'
fgcolor="#A9B7C6"

###
#labels here
solve_button = Button(mainframe,text="Calculate K-Means for 10 iterations",command=solve)
solve_button.pack()



#   main menu here

menu = Menu(root, tearoff=False)
root.title("K-Means calculator")
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

root.mainloop()
