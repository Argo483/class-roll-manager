#! /usr/bin/env python2.6

import tempfile
import os
import shutil

"""
This module contains functions for processing files related to a education
management system. It also contains the definition of a class Enrol and
it's functions, which are used to store and manage data for the education
management system.
"""

def readlines(filename):
   """
   Returns a list of strings, with each string being a line in the file 
   designated by the parameter filename. Lines in the file which start
   with a "#" are ignored. New lines characters are stripped at the end of 
   each line.
   """
   fp=open(filename)
   mylinelist = []
   for line in fp:
      if not line.startswith("#"):
         mylinelist.append(line.rstrip("\n"))
   fp.close()
   return mylinelist  

def readtable(filename):
   """
   Opens the file designated by filename. Lines in the file which start with
   "#" are ignored. Lines are stripped of their new line characters at the
   end of each line. Lines are split into a list based on ":".Function then
   returns a list of lists, each element in the parent list is itself a list
   in which each element is a part of the line in the textfile.
   """
   fp=open(filename)
   mytable = []
   for line in fp:
      if not line.startswith("#"):
         mytable.append(line.rstrip("\n").split(":"))
   fp.close()
   return mytable
   
def writelines(filename, lines):
   """
   Writes lines to a temporary file. Then deletes filename if it exists, and
   renames the tempfile to filename. Returns 1 if successful. 
   """
   tempfp = tempfile.NamedTemporaryFile(dir=".", delete=False)
   for line in lines:
      tempfp.write(line+"\n")
   if os.path.exists(filename):
      os.remove(filename)   
   os.rename(tempfp.name,filename)
   tempfp.close()
   return 1
   
def readEnrolFile(rollFilename):
   """
   Reads a .roll file and returns a list of students in that roll file. Lines
   starting with # are ignored. Lines are stripped of their new line characters
   at the end of each line. If a roll file doesn't exist, returns an empty list.
   """
   studentList=[]
   try:
      roll = open(rollFilename,'rw+')
   except IOError:
      #If the roll file does not exist for that class, I assume that there
      #are 0 students for that class, so I return the empty studentList
      roll.close()
      return studentList
   #Append each student number in the roll file to the student list
   for student in roll:
      if not student.startswith("#"):
         studentList.append(student.rstrip("\n"))
   roll.close()      
   return studentList       
   
