from PIL import Image
from wrapt_timeout_decorator import *

import os
import pytesseract
import json
import utilFunctions

#way to prevent pyteserreract command from freezing program
@timeout(30)
def imToStr(f):
    return pytesseract.image_to_string(f)


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

#main loop of program, searches through all files in the images_to_process folder
#runs them through the OCR then adds them to our dictionary
counter = 0
for path in os.scandir("images_to_process"):
    if path.is_file():

        print(counter)
        counter += 1

        #The path from which the file will be searchable by
        im = "processed_images/" + path.name

        #attempting to open the file
        try:
            imFile = Image.open("images_to_process/" + path.name)
        except:
            print(path.name, "was an invalid format")
            os.rename("images_to_process/" + path.name, "failed_processed_images/" + path.name)
            continue

        #attempting to run ocr file, imToStr has a max run time of 30 seconds
        try:
            imOutput = imToStr(imFile)
        except:
            print(path.name, "took to long to process")
            os.rename("images_to_process/" + path.name, "failed_processed_images/" + path.name)
            continue           

        #splitting words from file into a list
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



#We wait until we are done making changes to the datastructure before moving over all images
#that way if there is an issue during the processing of images we dont need to manually find
#and remove all of the images that got moved but did not save to the .json file
for path in os.scandir("images_to_process"):
    if path.is_file():
        os.rename("images_to_process/" + path.name, "processed_images/" + path.name)

#turning our sets back into arrays so we can save a JSON file 
utilFunctions.dictToJson(toJson)

#saving our data structure in a json
with open("data_file.json", "w") as write_file:
    json.dump(toJson, write_file)

"""
TODO:
add way to sort by date and user/other types of image IDing
expand list of common words and improve garbage identification
allow searcher to remove bad search results
"""




            

    
