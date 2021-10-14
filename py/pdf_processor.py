#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 13:39:28 2021

@author: jesseb
"""


from io import StringIO
import codecs
import os
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

#assumptions about doc structure
#This is the list of what can be a valid page number
chr_num_list = ["i", "x", "v", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "\n"]
#This is the list of what is valid for separating the topic from page number in table of contents
chr_misc_list = [".", "_", " "]
#This is the list of what is valid for the title to the table of contents
toc_titles = ["CONTENTS", "GENERAL", "Contents"]

####
#Read input pdf and convert to text
####
#Open a temp file so we can try to write page by page and catch what page causes error if there is one
file1=codecs.open("..\tmp\pdf_miner_temp.txt","w","utf-8")
output_string = StringIO()
#Open up the pdf to process it
in_file = print_file = '/var/www/html/files/navrules.pdf'
#in_file = print_file = "Flags_Penants_Customs.pdf"
#in_file = print_file = "IEEE_1589-2020.pdf"

with open(in_file, 'rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    page_num = 0
    for page in PDFPage.create_pages(doc):
        page_num += 1
        print("Converting page " + str(page_num) + " from pdf to text.") #\r writes to same line
        interpreter.process_page(page)
        text = output_string.getvalue()
        #Strip leading and trailing whitespaces (spaces and tabs)
        try:
            file1.writelines(text)
        except Exception as inst:
            print("\n*******ERROR WRITING PAGE " + str(page_num) + "\n")
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
            pass
#get rid of temp file to give errors on page numbers
file1.close()
os.remove("pdf_miner_temp.txt")
#write all text converted from pdf to file            
try:
    file2=codecs.open(r"\..\tmp\pdfminer_out_full.txt","w","utf-8")
    file2.writelines(text)
except Exception as inst:
    print("\n*******ERROR WRITING pdfminer_out_full\n")
    print(type(inst))    # the exception instance
    print(inst.args)     # arguments stored in .args
    print(inst)          # __str__ allows args to be printed directly,
    pass
in_file.close()
device.close()
output_string.close()        
file2.close()

#Now open pdf converted text file and process it
file3=codecs.open(r"..\tmp\pdfminer_out_full.txt","r","utf-8")
Lines = file3.readlines()
toc=[] #create table of contents list
read_toc = 0
#read line by line
for line in Lines:
    #get table of contents
    stripped_line = line.strip(" \n") #strip leading spaces and newline char
    #turn on toc reading
    if stripped_line in toc_titles and read_toc != -1: #toc_titles list is what the header of the toc can be
        print("****TABLE OF CONTENTS FOUND")
        #turn on to read toc 
        read_toc = 1
    elif stripped_line in toc and read_toc != -1:
        #turn off to stop note read TOC, we have seen a topic in toc titles twice so your are in the body of the document
        read_toc = -1
        print("****END READING TABLE OF CONTENTS")
        file3.close()  #full pdf text ouput (entire doc)
        break #this loop is just getting TOC, don't need to read the rest of the doc        
    elif read_toc == 1 and stripped_line != '' and stripped_line != "\n":
        #we are reading the toc write the line to the list
        toc.append(stripped_line)
        
#we have written the raw toc to the toc list        
print('#####PRINTING TOC######')
#file for raw table of contents (will be used to parse toc)
file4=codecs.open(r"..\tmp\pdfminer_TOC.txt","w","utf-8")

#Convert raw toc list to parsed toc
#loop through toc list from raw doc and parse
for topic in toc:
    #Only process lines with data.
    if  topic.strip()!='' and topic.strip!="\n":
        #Check to make sure there is a page number at the end of the line,
        #if not subject wraps two lines so join them
        if topic[-1] not in chr_num_list:
            #just write the line now without newline character
            file4.writelines(topic + " ")
        else:    
            #write to raw TOC file
            file4.writelines(topic)  
            file4.writelines("\n")
###########################################################
# We have completed extracting the raw TOC from the doc.  #
# Now parse the raw toc list.                             #
###########################################################
            
file4.close()
#file for parsed table of contents (testing purposes this will justed be used as toc list)
file5=codecs.open(r"..\tmp\pdfminer_TOC_modified.txt","w","utf-8")
#file for raw table of contents open read to parse
file6=codecs.open(r"..\tmp\pdfminer_TOC.txt","r","utf-8")
Lines = file6.readlines()
full_out_lst = [] #filename, page number, metadata, descripton
for topic in Lines:
    skip_to_next = 0
    topic.strip(" \n")
    #reverse string to read it backwards
    topic = topic[::-1]
    #now since backwards will loop getting page number, including if roman numeral lowercase
    #reset page number for new line
    page_num = ""
    #First extract page number since reading backwards
    #emulate do while
    while True:
        chr = topic[0]
        if chr not in chr_num_list or len(topic) == 0:
            break
        else:
            page_num = chr + page_num
            topic = topic[1:]
            #to fix code bug where it is putting the actual page number
            #at the bottom of the page with no toc title
            if len(topic) == 0:
                skip_to_next = 1
                break
    page_num.strip(" \n")   
    
    #Now extract miscellaneous characters and whitespace to TOC element
    if skip_to_next != 1:
        #Emulate do while loop
        #extract miscellaneous characters between title and page number
        while True:
            chr = topic[0]
            if chr not in chr_misc_list and len(topic)>0:
                break
            else:
                topic = topic[1:]            
    
        #Extract TOC Title bu just reversing what is left of the string
        title = topic[::-1]    
        topic.strip()
        
        #Print extracted section title and page number
        if title != "":
            print("TITLE:" + title + " PAGE:" + page_num.strip("\n"))
            file5.writelines("TITLE:" + title + " PAGE:" + page_num.strip("\n") + "\n")
            #filename, page number, metadata, descripton
            list_temp = [print_file, page_num.strip(), title, ""]
            full_out_lst.append(list_temp)
            
print(full_out_lst)
file5.close() #parsed TOC output file (testing purposes)
file6.close() #raw TOC output (needed because this is what is read to be parsed)
##############################################################
# We have completed parsing raw TOC to page num and title    #
# Now read the rest of the doc and parse text for each title #
##############################################################
file7=codecs.open(r"..\tmp\pdfminer_out_full.txt","r","utf-8")
#read line by line
#build list of titles
title_lst = []
for i in range(len(full_out_lst)):
    title_lst.append(full_out_lst[i][2])
Lines = file7.readlines()
index = len(full_out_lst) - 1
length = len(title_lst[len(title_lst)-1])
process_file_flag = 0
index_next = 1
#save_for_next = ''
final_section_flag = 0
for line in Lines:
    #read line
    stripped_line = line.strip(" \n") #strip leading spaces and newline char
    #read till the end of TOC, just look till you see last entry for toc
    if process_file_flag == 0 and stripped_line[0:length].strip() == title_lst[len(title_lst)-1]:
        #we have found the end of TOC, start extracting text
        process_file_flag = 1 
        print("\n*********found end of TOC: " + stripped_line[0:length].strip()+"\n")
    elif process_file_flag == 1: #we have past TOC and now will parse actual text
        #loop through text till you get to the next TOC title
        #have to check only first 4 chr's because text has titles on multiple lines
        if len(stripped_line) > 4 and stripped_line[0:7].strip() in title_lst[index_next] and final_section_flag == 0:
            print("*******found next section: " + str(title_lst[index_next]))
            curr_section = stripped_line[0:length].strip()
            #update index to look for next section
            print("INDEX_NEXT:" + str(index_next))
            if index_next != len(title_lst) - 1: 
                index_next += 1
            else:
                final_section_flag = 1    
        else:
            #update list item
            if final_section_flag == 1:
                full_out_lst[index_next][3] = full_out_lst[index_next][3] + " " +stripped_line.strip()
            else:
                full_out_lst[index_next-1][3] = full_out_lst[index_next-1][3] + " " +stripped_line.strip()
                
file7.close()
#file for full parsed input file (for test)
file8=codecs.open(r"..\tmp\PDF_FULL_PARSED.txt","w","utf-8")

for i in range(len(full_out_lst)):
     #filename, page number, metadata, descripton
     file8.writelines("*************************************************************\n")
     file8.writelines("FILENAME:" + full_out_lst[i][0])
     file8.writelines("\n")
     file8.writelines("PAGE:" + full_out_lst[i][1])
     file8.writelines("\n")
     file8.writelines("METADATA:" + full_out_lst[i][2])
     file8.writelines("\n")
     file8.writelines("TEXT:" + full_out_lst[i][3])
     file8.writelines("\n")
     file8.writelines("*************************************************************\n\n")

file8.close()










