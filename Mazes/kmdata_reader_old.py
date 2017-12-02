from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import math
import matplotlib.pyplot as plt

points = []
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
        for i in range(0,300):
            one_line = file.readline().split(" ")
            x = float(one_line[1])
            y = float(one_line[2])
            node = (x,y)
            points.append(node)
        file.close()


def classify(points,centroids):
    ans=[]
    for p in points:
        distances = []
        for c in centroids:
            distance = math.sqrt((p[0] - c[0])**2.0+(p[1] - c[1])**2.0)
            distances.append(distance)
        classification = distances.index(min(distances))
        """assign centroid and distance"""
        q = p,classification,min(distances)
        ans.append(q)
    return ans

def k_means(points,centroids,max_iteration):
    new_image_values = []
    current_j = 0.0
    previous_j = 0.0
    for iteration in range(max_iteration):
        """ assign each point to a centroid
            each element of the classes array is: [0]original point, [1] centroid_id, [2] distance
        """
        classes = classify(points,centroids)
        """do the graph printing code using classes here:"""
        """plot the centroids"""
        centroid_color = ['r','m','b']
        point_color = ['g','c','y']
        for i in range(0,3):
            """plot centroid for each group"""
            plt.scatter(centroids[i][0],centroids[i][1],10,centroid_color[i])
            """plot the points that belong to the same group"""
            eks = []
            why = []
            for point in classes:
                if point[1] == i:
                    eks.append(point[0][0])
                    why.append(point[0][1])
            plt.scatter(eks,why,1,point_color[i])
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Iteration: %s'%iteration)
        plt.show()
        new_image_values.clear()
        for new_p in classes:
            n_x = centroids[new_p[1]][0]
            n_y = centroids[new_p[1]][1]
            np = n_x,n_y
            new_image_values.append(np)
        #classes should update
        #update centroids:
        for i in range(0,3):
            sum_x = 0.0
            sum_y = 0.0
            average_x = 0.0
            average_y = 0.0
            count = 0.0
            for point in classes:
                if point[1] == i:
                    sum_x += point[0][0]
                    sum_y += point[0][1]
                    count +=1
            centroids[i] = (float(sum_x/count),float(sum_y/count))
        #computing for J:
        total=0.0
        count = 0.0
        for point in classes:
            total += point[2]
            count += 1.0
        current_j = total / count
        difference_j = current_j - previous_j
        previous_j = current_j
        #write current centroid assignments to _ca file:
        with open('iter'+(iteration+1).__str__()+'_ca.txt',"w+") as file:
            to_write = ''
            for p in classes:
                to_write += p[1].__str__()+"\n"
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
        print(new_image_values)
        classes.clear()
    return new_image_values

def solve():
    global points
    iterations = 10
    initial_centroids = list()
    initial_centroids.append((3.0, 3.0))
    initial_centroids.append((6.0, 2.0))
    initial_centroids.append((8.0, 5.0))
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

