import os

working_dir = os.getcwd()
file_path = os.path.join(working_dir, input('Please enter relative path to file.\n'))

dirname = os.path.dirname(__file__)
zones_path = os.path.join(dirname, 'zones')

#create absolute path to file.txt
os.path.join(os.path.abspath(os.path.dirname(__file__)), 'file.txt')