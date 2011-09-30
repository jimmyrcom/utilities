# By Jimmy Ruska
# Sorts Desktop and Downloads folder by extension.
# Made for easy modification. Tested: Windows/Ubuntu Python 2.7, 3.2.
# Beware, it will also move folders and program Shortcuts.

import ConfigParser
import os
import re

cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sort.cfg')
_organize = dict()
# conditions where sorting is avoided
_ignore = list()

def read_config():
    """ Get config data from cfg file.
    """
    config = ConfigParser.ConfigParser()    
    config.read(cfg_path)
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
    config = ConfigParser.ConfigParser()
    config.read(cfg_path)
    final = config.get('dirs', 'sorted')    
    # Split all file extensions into lists of strings 'foo,bar' -> ['foo','bar']
    for key,val in _organize.items():
        _organize[key]=val.strip().replace(' ','').split(",")

    if not os.path.isdir(final):
        os.mkdir(final)

    # Put which folders you want sorted. will ignore if doesn't exist
    sortTheseFolders = [os.path.abspath(os.path.join(final, p)) 
                        for p in config.get('dirs', 'toreview').split(',')
                        if os.path.exists(os.path.abspath(os.path.join(final, p)))]
    sort(sortTheseFolders, final)

# sort list of dirs into folder final
def sort(dirs,final): 
    # make base directories if they don't exist
    for key in _organize:
        path = os.path.join(final, key)
        if not os.path.isdir(path):
            os.makedirs(path)

    #loop through and sort all directories
    for path,file in sum([[(d,z) for z in os.listdir(d)] for d in dirs],[]):        
        target = os.path.join(path, file)
        if file in _organize or exclude(file):
            pass
        elif os.path.isdir(target) and not os.path.exists(final+"dir/"+file):
            os.rename(target, final+"dir/"+file)
        else: 
            to = os.path.join(final, grouping(file.rpartition(".")[2].lower())+file)
            if not os.path.exists(to):
                os.rename(target, to)

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
    
    main()
