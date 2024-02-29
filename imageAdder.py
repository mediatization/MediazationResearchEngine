from PIL import Image

import os
import pytesseract
import json
import utilFunctions

#opening the json file
#should be a dictionary with key value being words/dates/users
#value pairs are a list of path directories to corresponding images
try:
    with open("data_file.json", "r") as read_file:
        toJson = json.load(read_file)
    
    #converting the arrays to sets for faster adding/searching
    utilFunctions.jsonToDict(toJson)

except:
    #if json file does not exist create a new one
    print("No data file found, creating new")
    toJson = {}


#list of common words that we wont want to search through, may want to expand at some point
prepositions = {"about", "above", "across", "after", "against", "along", "among", "around", "before",
"behind", "below", "beneath", "beside", "between", "beyond", "despite", "down", "during", "except", 
"for", "from", "inside", "into", "like", "near", "off", "onto", "opposite", "out", "outside",
"over", "past", "round", "since", "than", "through", "toward", "under", "underneath", "unlike",
"until", "upon", "via", "with", "within", "without"}

#early stop is just for testing purposes will be removed in later iterations
counter = 0
#main loop of program, searches through all files in the needsProcessing folder
#runs them through the OCR then adds them to our dictionary
for path in os.scandir("images_to_process"):
    if path.is_file():
        print("Images processed:", counter)

        #moving image to new location
        im = "processed_images/" + path.name
        os.rename("images_to_process/" + path.name, im)

        #finding all words in the image and then turning it into an array we can iterate through
        imOutput = pytesseract.image_to_string(Image.open(im))
        imOutput = imOutput.split()

        #iterating through all words in the image
        for word in imOutput:
            word = word.lower()
            #Checking if a word in an image is something we might want to search by 
            if len(word) > 2 and word.isalpha() and word not in prepositions:
   
                #check if word is already a key value in dictionary, if it is simply 
                #add new file path to the set at that key value, otherwise create a 
                #new key value with a new set
                if word not in toJson:
                    toJson[word] = {im}
                else:
                    #do not need to worry abt images having a word multiple times as the
                    #set already checks image is not associated with word before adding it
                    toJson[word].add(im)
        
        counter += 1
        
            

#testing purposes will be removed later
for x in toJson:
    print("Word:", x)
    print("Images:", toJson[x])

#turning our sets back into arrays so we can save a JSON file 
utilFunctions.dictToJson(toJson)

#saving our data structure in a json
with open("data_file.json", "w") as write_file:
    json.dump(toJson, write_file)

"""
todo:
search by multiple keywords
potentially add way to sort by date and stuff
expand list of common words and improve garbage identification?
"""




            

    
