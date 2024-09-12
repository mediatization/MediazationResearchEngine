from PIL import ImageTk, Image
import tkinter as tk
import json
import utilFunctions
import os


class mainWindow():
    def __init__(self):
        #attempting to open the file
        self.toDict = None
        try:
            with open("data_file.json", "r") as read_file:
                self.toDict = json.load(read_file)
            utilFunctions.jsonToDict(self.toDict)
        except:
            print("Data File Not found")
            exit()

        #basic defines for root window
        root = tk.Tk()
        root.title("OCR searcher")

        #instructions for user
        instructions = tk.Label(root, text="enter key words you want to search by seperated with spaces\nonly images which contain all key words will be shown")
        instructions.pack()

        #creating search bar
        self.search = tk.Entry(root, width=30)
        self.search.pack()

        #creating search button
        searchBtn = tk.Button(root, text = "search" , command=self.getSearch)
        #allowing user to search via a key command
        root.bind("<Return>", self.commandSearch)
        searchBtn.pack()

        root.mainloop()
    
    #for whatever reason the binded version of the command passes in two arguments
    #we simply ignore the second argument and call the actual function with the
    #right number of arguments
    def commandSearch(self, a):
        self.getSearch()

    #creating search button
    def getSearch(self):
        #getting keywords from search bar
        keyWords = self.search.get().lower()
        keyWords = keyWords.split()

        #map which tracks how many of the listed keywords an image has
        unfilteredResults = {}
        for i in range(len(keyWords)):
            #checking that keyword is searchable
            if keyWords[i] in self.toDict:
                #adding all relevant images to map
                for im in self.toDict[keyWords[i]]:
                    if im not in unfilteredResults:
                        unfilteredResults[im] = 1
                    else:
                        unfilteredResults[im] += 1
            else:
                #if a given keyword does not exist create a basic error window and stop the function     
                errorWindow("No image with keyword: " + keyWords[i])
                return
        
        #list which stores the images whichs contain every keyword
        filteredResults = []
        for result in unfilteredResults.keys():
            if(unfilteredResults[result] == len(keyWords)):
                filteredResults.append(result)

        #opening search window to display results 
        if(len(filteredResults) != 0):
            searchWindow(filteredResults)
        else:
            errorWindow("no Image with all listed keywords")


#very basic class to tell user something has gone wrong
class errorWindow():
    def __init__(self, kw):
        err = tk.Toplevel()
        err.title("error")
        s = "Error: " + str(kw)
        explanation = tk.Label(err, text=s)
        explanation.pack()
        err.mainloop()

class searchWindow():
    def __init__(self, filteredResults):
        self.root = tk.Toplevel()
        self.root.title("Results of search")
    
        #for keeping track of which image we are looking at
        self.index = 0

        #important for button functions
        self.filteredResults = filteredResults

        #ui element for displaying the image
        self.display = tk.Label(self.root)
        #global variable to track the image
        self.img = None
        self.display.grid(row=1, column=1)
        
        #gui element to tell us index of image
        self.totalIM = tk.Label(self.root)
        self.totalIM.grid(row=0, column=1)

        #button to save notes
        saveNotesBtn = tk.Button(self.root, text = "save notes", command=self.saveNotes)
        saveNotesBtn.grid(row=3, column=1)

        #text widget for taking notes on current image
        self.notesWindow = tk.Text(self.root)
        self.notesWindow.grid(row=4, column=1)

        #if we have more than one search result add buttons for navigating between them
        if(len(self.filteredResults) > 1):
            fwdBtn = tk.Button(self.root, text = "next image", command=self.nextImage)
            fwdBtn.grid(row=1, column=2)

            backBtn = tk.Button(self.root, text = "previous image", command=self.prevImage)
            backBtn.grid(row=1, column=0)

        #filling in all our ui elements with data
        self.updateDisplay()

        self.root.mainloop()

    #controls for sorting thru images, just updates current index then calls update display function    
    def prevImage(self):
        #saving notes before switching images
        self.saveNotes()

        #safeguards against moving out of bounds
        if self.index*-1 == len(self.filteredResults) -1:
            self.index = 0
        else:
            self.index -= 1
        
        self.updateDisplay()

    def nextImage(self):
        #saving notes before switching images
        self.saveNotes()
        
        #safeguards against moving out of bounds
        if self.index == len(self.filteredResults) - 1:
            self.index = 0
        else:
            self.index += 1

        self.updateDisplay()

    #save notes from textbox to a file
    def saveNotes(self):
        #opening the file, writing to the file the new notes then closing the file
        file = open("./image_notes/" + self.filteredResults[self.index][17:-4] + ".txt", "w")
        file.write(self.notesWindow.get("1.0", "end"))
        file.close()

    #updates all elements of our display each time we
    def updateDisplay(self):
        #updating the image
        self.updateImage()

        #updating the notes to match the image
        self.updateNotes()

        #updating the image meta data
        self.updateMetaData()


    #updating the image being displayed based on current index
    def updateImage(self):
        #opening image
        unsizedImage = Image.open(self.filteredResults[self.index])
        
        #halving size of image if its too big
        if(unsizedImage.width > self.root.winfo_screenwidth() * .60 or unsizedImage.height > self.root.winfo_screenheight() * .60):
            widthReduction = unsizedImage.width - self.root.winfo_screenwidth() * .60
            heightReduction = unsizedImage.height - self.root.winfo_screenheight() * .60
            unsizedImage = unsizedImage.resize((int(unsizedImage.width - widthReduction), int(unsizedImage.height - heightReduction)))
        
        #displaying image
        self.img = ImageTk.PhotoImage(unsizedImage)
        self.display.config(image=self.img)

    #upates the notes to be that of the current image
    def updateNotes(self):
        #checking if notes already exist for given image
        fName = "./image_notes/" + self.filteredResults[self.index][17:-4] + ".txt"
        if os.path.isfile(fName):
            #if file exists read its contents into the notes box
            file = open(fName, "r")
            self.notesWindow.delete("1.0", "end")
            self.notesWindow.insert("end", file.read())
            file.close

    #updating the meta data such as where image is stored and what number search result it is
    def updateMetaData(self):
        #determing which index to display to user
        displayIndex = self.index
        if displayIndex < 0:
            displayIndex = len(self.filteredResults) + displayIndex
        #giving user information about the search results
        s = "Showing image: " + str(displayIndex+1) + "/" + str(len(self.filteredResults)), self.filteredResults[self.index]
        self.totalIM.config(text=s)


mainWindow()
