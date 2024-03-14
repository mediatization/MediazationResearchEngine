from PIL import ImageTk, Image
import tkinter as tk
import json
import utilFunctions


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
        root.geometry('400x250')

        #instructions for user
        instructions = tk.Label(root, text="enter key words you want to search by seperated with spaces\nonly images which contain all key words will be shown")
        instructions.pack()

        #creating search bar
        self.search = tk.Entry(root, width=30)
        self.search.pack()

        #creating search button
        searchBtn = tk.Button(root, text = "search" , command=self.getSearch)
        searchBtn.pack()

        root.mainloop()
    
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
                #adding all relevant images to array
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
        err.geometry("400x200")
        s = "Error: " + str(kw)
        explanation = tk.Label(err, text=s)
        explanation.pack()
        err.mainloop()

class searchWindow():
    def __init__(self, filteredResults):
        res = tk.Toplevel()
        res.title("Results of search")
        res.geometry("400x400")
    

        #for keeping track of which image we are looking at
        self.index = 0
        
        #displaying first image
        self.img = ImageTk.PhotoImage(Image.open(filteredResults[self.index]))
        self.display = tk.Label(res, image = self.img)
        self.display.pack()
        
        #gui element to tell us index of image
        s = "Showing image: " + str(self.index+1) + "/" + str(len(filteredResults)), "(" + filteredResults[self.index] + ")"
        self.totalIM = tk.Label(res, text=s)
        self.totalIM.pack(side=tk.BOTTOM)
        
        #important for button functions
        self.filteredResults = filteredResults

        #buttons for controlling which image is displayed
        backBtn = tk.Button(res, text = "previous image", command=self.prevImage)
        backBtn.pack(side=tk.LEFT)
        
        fwdBtn = tk.Button(res, text = "next image", command=self.nextImage)
        fwdBtn.pack(side=tk.RIGHT)

        res.mainloop()

    #controls for sorting thru images    
    def prevImage(self):
        #safeguards against moving out of bounds
        if self.index*-1 == len(self.filteredResults) -1:
            self.index = 0
        else:
            self.index -= 1
            
        #opening image and updating our label
        self.img = ImageTk.PhotoImage(Image.open(self.filteredResults[self.index]))
        self.display.config(image=self.img)
        #determing which index to display to user
        displayIndex = self.index
        if displayIndex < 0:
            displayIndex = len(self.filteredResults) + displayIndex
        #giving user information about the search results
        s = "Showing image: " + str(displayIndex+1) + "/" + str(len(self.filteredResults)), "(" + self.filteredResults[self.index] + ")"
        self.totalIM.config(text=s)

    def nextImage(self):
        if self.index == len(self.filteredResults) - 1:
            self.index = 0
        else:
            self.index += 1

        self.img = ImageTk.PhotoImage(Image.open(self.filteredResults[self.index]))
        self.display.config(image=self.img)
        displayIndex = self.index
        if displayIndex < 0:
            displayIndex = len(self.filteredResults) + displayIndex
        s = "Showing image: " + str(displayIndex+1) + "/" + str(len(self.filteredResults)), "(" + self.filteredResults[self.index] + ")"
        self.totalIM.config(text=s)




mainWindow()