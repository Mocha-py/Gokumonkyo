import unittest
from os import getcwd
import main
TESTING_DIRECTORY = getcwd()+'/testing/'

class TestGokumonkyō(unittest.TestCase):
    def test_getting_files(self):
        '''
        Subroutine to test the get_files function.
        :Test 1: Detecting one text file.
        :Test 2: Detecting multiple files of different types.
        '''
        print('Testing getting files...\n')
        self.assertEqual(main.get_files(TESTING_DIRECTORY+'test1'), ['file.txt'])
        print("Test 1 completed.\n")
        self.assertEqual(main.get_files(TESTING_DIRECTORY+'test2'), ['file.bat','file.py','file.txt'])
        print("Test 2 completed.\n")
        print('Getting files tests finished.\n')
    def test_getting_keys(self):
        '''
        Subroutine to test the get_key function.
        :Test 1: Testing getting a valid key from a text file.
        :Test 2: Testing to check if False is returned when no text file is detected.
        '''
        print('Testing getting keys...\n')
        self.assertEqual(main.get_key(TESTING_DIRECTORY+'test1'), \
        bytes('V3vVohYr9gzeGU9P_2OdJ2caiKeCSGMU2EPilB3ye34=', 'utf-8'))
        print('Test 1 completed.\n')
        self.assertEqual(main.get_key(TESTING_DIRECTORY+'test2'), False)
        print('Test 2 completed.\n')
        print('Getting keys tests finished.\n')
    def test_get_files_for_key(self):
        '''
        Subroutine to test get_files_for_key function.
        :Test 1: Testing cleaning files.
        :Test 2: Testing checking a changed key returns False (files located
        in test 3 because test 2 for other tests requires an empty key folder).
        '''
        print('Testing getting valid files from key file...')
        self.assertEqual(main.get_files_for_key(TESTING_DIRECTORY+'test1', \
        bytes('V3vVohYr9gzeGU9P_2OdJ2caiKeCSGMU2EPilB3ye34=', 'utf-8'), ['file.txt','file.bat']), ['file.txt'])
        print('Test 1 completed.\n')
        self.assertEqual(main.get_files_for_key(TESTING_DIRECTORY+'test3', \
        bytes('V3vVohYr9gzeGU9P_2OdJ2caiKeCSGMU2EPilB3ye34=','utf-8'),['file.txt']),False)
if __name__ == '__main__':
    unittest.main()