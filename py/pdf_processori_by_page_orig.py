#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 13:39:28 2021
@author: jesseb
10/27/2021 - This is version 2 which will not use the TOC for documents
but just parse page numbers and content to create metadata
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
from pdfminer.pdfinterp import resolve1

####
#Read input pdf and convert to text
####
#Open a temp file so we can try to write page by page and catch what page causes error if there is one
file1=codecs.open("../tmp/pdf_miner_temp.txt","w","utf-8")
output_string = StringIO()
#Open up the pdf to process it
in_file = print_file = '../files/navrules.pdf'
#in_file = print_file = "Flags_Penants_Customs.pdf"
#in_file = print_file = "IEEE_1589-2020.pdf"

with open(in_file, 'rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    # This will give you the count of pages
    total_pages = str(resolve1(doc.catalog['Pages'])['Count'])
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    page_num = 0
    for page in PDFPage.create_pages(doc):
        page_num += 1
        print("Converting page " + str(page_num) + " of " + total_pages + " from pdf to text.", end='\r') #\r writes to same line
        interpreter.process_page(page)
        text = output_string.getvalue()
        text = "|||||PAGE:" + str(page_num) + "|||||\n" + text
        #Strip leading and trailing whitespaces (spaces and tabs)
        try:
            #text = "|||||PAGE:" + str(page_num) + "|||||\n" + text
            #file1.writelines("|||||PAGE:" + str(page_num) + "|||||")
            file1.writelines(text)
        except Exception as inst:
            print("\n*******ERROR WRITING PAGE " + str(page_num) + "\n")
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,
print("Converted page " + str(page_num) + " of " + total_pages + " from pdf to text.")
print("Closing temp file for error checking")
#get rid of temp file to give errors on page numbers
file1.close()
#os.remove("pdf_miner_temp.txt")
#write all text converted from pdf to file            
print("\nTrying to open pdfminer_out_full")
try:
    file2=codecs.open("../tmp/pdfminer_out_full.txt","w","utf-8")
    print("\nTrying to write pdfminer_out_full")
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


