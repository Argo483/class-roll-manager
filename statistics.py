#!/usr/bin/env python

import os
import sys

def readtable(filename):
   fp=open(filename)
   mytable = []
   for line in fp:
      if not line.startswith("#"):
         mytable.append(line.rstrip("\n").split(":"))
   fp.close()
   return mytable
   
def readlines(filename):
   fp=open(filename)
   mylinelist = []
   for line in fp:
      if not line.startswith("#"):
         mylinelist.append(line.rstrip("\n"))
   fp.close()
   return mylinelist  

# This function is used to count the number of students in a roll file. 
# def countEnroledStudents(filename):
   # numStudents=0
   
   # try:
      # fp = open(filename)
   # except IOError:
      # If the file does not exist, I assume there are 0 students enroled in 
      # that subject, so I just return numStudents
      # return numStudents
   # For each student number in the file, add 1 to numStudents   
   # for student in fp:
      # numStudents+=1
   # return numStudents   
   
def readEnrolFile(rollFilename):
   studentList=[]
   try:
      roll = open(rollFilename)
   except IOError:
      #If the roll file does not exist for that class, I assume that there
      #are 0 students for that class, so I return the empty studentList
      return studentList
   #Append each student number in the roll file to the student list
   for student in roll:
      if not student.startswith("#"):
         studentList.append(student.rstrip("\n"))
   return studentList    
   
#This function takes a classCode and a classTable (the classTable and 
#subjectTable should lists that were created with the readTable() function
#and returns a string, which is the class information assembled in the format 
#necessary for the assignment specification
def printClassInfo(classTable,subjectTable,classCode):
   for classInfo in classTable:
      if classInfo[0]==classCode:
         #We have found the matching classInfo. Now we fetch the subject name
         #from the subject table
         for subjectInfo in subjectTable:
            if subjectInfo[0]==classInfo[1]:
               subjectName = subjectInfo[1]
         #Assemble the string in the form: 
         #bw201 (Baskets throughout History), Mon 11.30, in 2.6.10      
         print classInfo[1]+" ("+subjectName+"), "+classInfo[2]+", in "+classInfo[3]
         

#Initialising envvalid to True. Will later be changed to false if the directory
#specified by os.environ['ENROLDIR'] does not contain all of the valid data
#files.
envvalid=True
os.environ['ENROLDIR']="./"   
#If the environment variable ENROLDIR exists   
if(os.environ.get('ENROLDIR')!=None):
   enroldir = os.environ.get('ENROLDIR')
   roll = {}
   try:
      subjectsTable = readtable(os.path.join(enroldir,"SUBJECTS"))
      classesTable = readtable(os.path.join(enroldir,"CLASSES"))
      for classInfo in classesTable:
         rollFileName=classInfo[0]+".roll"
         roll[classInfo[0]]=readEnrolFile(os.path.join(enroldir,rollFileName))
         
   except IOError:
      print "Error opening file in environment variable directory. Will now" 
      print "attempt default data directory instead."  
      envvalid=False

#Check if environment variable is undefined or invalid. In which case we will
#use the default data directory in the current subdirectory instead      
if(os.environ.get('ENROLDIR')==None or envvalid==False):
   enroldir="./data/"
   try:
      subjectsTable = readtable(os.path.join(enroldir,"SUBJECTS"))
      classesTable = readtable(os.path.join(enroldir,"CLASSES"))
      for classInfo in classesTable:
         rollFileName=classInfo[0]+".roll"
         roll[classInfo[0]]=readEnrolFile(os.path.join(enroldir,rollFileName))
   except IOError:
      sys.exit("Could not load data because both data directories are invalid. This program will now exit.")
   
if(len(sys.argv)==1):
   print "Subjects are:"
   for subjectInfo in subjectsTable:
      numClasses=0
      numStudents=0
      for classLine in classesTable:
         #If this particular class is for the subject in question, that means 
         #we should add 1 to the number of classes for that subject. Then
         #we count all the students in the relevant roll data for that class
         #and add it to the number of students tally for this subject
         if classLine[1]==subjectInfo[0]:
            numClasses+=1
            for student in roll[classLine[0]]:
               numStudents+=1
         
      
      print subjectInfo[0]+"\t"+subjectInfo[1]+"\tclasses: "+str(numClasses)+" students: "+str(numStudents)
#Arguments (besides script name) were entered. 
else:
   #Check arguments are right format e.g. ./statistics --student 1123445
   if(sys.argv[1]!="--student"):
      sys.exit("Incorrect arguments. Correct usage is --student <studentNo> or no arguments ")
   
   for classCode, studentList in roll.iteritems():
      for studentID in studentList:
         if (studentID==sys.argv[2]):
            #The student is enroled in the class with code "classCode" so now
            #we should print the class information for that class
            printClassInfo(classesTable, subjectsTable, classCode)
            

#print os.environ['ENROLDIR']