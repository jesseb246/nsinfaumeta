# -*- coding: utf-8 -*-
"""
Created on 11/1/2021
@author: jesseb
@descrption: process pdf file to text and parses out by page number
"""
import PyPDF2 #library for reading pages
import codecs #you need to use codecs or you will get errors on certain pages
import time #using this for slowing down output to screen for validation
 
#create file object variable
#opening method will be rb
file_name = 'navrules.pdf'
pdffileobj=open('../files/' + file_name,'rb')
 
#create reader variable that will read the pdffileobj
pdfreader=PyPDF2.PdfFileReader(pdffileobj)
 
#This will store the number of pages of this pdf file
x=pdfreader.numPages
print("Number of pages: " + str(x))

#open file to write to
file1=codecs.open("../tmp/pypdf2out.txt","w","utf-8")
#loop through and read pages and also write to a list
full_out_lst =[] #filename, page number, metadata, descripton ##list for storing data to write to DB
for i in range(x-1):
    pageobj=pdfreader.getPage(i)
    text= pageobj.extractText()
    print("Processing Page Number: " + str(i+1), end='\r') #write page numbers so you can parse output file
    try:
        file1.writelines("\n|||||PAGE:" + str(i+1) + "|||||\n")
        file1.writelines(text)
    except:
        print("\n*******ERROR WRITING PAGE " + str(i+1) + "\n")
        pass
    #write the data to the list for insertion into the database
    list_tmp = [file_name, str(i+1), "metadata work in progress", text]
    full_out_lst.append(list_tmp)
        
pdffileobj.close()
file1.close()

#print the list to the screen for verification
for i in range(len(full_out_lst)):
    #pause for a second for validation purpose, this should all be removed when working
    #time.sleep(1)
    print("*************************************************************\n")
    print("FILENAME:" + full_out_lst[i][0])
    print("\n")
    print("PAGE:" + full_out_lst[i][1])
    print("\n")
    print("METADATA:" + full_out_lst[i][2])
    print("\n")
    print("TEXT:" + full_out_lst[i][3])
    print("\n")
    print("*************************************************************\n\n")



