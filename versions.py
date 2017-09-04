#!/usr/bin/env python

import subprocess
import importlib
import sys
import os
import json

def get_dist_info(mname):
    distpaths = [ x for x in sys.path if 'dist-packages' in x ]
    normalized_name = mname.replace('-','_')
    path = None
    for d in distpaths:
        for subdir in os.listdir(d):
            if subdir.startswith(normalized_name): 
                if subdir.endswith('dist-info'):
                    with open(d+"/"+subdir+"/metadata.json", 'r') as j:
                        return json.load(j)['version']
                elif subdir.endswith('egg-info'):
                    with open(d+"/"+subdir+"/PKG-INFO","r") as p:
                        version_lines = [ l for l in p.readlines() if l.startswith("Version") ] 
                        if version_lines:
                            return version_lines[0].replace("Version:","").strip()
    return "None"

    

def v(mname):
    try:
        m=importlib.import_module(mname)
    except ImportError:
        return "None"

    try: 
        return m.version.version
    except AttributeError:
        try: 
            return m.VERSION
        except AttributeError:
            try:
                return m.__version__
            except AttributeError:
                return "UNKNOWN"

print ("ENVIRONMENT:\n")
print ("Python:\t%s" % ".".join( [ str(x) for x in sys.version_info[:3] ]) ) 
try:
    print ("Java: %s" % subprocess.check_output("java -version", stderr=subprocess.STDOUT, shell=True).decode('utf-8').strip().split("\n")[0].replace("openjdk version","").replace('"','').strip() )
except subprocess.CalledProcessError:
    pass

print ("\nMODULES:\n")
modules = ('numpy','tensorflow','scipy','skimage',
		'mxnet', 'gym', 'cntk',
		'theano','lasagne',
        'pandas','keras','chainer','h5py','cv2','torch')
for mname in sorted(modules):
    print(":\t".join(['opencv' if mname=='cv2' else mname, v(mname)]))

print ("\nPACKAGES:\n")
packages = ('keras-rl','torchvision','ipython','tensorboard')
for pname in packages:
        print ("%s:\t%s" % (pname, get_dist_info(pname) ))

print ("\nTOOLS:\n")
print ("CAFFE: %s" % subprocess.check_output("caffe --version", shell=True).decode('utf-8').replace('caffe version','').strip() )
print ("Ipython: %s" % subprocess.check_output("ipython --version", shell=True).decode('utf-8').strip() )
print ("Jupyter: %s" % subprocess.check_output("jupyter --version", shell=True).decode('utf-8').strip() )
print ("Jupyter notebook: %s" % subprocess.check_output("jupyter notebook --version", shell=True).decode('utf-8').strip() )

# TODO: validate and test tensorflow/tensorboard
