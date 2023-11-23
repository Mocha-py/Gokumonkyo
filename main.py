from os import getcwd, system, listdir, remove
import curses
from sys import exit
from cryptography.fernet import Fernet
from time import sleep

#get directory of where the program is currently located
CURRENT_DIRECTORY = getcwd()

def check_certainty(stdscr=object, action=str, files_selected=list):
    '''
    Function to check if the user is certain that they want to
    perform the selected action to the valid files found.
    :param stdscr: curses virtual window (obj).
    :param action: The selected action, always either 'encrypt' or 'decrypt' (str).
    :param files_selected: The files to be acted on (list).
    :return: Returns True if user inputs yes and False if no (bool).
    '''
    #horizontal location of the selected option to place the X marker
    x_location = 2
    #do until broken:
    while True:
        #clear the curses window
        stdscr.clear()
        #ask the user if they would like to perform the action in the parameters
        stdscr.addstr(1,1,f'Would you like to {action} these files?:')
        #for the number of files
        for num in range(len(files_selected)):
            #add a row showing each file
            stdscr.addstr(num+2,3,files_selected[num])
            #if the current iteration is for the last file
            if num == len(files_selected)-1:
                #show options
                stdscr.addstr(num+3,1,'''[ ]            [ ]\n YES            NO''')
                #adds selection marker
                stdscr.addstr(num+3,x_location,'X')
        #get input from the user
        key = stdscr.getkey() 
        #start matching key
        match key:
            #if the user presses left or right
            case key if key in ["KEY_LEFT", "KEY_RIGHT"]:
                #if left option is selected
                if x_location == 2:
                    #set option to right option
                    x_location=17
                #otherwise the right option must be selected
                else:
                    #so set the option to the left option
                    x_location=2
            #if the user presses space
            case " ":
                break
    #if the option was the left
    if x_location == 2:
        #return True (yes)
        return True
    #if option was the right
    elif x_location == 17:
        #return False (no)
        return False

            

def encrypt(directory=str, files=list, key=bytes):
    '''
    Function to encrypt the files in the parameters using
    the key also in the parameters.
    :param directory: The directory where the files were located in (str).
    :param files: List of files in the files directory (list).
    :param key: The key to be used to encrypt the files (bytes).
    '''
    #for each file to encrypt
    for item in files:
        #open the files binary with read permissions
        with open(directory+'/files/'+item,'rb') as file:
            #collect all the binary contents
            original_contents = file.read()
        #open a new file to add the encrypted contents to
        with open(directory+'/files/'+item+'.gkmk','wb') as file:
            #encrypt the contents with the key
            file.write(Fernet(key).encrypt(original_contents))
        #delete old file
        remove(directory+'/files/'+item)

def decrypt(directory=str, files=list, key=bytes):
    '''
    Function to decrypt the files in the parameters using
    the key also in the parameters.
    :param directory: The directory where the files were located in (str).
    :param files: Cleaned list of files in the files directory (list).
    :param key: The key to decrypt the files with (bytes).
    '''
    #for each file to decrypt
    for item in files:
        #open the files binary with read permissions
        with open(directory+'/files/'+item,'rb') as file:
            #collect all the binary contents
            original_contents = file.read()
        with open(directory+'/files/'+item.removesuffix('.gkmk'), 'wb') as file:
            #decrypt the contents with the key
            file.write(Fernet(key).decrypt(original_contents))
        #delete old file
        remove(directory+'/files/'+item)

def get_key(directory=str):
    '''
    Function to attempt to find the key file in the key folder.
    :param directory: The directory to search for the key in (str).
    :return: Returns the key (bytes) if it is found, otherwise returns False (bool).
    '''
    #clear the CLI
    system('cls')
    #attempt to:
    try:
        #open the key file with read permissions
        with open(directory+'/key/gkmk_key.txt', 'r') as key_file:
            #get the first line, strip any spaces and encode it to bytes
            key = bytes(key_file.readlines()[0].strip(), 'utf-8')
    #if this fails:
    except:
        #tell user key was not detected
        print('ERR: NO KEY FILE DETECTED, RETURNING TO MENU IN 3 SECONDS.\n')
        #wait 3 seconds
        sleep(3)
        #return False to show that function failed
        return False
    #otherwise if it works:
    else:
        #return the key found
        return key
    
def get_files_for_key(directory=str, key=bytes, files=list):
    '''
    Function to get the files that are encrypted with the
    current key and clean the files list so that only files
    encrypted with the current key will be decrypted.
    :param directory: The directory where the key can be found (str).
    :param key: The current key being used (bytes).
    :param files: The list of files to clean (list).
    :return: Returns the cleaned files (list).
    '''
    #clear the CLI
    system('cls')
    #open the key file with read permissions
    with open(directory+'/key/gkmk_key.txt', 'r') as key_file:
        #get contents of the file and store them
        contents = key_file.readlines()
        #if the first line casted to bytes is not the key
        if bytes(contents[0].strip(), 'utf-8') != key:
            #return False to show function failed
            return False
        #remove the first line from the contents variable
        contents.pop(0)
        #for every file listed in the files param
        for item in files:
            #if the file is not in the contents text file
            if item not in contents:
                #remove the file from the list of files
                files.remove(item)
    #return the cleaned list of files
    return files

