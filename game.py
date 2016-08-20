from random import randint
import math, time
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.wm_title("Find Shortest Path")
        self.circleSize = 4
        master.resizable(width=False, height=False)
        master.geometry('{}x{}'.format(375, 256))
        self.pack()
        self.create_widgets()
        self.selectedNodes = []
        self.lastNode = None

    def mouseclickEvent(self, event):
        for node in self.nodes:
            if node.distance(Node(event.y, event.x)) <= self.circleSize**2:
                self.createLine(node)
                break

    def createLine(self, node):
        if node in self.selectedNodes:
            self.selectedNodes.remove(node)
            if len(self.selectedNodes) == 0:
                self.putNodesonScreen(nodesAvailable=True)
                self.makeButtons()
                return
        else:
            self.selectedNodes.append(node)
        self.putNodesonScreen(nodesAvailable=True)
        for n in self.selectedNodes:
            x0 = n.x-self.circleSize
            x1 = n.x+self.circleSize
            y0 = n.y-self.circleSize
            y1 = n.y+self.circleSize
            if not self.lastNode:
                self.lastNode = n
                self.canvas_thing.create_oval(x0, y0, x1, y1, fill="green")
                continue
            self.canvas_thing.create_line(self.lastNode.x, self.lastNode.y, n.x, n.y, fill="green")
            self.canvas_thing.create_oval(x0, y0, x1, y1, fill="green")
            self.lastNode = n
        self.makeButtons()
        self.lastNode = None
    
    def create_widgets(self):
        self.canvas_thing = tk.Canvas()
        self.results = tk.Button()
        self.clear = tk.Button()
        self.reset = tk.Button()
        self.quit = tk.Button()
        
        self.resetWindow()
    
    def putNodesonScreen(self, nodesAvailable=False):
        self.canvas_thing.destroy()
        self.results.destroy()
        self.clear.destroy()
        self.reset.destroy()
        self.quit.destroy()
        self.canvas_thing = tk.Canvas(self, height=256, width=256, bg="purple")
        if not nodesAvailable:
            self.nodes = self.makeNodes(randint(4, 8))
        
        for node in self.nodes:
            x0 = node.x-self.circleSize
            x1 = node.x+self.circleSize
            y0 = node.y-self.circleSize
            y1 = node.y+self.circleSize
            circle = self.canvas_thing.create_oval(x0, y0, x1, y1, fill="blue")
            
        self.canvas_thing.bind("<Button-1>", self.mouseclickEvent)

    def clearBoard(self):
        self.selectedNodes = []
        self.putNodesonScreen(nodesAvailable=True)
        self.makeButtons()

    def checkResults(self):
        hopefullythepersonknowswhattheyaredoing = self.compareAnswers()
        if hopefullythepersonknowswhattheyaredoing != "nahda" and hopefullythepersonknowswhattheyaredoing != "ERROR":
            print("Correct")
            print("Answer: " + str(hopefullythepersonknowswhattheyaredoing))
            tk.messagebox.showinfo("Congratulations", "You've found the shortest path!\nAnswer in length: "+str(hopefullythepersonknowswhattheyaredoing))
        elif hopefullythepersonknowswhattheyaredoing == "nahda":
            print("You Suck, Try Again xD")
            tk.messagebox.showinfo("Try Again", "The path you've made is not correct. Try again.")
        else:
            print("You didn't even select every node (%.%)")
            tk.messagebox.showinfo("Srsly", "You haven't selected every node on the screen, so I can't calculate your answer.")

    def compareAnswers(self):
        if len(self.selectedNodes) != len(self.nodes):
            return "ERROR"
        correctAnswer = bruteForcePath(self.nodes)
        startNode = None
        answerGiven = 0
        for node in self.selectedNodes:
            if not startNode:
                startNode = node
                continue
            answerGiven += node.distance(startNode)
            startNode = node
        print(str(answerGiven) + " == " +str(correctAnswer)+"?")
        if answerGiven == correctAnswer:
            return answerGiven
        return "nahda"

    def resetWindow(self):
        self.selectedNodes = []
        self.putNodesonScreen()
        self.makeButtons()

    def makeButtons(self):
        self.canvas_thing.pack(side="top")
        self.canvas_thing.pack(side="left")

        self.results = tk.Button(self)
        self.results["text"] = "Check Results"
        self.results["command"] = self.checkResults
        self.results.pack(side="top")

        self.clear = tk.Button(self)
        self.clear['text'] = "Clear Board"
        self.clear['command'] = self.clearBoard
        self.clear.pack()

        self.reset = tk.Button(self)
        self.reset['text'] = "Make New Board"
        self.reset['command'] = self.resetWindow
        self.reset.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def makeNodes(self, n):
        nodes = []

        for i in range(n):
            while True:
                node = Node(randint(10, 246), randint(10, 246))
                Okay = True
                x = 0
                for existingNode in nodes:
                    if ((node.x-existingNode.x)**2)+((node.y-existingNode.y)**2) <= self.circleSize**2:
                        Okay = False
                        break
                    x+=1
                if not Okay:
                    continue
                break
            nodes.append(node)

        for i in range(n):
            for j in range(i+1, n):
                nodes[i].pair(nodes[j])
                nodes[j].pair(nodes[i])

        return nodes

class Node:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.visited = False
        self.nodes = []

    def pair(self, node):
        self.nodes.append(node)
    
    def distance(self, node):
        return ((self.x-node.x)**2)+((self.y-node.y)**2)

def bruteForcePath(nodes):
    pathValues = []
    for i in range(len(nodes)):
        pathValues.append(findShortPath(nodes[i], 0))
        for node in nodes:
            node.visited = False
    return min(pathValues)

def findShortPath(node, pathCost):
    pathValues = []
    node.visited = True
    found = False
    for n in node.nodes:
        if not n.visited:
            found = True
            pathValues.append(findShortPath(n, pathCost+node.distance(n)))
            n.visited = False
    if not found:
        return pathCost
    return min(pathValues)

def main():
    root = tk.Tk()
    app = Application(master=root)
    #app.mainloop()
    while True:
        try:
            app.update()
        except:
            break

if __name__ == "__main__":
    main()
