'''
Created on 29/09/2011

@author: dave
'''
import ConfigParser
import datetime
import os
import shutil

import sort as u_sort

class TestSort(object):

    def setup(self):
        """ setup some dirs and files for testing
        """
        
        config = ConfigParser.ConfigParser()
        config.read("../sort.cfg")
        self.organize, self.ignore = u_sort.read_config()  
        self.toreview = ['source1', 'source2',]        
        self.sorted = "sorted"
        self.build_test_data()
        u_sort._organize = self.organize
        u_sort._ignore = self.ignore
        
    def build_test_data(self):
        os.mkdir(self.sorted)
        step = 0
        for d in self.toreview:
            os.mkdir(d)
            stamp = datetime.datetime.now().strftime('%Y%m%d%H%M%s')
            for _, v in self.organize.items():
                for ext in v.split(','):
                    path = os.path.join(d, "%s_%04d.%s" % (stamp, step, ext))
                    with open(path, 'w') as fh:
                        fh.write(path)
                    step += 1
            for op, pats in self.ignore:
                for pat in pats.split(','):
                    if op == 'exact':
                        path = os.path.join(d, pat)
                        with open(path, 'w') as fh:
                            fh.write(path)
                    elif op == 'match':
                        fn = "_".join([stamp, pat, "%04d" % (step,)])
                        path = os.path.join(d, fn)
                        with open(path, 'w') as fh:
                            fh.write(path)
                        step += 1
                        fn = "_".join([stamp, "%04d" % (step,), pat])
                        path = os.path.join(d, fn)
                        with open(path, 'w') as fh:
                            fh.write(path)
                        step += 1
                        fn = "_".join([pat, stamp, "%04d" % (step,)])
                        path = os.path.join(d, fn)
                        with open(path, 'w') as fh:
                            fh.write(path)
                        step += 1

    def teardown(self):
        """ clean up the test dirs
        """
        for d in self.toreview:
            shutil.rmtree(d)
        shutil.rmtree(self.sorted)

    def test_sort(self):
        u_sort.sort(self.toreview, self.sorted)

if __name__ == "__main__":
    print "testing\n"
    
    ts = TestSort()
    ts.setup()
    ts.test_sort()
    ts.teardown()
    
    print "\n\ndone!"