class Enrol:
   """
   This class  encapsulates the education management system. 
   When the enrol object is created, it will read its data from the directory 
   whose name is given to it. When the program using Enrol calls its methods 
   to retrieve data, it will retrieve the information from its in-memory data 
   structures. When the user calls methods to change data (i.e., to add students 
   to classes), it will change both its data structures and the files on the disk.
   """
   def __init__(self, dirname):
      self.dirname=dirname
      self.subjectTable = readtable(os.path.join(dirname, "SUBJECTS"))
      self.classTable = readtable(os.path.join(dirname, "CLASSES"))
      self.rollTable = []
      self.classRoll = []
      self.roll={}
      self.venueTable=readtable(os.path.join(dirname, "VENUES"))
      # This for loop initialises the rollTable. Roll table is a list of lists.
      # Each list inside rollTable contains the class name of that roll (e.g.
      # bw101.2) as the first element. Each subsequent element of that list
      # will be a student number
      for line in self.classTable:
         #Set first element as the class name
         self.classRoll.append(line[0])
         # Append each student number to the class roll
         for line in readtable(os.path.join(dirname, line[0]+".roll")):
            self.classRoll.append(line[0])
         # Adding the list of students for this class to the rollTable
         self.rollTable.append(self.classRoll)   
         
      for classInfo in self.classTable:
         rollFileName=classInfo[0]+".roll"
         self.roll[classInfo[0]]=readEnrolFile(os.path.join(dirname,rollFileName))   
         
   def subjects(self):
      """
      Returns a list of subject codes handled by the enrolment system. 
      Accepts no arguments.
      """
      self.subjectcodes=[]
      for subjectInfo in self.subjectTable:
         self.subjectcodes.append(subjectInfo[0])
      return self.subjectcodes
      
   def subjectName(self, subjectCode):
      """
      Accepts one argument: a subject code. Returns the name of the subject with 
      that code, or None if no subject matches.
      """
      for subjectInfo in self.subjectTable:
         if subjectInfo[0]==subjectCode:
            return subjectInfo[1]
      return None
      
   def classes(self, subjectCode):  
      """
      Returns a list of class IDs for a particular subject. Accepts one 
      argument: the subject code of a subject. Raise KeyError if the 
      subject does not exist.
      """
      classIds=[]
      for classInfo in self.classTable:
         if classInfo[1]==subjectCode:
            classIds.append(classInfo[0])
      #If no matching subject exists raise a key error
      if len(classIds)==0:
         raise KeyError("No matching subject")
      return classIds   
   
   def classInfo(self, classId):
      """
      Returns information about a class. Accepts one argument: a string 
      containing the class ID. Returns a tuple of the form (subjcode, 
      time, room, tutor, students). The first four elements are strings, 
      and contain the information as described in the CLASSES file specification 
      above. The last item is a list of the student IDs enrolled in the class. 
      Raise KeyError if the class does not exist.
      """
      classinfo=()
      for line in self.classTable:
         if line[0]==classId:
            classinfo=(line[1],line[2],line[3],line[4],self.roll[classId])
            return classinfo
      raise KeyError("Class does not exist")
   
   def checkStudent(self, studentID, *args):   
      """
      Checks which classes a student is enrolled in. Accepts one or two arguments. 
      The first (required) argument is the student ID to check. The second (optional) 
      argument is an optional subject code. If a subject code is specified, returns 
      the class code of the class in which the student is enrolled for that subject; 
      if the student isn't enrolled in any class in that subject, it returns None. If 
      no subject code is specified, it returns a list of zero or more class codes the 
      student is enrolled in across all possible subjects.
      """
      self.enrolledClasses=[]
      if len(args) > 1:
         raise ValueError("Incorrect number of arguments supplied")
      #If function has been called with the optional subject code argument
      if len(args) == 1:
         #Search through all the subjects. For each class for that subject,
         #check if the student is enrolled in that class
         for classInfo in self.classTable:
            #If the class is the one specified in the optional argument
            if classInfo[1] == args[0]:
               #For each student in a matching roll
               for student in self.roll[classInfo[0]]:
                  #If the student enroled in the class, return the class ID
                  if student==studentID:
                     return classInfo[0]
         return None              
      #If function has been called without the optional subject code argument   
      else:
         for classCode, studentList in self.roll.iteritems():
            for studentData in studentList:
               if studentData==studentID:
                  self.enrolledClasses.append(classCode)
         return self.enrolledClasses  

   def enrol(self, studentID, classCode):
      """
      Attempts to enrol a student in a class. Accepts two arguments: a 
      student ID and a class code. It returns 1 if successful, None if not. 
      Before attempting to enrol a student in a class, it attempts to check 
      whether the number of students in the class is less than the capacity 
      of the class's venue. If not, then there is no space in the class and 
      it fails. If there is space, it proceeds. If the student is enrolled in
      any other classes in the same subject as the class, she is removed from 
      those classes and placed in the new one. Raise KeyError if the class 
      does not exist.
      """
      numStudents = 0
      classExists = False
      #This for loop sets the number of students enroled in the classCode
      for classInfo in self.classTable:
         #Check if there is a matching class in the class list
         if classInfo[0]==classCode:
            classExists=True
            matchingSubjectCode=classInfo[1]
            matchingClassLine = classInfo
            for classID, studentList in self.roll.iteritems():
               if classID==classCode:
                  matchingRoll=studentList
                  matchingClassId=classID
                  for student in studentList:
                     numStudents+=1
      #No matching classes
      if not classExists:
         raise KeyError("No matching class") 
      #Check the number of currently enroled students against the maximum venue
      #size and return None if there is not enough room in the venue for another student
      for venueInfo in self.venueTable:
         if matchingClassLine[3]==venueInfo[0]:
            if numStudents>=venueInfo[1]:
               return None
      
      #Search through the roll dictionary for classes with the subject code 
      #of the subject we are enroling the student in. If a matching class is
      #found, and the student is enroled in that class, then remove that student 
      #from memory, and then remove that student from the data file by writing the 
      #modified student list back to the data file.
      for classID, studentList in self.roll.iteritems():
         for classInfo in self.classTable:
            if classInfo[0]==classID and classInfo[1]==matchingSubjectCode:
               for student in studentList:
                  if student==studentID:
                     studentList.remove(student)
                     writelines(os.path.join(self.dirname, classID+".roll"),studentList)   
         
      #Add student to class
      matchingRoll.append(studentID)
      #Open the matching roll file
      fp = open(os.path.join(self.dirname, matchingClassId+".roll"),"a")
      fp.write(studentID+"\n")
      return 1