#!/usr/bin/env python

import tempfile
import os
import shutil

def readlines(filename):
   fp=open(filename)
   mylinelist = []
   for line in fp:
      if not line.startswith("#"):
         mylinelist.append(line.rstrip("\n"))
   fp.close()
   return mylinelist  

def readtable(filename):
   fp=open(filename)
   mytable = []
   for line in fp:
      if not line.startswith("#"):
         mytable.append(line.rstrip("\n").split(":"))
   fp.close()
   return mytable
   
def writelines(filename, lines):
   #tempfp = tempfile.NamedTemporaryFile(dir=".", delete=False)
   tempfp=open("temp.txt","w")
   for line in lines:
      tempfp.write(line)
   if os.path.exists(filename):
      os.remove(filename)
   print tempfp
   os.rename(tempfp.name,filename)
   tempfp.close()
   return 1
   
class Enrol:
   def __init__(self, dirname):
      print os.path.join(dirname, "SUBJECTS")
      self.dirname=dirname
      self.subjectTable = readtable(os.path.join(dirname, "SUBJECTS"))
      self.classTable = readtable(os.path.join(dirname, "CLASSES"))
      self.rollTable = []
      self.classRoll = []
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
         
   def subjects(self):
      self.subjectcodes=[]
      for line in self.subjectTable:
         self.subjectcodes.append(line[0])
      return self.subjectcodes
      
   def subjectName(self, subjectCode):
      for line in self.subjectTable:
         if line[0]==subjectCode:
            return line[1]
      return None
      
   def classes(self, subjectCode):    
      self.classIds=[]
      for line in self.classTable:
         if line[1]==subjectCode:
            self.classIds.append(line[0])
      #If no matching subject exists
      if len(self.classIds)==0:
         raise KeyError("No matching subject")
      return self.classIds   
   
   def classInfo(self, classId):
      classinfo=()
      for line in self.classTable:
         if line[0]==classId:
            self.studentsInClass=readtable(os.path.join(self.dirname, line[0]+".roll"))
            classinfo=(line[1],line[2],line[3],line[4],self.studentsInClass)
      return classinfo   
   
   def checkStudent(self, studentID, *args):   
      self.enrolledClasses=[]
      if len(args) > 1:
         sys.exit("Wrong number of arguments for checkStudent function")
      #If function has been called with the optional subject code argument
      if len(args) == 1:
         #Search through all the subjects. For each class for that subject,
         #check if the student is enrolled in that class
         for line in self.classTable:
            if line[1] == args[0]:
               for classX in self.rollTable:
                  #Check if the class code of the enroled students list is
                  #the same as the class code for a matching subject
                  if classX[0]==line[0]:
                     for student in classX:
                        if student==studentID:
                           return classX[0]
         return None              
      #If function has been called without the optional subject code argument   
      else:
         print "Function was called without optional subject code argument"
         for classList in self.rollTable:
            for line in classList:
               #If the student is in the list of enrolled students for this
               # class list
               if line==studentID:
                  # Only add the class name to the list if it hasn't
                  # already been added. No duplicates.
                  if classList[0] not in self.enrolledClasses:
                     self.enrolledClasses.append(classList[0])
         return self.enrolledClasses  

   def enrolStudent(self, studentID, classCode):
      self.numStudents = 0
      self.classExists = False
      
      #Setting the number of students enroled in the classCode
      for line in self.classTable:
         #Check if there is a matching class in the class list
         if line[0]==classCode:
            self.classExists=True
            self.matchingClassLine = line
            for roll in self.rollTable:
               if roll[0]==classCode:
                  self.matchingRoll=roll
                  for student in roll:
                     self.numStudents+=1
            
      for line in self.venueTable:
         if self.matchingClassLine[3]==line[0]:
            if self.numStudents>=line[1]:
               return None
      
      
      #Need to do the remove student part here...
      
      #No matching classes
      if not self.classExists:
       raise KeyError("No matching class") 
      #Add student to class
      self.matchingRoll.append(studentID)
      #Open the matching roll file
      fp = open(os.path.join(self.dirname, self.matchingRoll[0]+".roll"),"a")
      fp.write(studentID+"\n")
      return 1
      
      
        
   

         
enrolobject = Enrol(".")

# print enrolobject.subjects()
# print enrolobject.subjectName('bw110')
# print enrolobject.classes('bw101')
# print enrolobject.classInfo('bw101.1')   
# print enrolobject.checkStudent('1109202','bw101')
print enrolobject.enrolStudent('s5','bw101.1')

# print enrolobject.checkStudent("s1")
# print enrolobject.rollTable
   
# x=readlines("SUBJECTS")
# print x

# y = readtable("SUBJECTS")
# print y

# z=['test1','test2']
# writelines("winning.txt",z)