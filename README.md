**SETUP:**
1) Create a folder that will contain all of the python files and necessary sub folders
2) Place the three python scripts all in this folder
3) Within this folder create three more sub folders named "images_to_process", "failed_processed_images", and "processed_images"
4) You may neeed to install tesseract/py tersseract, https://pypi.org/project/wrapt-timeout-decorator/, and python itself if these are not already on your machine

**ADDING IMAGES TO SEARCH ENGINE:**
1) Move all images you wish to search by into the "images_to_process" folder
2) Run "imageAdder.py"
3) Any image that was sucessfully added to your search database will have been moved to "processed_images" and any file that could not be processed will end up in "failed_processed_images"

**SEARCHING FOR IMAGES:**

Once images have been added by the above process simply run "imageSearcher.py" and follow the instructions in the program
