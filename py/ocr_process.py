#Main instalation
import os
from shutil import move
import fitz
import pytesseract as tess
from PIL import Image
tess.pytesseract.tesseract_cmd= r'C:\Users\aleja\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


current_directory = os.path.dirname(os.path.abspath(__file__))
file_name = input("Enter the pdf file name: ")
try:
    file= fitz.open(file_name)
except:
    print("Searching for the file in the current directory")
    file_name = current_directory + "\\" + file_name
    file= fitz.open(file_name)
    if file is None:
        print("File not found")
        exit()
    
directory_name = input("Enter the directory name for the extracted data: ")

current_directory = os.path.join(current_directory, directory_name)
if not os.path.exists(current_directory):
    os.mkdir(current_directory)

images = []

#For text
for pageNumber, page in enumerate(file.pages(), start=1):

    #Get Text
    text= page.getText()

    file_name_ = "page_" + str(pageNumber) + ".txt"
    #Save all Text into a single TXT file with an append mode
    txt=open(file_name_, 'a')
   
    #Write the text 
    txt.writelines(text)
    txt.close()
 
    # Move the TXT file to the current directory
    os.mkdir(current_directory+"\\"+"Text")
    move(os.path.join(os.getcwd(),file_name_), os.path.join(current_directory + "\\TEXT\\",file_name_))

#for image

#Get the page number and page information enumarated
for pageNumber, page in enumerate(file.pages(), start=1):


    #Get the location of the image
    for imgNumber, img in enumerate(page.getImageList(),start= 1):
        xref= img[0]


    #Create
        pix=fitz.Pixmap(file,xref)
        #Bits per pixel
        if pix.n >4:

            pix=fitz.Pixmap(fitz.csRGB,pix)  #since this is not RBG or GREY it is converted into PIX
        
       
        image_name = f'a_Page_{pageNumber}_Image_{imgNumber}.png'
        pix.writePNG(image_name)

        # Move the image to the current directory
        os.mkdir(current_directory+"\\"+"Images")
        move(os.getcwd()+"\\"+image_name, current_directory + "\\IMAGES\\"+image_name)
        images.append(image_name)
        
# printing the text from the image
for image in images:
    img= Image.open(current_directory+"\\IMAGES\\" + image)
    ocr = tess.image_to_string(img, lang='eng',config='-c page_separator=')
    print(ocr)
    
