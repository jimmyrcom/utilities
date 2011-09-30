# By Jimmy Ruska
# Sorts Desktop and Downloads folder by extension.
# Made for easy modification. Tested: Windows/Ubuntu Python 2.7, 3.2.
# Beware, it will also move folders and program Shortcuts.

import ConfigParser
import os
import re

cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sort.cfg')

class FileSorter(object):
    """ By Jimmy Ruska
    Sorts Desktop and Downloads folder by extension.
    Made for easy modification. Tested: Windows/Ubuntu Python 2.7, 3.2.
    Beware, it will also move folders and program Shortcuts.
    
    Refactor, cleanup, and tests by Dave Kujawski
    Note: changes only tested on Kubuntu.
    """
    def __init__(self):
        """ read the config file
        """
        config = ConfigParser.ConfigParser()
        config.read(cfg_path)
        self.organize = dict()
        for k, v in config.items('organize'):
            self.organize[k] = v.split('.')
        self.ignore = list()
        for k, v in config.items('ignore'):
            for item in v.split(','):
                token = (k, item)
                self.ignore.append(token)                
        self.dest = config.get('dirs', 'sorted')
        self.review_dirs = config.get('dirs', 'toreview').split(',')    

    # sort list of dirs into folder final
    def sort(self): 
        if not os.path.isdir(self.dest):
            os.mkdir(self.dest)

        # make base directories if they don't exist
        for key in self.organize:
            path = os.path.join(self.dest, key)
            if not os.path.isdir(path):
                os.makedirs(path)
    
        #loop through and sort all directories
        path_files = [[(d,z) for z in os.listdir(d)] for d in self.review_dirs]
        for path, file in sum(path_files,[]):        
            target = os.path.join(path, file)
            if file in self.organize or self._exclude(file):
                """ skip anything that we are supposed to ignore
                """
                pass
            elif os.path.isdir(target) \
            and not os.path.exists(os.path.join(self.dest, 'dir', file)):
                """ if the target is a directory, move the directory only if it
                has not already been moved.
                """
                # TODO: tests do not cover this yet!
                os.rename(target, os.path.join(self.dest, 'dir', file))
            else: 
                ext = file.rpartition(".")[2].lower()
                to = os.path.join(self.dest, self._grouping(ext), file)
                if not os.path.exists(to):
                    os.rename(target, to)

    # Don't sort certain files like desktop.ini
    def _exclude(self, name):
        for op,check in self.ignore:
            if ((op=="re" and re.match(check,name))
                or (op=="match" and re.search(check,name))
                or (op=="exact" and check==name)):
                    return True
    
    # Match file extensions to find group
    def _grouping(self, ext):
        for folder,exts in self.organize.items():
            if ext in exts:
                return folder
        return "other"

if __name__ == '__main__':    
    fs = FileSorter()
    fs.sort()
