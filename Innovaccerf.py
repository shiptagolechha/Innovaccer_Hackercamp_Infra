#!/usr/bin/python
import os    
import shutil
from os.path import splitext
import stat
import hashlib
import sys


filepaths = []
 # To find the largest files on the system if first option is chosen
def Largest_files(dirname,reverse=True): #reverse= True to sort in decreasing order of file size
    for dirName, subdirList, fileList in os.walk(dirname):    # recursively iterate through the directory structure
        for filename in fileList:
            filename = os.path.join(dirName, filename)
            if os.path.isfile(filename): # check if a file with the given path and name exists or not
                st = os.stat(filename)
                if(st.st_mode & stat.S_IRUSR): # check if the user has read permissions on the file or not
                    filepaths.append(filename)
    
    for i in range(len(filepaths)):
        filepaths[i] = (filepaths[i], os.path.getsize(filepaths[i])) # to get the size of all the files
    
    filepaths.sort(key=lambda filename: filename[1],reverse=reverse)  # sort the filenames according to the filesize(largest files first)
    
    return filepaths # return the filenames in dec order of their filesize


# To clean the given folder(moving similar types of files to same folder) if option 2 is chosen
def Clean_folder(drname):
    print("Enter the path of the folder where you want to move the fies to(destination folder):\n") # chose it to be Documents/ folder or any other according to your requirements 
    dest = input()
    print("\nFiles moved\n")
    for dirName, subdirList, fileList in os.walk(drname): # Recursively iterate through all the files in the directory structure
        for i,filename in enumerate(fileList):
            fn = filename
            filename = os.path.join(dirName, filename) #complete file path
            if os.path.isfile(filename): # check if the file with given path exists or not
                st = os.stat(filename)
                if((st.st_mode & stat.S_IWUSR) and (st.st_mode & stat.S_IRUSR)): # check if user has read and write permissions on the file or not
                    filepaths.append(filename)
                    file_name,extension = splitext(filename)  # split the filename to separate its extension 
                    if extension != '.lnk':  # If its a type of link file(shortcut) then dont move this file
                        print(file_name,extension)
                        s = dest
                        s = s + extension[1:] + '/'
                        os.makedirs(s, exist_ok=True) # creating a directory under the destination folder name naming the extension(type) of the file if such a directory already does not exist
                        shutil.move(filename,s) # move the file from the source location to the destination_folder/extension folder


# To find all the duplicate files if option 3 is chosen
def findduplicatefiles(dirname):
    
    duplicate_files = {}
    for dirName, subdirs, fileList in os.walk(dirname):  # recursively iterate through the directory structure
        print('\nSearching for duplicate files in " %s " Folder...' % dirName)
        for filename in fileList:
            filepaths = os.path.join(dirName, filename)
            filen = open(filepaths, 'rb')
            hash_val = hashlib.md5()  # for calculating the md5(message digest 5) algorihtm 
            blocksize = 65536
            data = filen.read(blocksize) # reading the file by dividing it into chunks/blocks of size 65536
            while len(data) > 0:
                hash_val.update(data)
                data = filen.read(blocksize)
            filen.close()
            file_hash= hash_val.hexdigest() # calculating hash value of the file by using hexdigest function that returns the  128 bits md5 hash value in hexadecimal form
           # if a file exists with the same md5 hash value then we have found a duplicate file of that file so enter the filepath of the file at the same key(hash value) or else create a new entry for that particular file   
            if file_hash in duplicate_files:
                duplicate_files[file_hash].append(filepaths)
            else:
                duplicate_files[file_hash] = [filepaths]
    
    return duplicate_files # return all the duplicate files found recursively in the folder 
 

#Printing the menu 
print("\n1. Find largest 10 files in a directory\n")
print("2. Clean a folder(Moving files of the same type to the same folder) \n")
print("3. Find all the duplicate files in a directory")
print("\nEnter your choice:\t")
#input the option according to what action is needed to be performed 
num = int(input())
print("\nEnter the complete path of the folder on which the operation is needed to be performed:\n")
drname = input() 

#option 1 chosen then perform
if num == 1:
    dirname = drname
    filepathss = []
    filepathss = Largest_files(dirname) # function returns the list of all files in the current folder sorted in dec order of their file size
    print("\nLargest 10 files in this directory are:\n")
    for i in range(10):   # print the largest 10 files along with their size in MBs
        print(filepathss[i][1] / float(1024 * 1024),"MB","   ",filepathss[i][0])

#option 2 chosen then perform
if num == 2:
    Clean_folder(drname) #function to clean the folder (generally the desktop folder)

#option 3 chosen then perform     
if num == 3:
    duplicate_files = {}
    dirname = [drname]
    for files in dirname: # iterate through all the files and subdirectories within this directory
        if os.path.exists(files): # if file exists
            duplicate_files1 = {}
            duplicate_files1 = duplicate_files
            duplicate_files2 = {}
            duplicate_files2 = findduplicatefiles(files)  # function returns dict of all the duplicate files

            # TO check if an entry for the file already exits int the hashtable or not
            for key in duplicate_files2.keys():
                if key in duplicate_files1: # entry exists append the filename to that particular key
                    duplicate_files1[key] = duplicate_files1[key] + duplicate_files2[key]
                else: # create a new key value pair
                    duplicate_files1[key] = duplicate_files2[key]
 
        else:
            print('%s is not a valid filepath/directorypath' % files) # if no such  file/ folder was present on the system with the given path
            sys.exit() # then exit

    duplicates = list(filter(lambda x: len(x) > 1, duplicate_files.values()))  # To check for files where there are more than one records for the same key value in the hashmap
    if len(duplicates) > 0: # if any duplicates found print them
        print('Duplicates Found:')
        print('\nThe following files contain the same content:\n')

        cnt = 0 
        for i,duplicates in enumerate(duplicates):
            print('\n\t********Duplicate files:%d*********\n' %(i+1) )
            for filenames in duplicates:
                sizeoffile = os.path.getsize(filenames) # to get size of the file
                sizeoffile = sizeoffile / 1024 # to convert into KBs
                print(sizeoffile,"KB   ",filenames)  #print filename along with its size in KBs
                print('\n')
                cnt = cnt + 1 # to count total number of duplicate files
        print("\nTotal duplicate files found in the given directory:%d\t" %cnt)    
    else:
        print('No duplicate files found in the given folder!')

    
