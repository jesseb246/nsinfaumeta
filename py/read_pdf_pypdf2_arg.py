# -*- coding: utf-8 -*-
"""
Created on 11/1/2021
@author: jesseb
@descrption: process pdf file to text and parses out by page number
"""
import PyPDF2 #library for reading pages
import codecs #you need to use codecs or you will get errors on certain pages
import time #using this for slowing down output to screen for validation
import sys #to get arguments 
 
#create file object variable
#opening method will be rb
print("Python script called with arguments:")
print(sys.argv)
print("<br>")

#get filename input value, script name is arg[0], filename is arg[1]
print("Opening file for pdf conversion.<br>")
file_name = sys.argv[1] 
pdffileobj=open('/var/www/html/files/' + file_name,'rb')

print("Creating reader variable that will read pdffileobj.<br>")
#create reader variable that will read the pdffileobj
pdfreader=PyPDF2.PdfFileReader(pdffileobj)
 
#This will store the number of pages of this pdf file
x=pdfreader.numPages
print("Number of pages: " + str(x) + "<br>")

print("Looping through pages...<br>")
#loop through and read pages and also write to a list
full_out_lst =[] #filename, page number, metadata, descripton ##list for storing data to write to DB
for i in range(x-1):
    pageobj=pdfreader.getPage(i)
    text= pageobj.extractText()
    print("Processed Page Number: " + str(i+1) + "<br>") #write page numbers so you can parse output file
    list_tmp = [file_name, str(i+1), "metadata work in progress", text]
    full_out_lst.append(list_tmp)
        
pdffileobj.close()

#print the list to the screen for verification
for i in range(len(full_out_lst)):
    #pause for a second for validation purpose, this should all be removed when working
    #time.sleep(1)
    print("*************************************************************<br>")
    print("FILENAME:" + full_out_lst[i][0] + "<br>")
    print("\n")
    print("PAGE:" + full_out_lst[i][1] + "<br>")
    print("\n")
    print("METADATA:" + full_out_lst[i][2] + "<br>")
    print("\n")
    print("TEXT:" + full_out_lst[i][3] + "<br>")
    print("\n")
    print("*************************************************************\n\n")



