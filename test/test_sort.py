'''
Created on 29/09/2011

@author: dave
'''
import ConfigParser
import datetime
import os
import re
import shutil

import sort as u_sort

from nose.tools import assert_true

class TestSort(object):
    step = 0
    def setup(self):
        """ setup some dirs and files for testing
        """
        self.step += 1
        stamp = datetime.datetime.now().strftime('%Y%m%d%H%M%s%f')
        config = ConfigParser.ConfigParser()
        config.read("../sort.cfg")
        self.fs = u_sort.FileSorter()
        self.fs.review_dirs = ['/tmp/source1_%s_%d' % (stamp, self.step), 
                               '/tmp/source2_%s_%d' % (stamp, self.step),]        
        self.fs.dest = "/tmp/sorted_%s_%d" % (stamp, self.step)

        self.build_data()
        
    def build_data(self):
        os.mkdir(self.fs.dest)
        step = 0
        for d in self.fs.review_dirs:
            os.mkdir(d)
            stamp = datetime.datetime.now().strftime('%Y%m%d%H%M%s%f')
            for _, v in self.fs.organize.items():
                for ext in v:
                    path = os.path.join(d, "%s_%04d.%s" % (stamp, step, ext))
                    with open(path, 'w') as fh:
                        fh.write(path)
                    step += 1
            for op, pats in self.fs.ignore:
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
        for d in self.fs.review_dirs:
            shutil.rmtree(d)
        shutil.rmtree(self.fs.dest)

    def test_sort_dirs(self):        
        # do the sort
        self.fs.sort()
                
        for k in self.fs.organize:
            # make sure all dirs were created
            path = os.path.join(self.fs.dest, k)
            assert_true(os.path.isdir(path))

    def test_sort_files(self):        
        # do the sort
        self.fs.sort()
                
        for k, v in self.fs.organize.items():
            path = os.path.join(self.fs.dest, k)
            # check that the files are in the right place
            exts = [f.rpartition('.')[-1].lower() for f in os.listdir(path) 
                    if os.path.isfile(os.path.join(path,f))]
            expected = v
            for ext in exts:
                assert_true(ext in expected)
    
    def test_sort_ignores(self):        
        # do the sort
        self.fs.sort()
                
        # check that ignored files were left behind
        for source_dir in self.fs.review_dirs:
            files = [f for f in os.listdir(source_dir)
                     if os.path.isfile(os.path.join(source_dir, f))]
            for fn in files:
                assert_true(self.ok_to_ignore(fn))

    def ok_to_ignore(self, fn):
            for op, pats in self.fs.ignore:
                if op == 'exact':
                    if fn in pats.split(','):
                        return True
                if op == 'match':
                    for pat in pats.split(','):
                        if re.search(pat, fn):
                            return True
            return False

