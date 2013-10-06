#! /usr/bin/env python2.6

import os
import shutil
import unittest

import enrol

class TestEnrol(unittest.TestCase):
    def setUp(self):
        self.data = 'test-data'

        if os.path.exists(self.data):
            shutil.rmtree(self.data)

        os.mkdir(self.data)

        enrol.writelines(os.path.join(self.data, 'CLASSES'), [
            'bw101.1:bw101:Mon 9.30:2.5.10:Alice Chiswick',
            'bw101.2:bw101:Wed 14.30:2.6.1:Bob Turnham',
            'bw330A:bw330:Tue 15.30:23.5.32:Carlos Stamford'])

        enrol.writelines(os.path.join(self.data, 'SUBJECTS'), [
            'bw101:Introductory Basketweaving 1',
            'bw110:Introductory Basketweaving 2',
            'bw330:Underwater Basketweaving'])

        enrol.writelines(os.path.join(self.data, 'VENUES'),
                   ['2.5.10:18', '2.5.11:18', '2.6.1:22', '23.5.32:50'])

        enrol.writelines(os.path.join(self.data, 'bw101.1.roll'),
                   ['1124395', '1125622', '1109202', '1136607'])

        enrol.writelines(os.path.join(self.data, 'bw101.2.roll'),
                   [])

        enrol.writelines(os.path.join(self.data, 'bw330A.roll'),
                   ['1125622', '1136607'])

        self.e = enrol.Enrol(self.data)

    def tearDown(self):
        if os.path.exists(self.data):
            
            shutil.rmtree(self.data)
            

    def testSubjects(self):
        result = self.e.subjects()
        result.sort()
        self.assertEquals(result, ['bw101', 'bw110', 'bw330'])

    def testSubjectNameValid(self):
        self.assertEquals(self.e.subjectName('bw110'), "Introductory Basketweaving 2")

    def testSubjectNameInvalid(self):
        self.assertEquals(self.e.subjectName('Guam'), None)

    def testClassesValid(self):
        result = self.e.classes('bw101')
        result.sort()
        self.assertEqual(result, ['bw101.1', 'bw101.2'])

    def testClassesInvalid(self):
        self.assertRaises(KeyError, self.e.classes, 'Guam')

    # Add your own test cases below...

if __name__ == '__main__':
    unittest.main()