def generate_key_file(directory=str, files=list):
    '''
    This function generates the key and stores it in a file, along with
    the names of the files that were encrypted. Returns the key.
    :param directory: The directory to create the key file in.
    :param files: list of files in the files directory (list).
    :return: Returns the generated key (bytes).
    '''
    #generate a key
    key = Fernet.generate_key()
    #cast key to a string and remove the b'' around the key, then add this to a variable
    to_write = str(key).split("'")[1]
    #for each file in the parameters: 
    for item in files:
        #add the files name with the .gkmk extension on the next line of the variable
        to_write+=f'\n{str(item)}.gkmk'
    #open the key file or create a new one if it does not exist with write permissions
    with open(directory+'/key/gkmk_key.txt', 'w') as key_file:
        #write the contents of the variable
        key_file.write(to_write)
    #return the generated key
    return key

def get_files(directory=str):
    '''
    This function returns all the files in the "files"
    folder ready to be encrypted or decrypted by the program.
    :param directory: The directory to search for files in (str).
    :return: Returns all files found in the directory (list).
    '''
    #create an empty variable for files found in the directory
    found_files = []
    #for each file in the directory
    for file in listdir(directory+'/files/'):
        #add file to the list of files found
        found_files.append(file)
    #return the files found
    return found_files

def main_menu(stdscr=object):
    '''
    This is the main menu for the program, where the user 
    can input the function they would like to use.
    :param stdscr: curses virtual window (obj).
    '''
    #set the y location of the option marker to the first option
    y_location = 6
    #do until broken:
    while True:
        #intialise curses window
        curses.initscr()
        #clear the curses window
        stdscr.clear()
        #add the title screen
        stdscr.addstr(0,1,""" _____     _                     _       ===    
 |   __|___| |_ _ _ _____ ___ ___| |_ _ _ ___ 
 |  |  | . | '_| | |     | . |   | '_| | | . |
 |_____|___|_,_|___|_|_|_|___|_|_|_,_|_  |___|
                                     |___|
 ---------------------------------------------
 [ ] Encrypt Files

 [ ] Decrypt Files

 [ ] Exit""")
        #add the option marker at the y location of the currently selected option
        stdscr.addstr(y_location,2,'X')
        #refresh the curses window to update display
        stdscr.refresh()
        #get key input from the user
        key_input = stdscr.getkey()
        #start matching key
        match key_input:
            #if the key pressed was up arrow:
            case "KEY_UP":
                #if the current option is already the top option
                if y_location == 6:
                    #set y location to that of the bottom option
                    y_location=10
                #otherwise:
                else:
                    #change y location to that of the option above
                    y_location-=2
            #if the key pressed was down arrow
            case "KEY_DOWN":
                #if the current option is already the bottom option 
                if y_location == 10:
                    #set y location to that of the top option
                    y_location=6
                #otherwise:
                else:
                    #change y location to that of the option above
                    y_location+=2
            #if the key pressed was space
            case " ":
                #end the curses window
                curses.endwin()
                #start matching the y location of the marker
                match y_location:
                    #if the option was the first (encrypt)
                    case 6:
                        #get the files from the current directory
                        files = get_files(CURRENT_DIRECTORY)
                        #for each of these files
                        for file in files:
                            #if the file is already encrypted
                            if file.endswith('.gkmk'):
                                #remove it from the files to be encrypted
                                files.remove(file)
                        #if no files are detected
                        if len(files) == 0:
                            #inform the user of the error
                            print('ERR: NO FILES DETECTED, RETURNING IN 3 SECONDS.')
                            #wait 3 seconds
                            sleep(3)
                            #start again
                            continue
                        #check if the user is sure they want to perform this action
                        certainty = check_certainty(stdscr, action='encrypt',files_selected=files)
                        #if the user is certain:
                        if certainty == True:
                            #generate a key in the current directory for the current files
                            key = generate_key_file(CURRENT_DIRECTORY, files)
                            #encrypt the files in the current directory with the generated key
                            encrypt(CURRENT_DIRECTORY, files, key)
                            #inform the user that the encryption was successful
                            print('ENCRYPTION SUCCESSFUL. RETURNING TO MENU IN 3 SECONDS.')
                            #wait 3 seconds
                            sleep(3)
                        #start again
                        continue
                    #if option was the second (decrypt)
                    case 8:
                        #get the key from the current directory
                        key = get_key(CURRENT_DIRECTORY)
                        #if this fails:
                        if key == False:
                            #start again
                            continue
                        #get a cleaned list of files from the current directory using the key
                        files = get_files_for_key(CURRENT_DIRECTORY, key, \
                        get_files(CURRENT_DIRECTORY))
                        #if this failed:
                        if files == False:
                            #inform the user of the error
                            print('ERR: KEY HAS BEEN CHANGED, RETURNING IN 3 SECONDS.')
                            #wait 3 seconds
                            sleep(3)
                            #start again
                            continue
                        #if no files are found:
                        if len(files) == 0:
                            #inform the user of this error
                            print('ERR: NO FILES DETECTED, RETURNING IN 3 SECONDS.')
                            #wait 3 seconds
                            sleep(3)
                            #start again
                            continue
                        #check if the user is sure they want to perform this action
                        certainty = check_certainty(stdscr,action='decrypt',files_selected=files)
                        #if the user is certain:
                        if certainty == True:
                            #decrypt the files in the current directory with the key
                            decrypt(CURRENT_DIRECTORY, files, key)
                            #inform the user that the decryption was successful
                            print('DECRYPTION SUCCESSFUL. RETURNING TO MENU IN 3 SECONDS.')
                            #wait 3 seconds
                            sleep(3)
                        #start again
                        continue
                    #if option was the third (exit)
                    case 10:
                        #clear the CLI
                        system('cls')
                        #exit the program
                        exit()

#if this script is not being ran as a module
if __name__ == "__main__":
    #clear the CLI
    system('cls')
    #run the menu
    curses.wrapper(main_menu)