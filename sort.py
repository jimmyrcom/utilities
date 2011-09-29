# By Jimmy Ruska
# Sorts Desktop and Downloads folder by extension.
# Made for easy modification. Tested: Windows/Ubuntu Python 2.7, 3.2.
# Beware, it will also move folders and program Shortcuts.

import ConfigParser
import platform
import os
import re

_organize = dict()
# conditions where sorting is avoided
_ignore = list()

def read_config():
    """ Get config data from cfg file.
    """
    config = ConfigParser.ConfigParser()
    config.read('sort.cfg')
    organize_dict = dict()
    for k, v in config.items('organize'):
        organize_dict[k] = v
    ignore_list = list()
    for k, v in config.items('ignore'):
        for item in v.split(','):
            token = (k, item)
            ignore_list.append(token)
    return organize_dict, ignore_list

def main():
    # Set which folder things get sorted into
    OS=(platform.uname())[0]
    if   OS=="Windows":
        final=os.path.join(os.environ['USERPROFILE'],"My Documents/Downloads/")
    else:
        final=os.path.join(os.environ.get("HOME"),"Downloads/")

    # Split all file extensions into lists of strings 'foo,bar' -> ['foo','bar']
    for key,val in _organize.items():
        _organize[key]=val.strip().replace(' ','').split(",")

    if not os.path.isdir(final):
        os.mkdir(final)

    # Put which folders you want sorted. will ignore if doesn't exist
    sortTheseFolders = [final, final+"../../Desktop/", final+"../Desktop/"]
    sort(sortTheseFolders, final)

# sort list of dirs into folder final
def sort(dirs,final): 
    # make base directories if they don't exist
    for key in _organize:
        if not os.path.isdir(final+key):
            os.makedirs(final+key)
    #loop through and sort all directories
    for path,file in sum([[(d,z) for z in os.listdir(d)] for d in dirs if os.path.exists(d)],[]):        
        if file in _organize or exclude(file):
            pass
        elif os.path.isdir(path+file) and not os.path.exists(final+"dir/"+file):
            os.rename(path+file, final+"dir/"+file)
        else: 
            to=final+grouping(file.rpartition(".")[2].lower())+file
            if not os.path.exists(to):
                os.rename(path+file,to)

# Don't sort certain files like desktop.ini
def exclude(name):
    for op,check in _ignore:
        if ((op=="re" and re.match(check,name))
            or (op=="match" and re.search(check,name))
            or (op=="exact" and check==name)):
                 return True

# Match file extensions to find group
def grouping(ext):
    for folder,exts in _organize.items():
        if ext in exts:
            return folder+"/"
    return "other/"

if __name__ == '__main__':

    _organize, _ignore = read_config()
    
    #main()
