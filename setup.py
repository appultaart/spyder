# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see spyderlib/__init__.py for details)

"""
Spyder
======

The Scientific PYthon Development EnviRonment
"""

from distutils.core import setup
from distutils.command.build import build
from sphinx import setup_command
import os, os.path as osp, sys


def get_package_data(name, extlist):
    """Return data files for package *name* with extensions in *extlist*"""
    flist = []
    # Workaround to replace os.path.relpath (not available until Python 2.6):
    offset = len(name)+len(os.pathsep)
    for dirpath, _dirnames, filenames in os.walk(name):
        for fname in filenames:
            if not fname.startswith('.') and osp.splitext(fname)[1] in extlist:
                flist.append(osp.join(dirpath, fname)[offset:])
    return flist

def get_subpackages(name):
    """Return subpackages of package *name*"""
    splist = []
    for dirpath, _dirnames, _filenames in os.walk(name):
        if osp.isfile(osp.join(dirpath, '__init__.py')):
            splist.append(".".join(dirpath.split(os.sep)))
    return splist

# Sphinx build (documentation)
class MyBuild(build):
    def has_doc(self):
        setup_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.isdir(os.path.join(setup_dir, 'doc'))
    sub_commands = build.sub_commands + [('build_doc', has_doc)]

class MyBuildDoc(setup_command.BuildDoc):
    def run(self):
        build = self.get_finalized_command('build')
        sys.path.insert(0, os.path.abspath(build.build_lib))
        dirname = self.distribution.get_command_obj('build').build_purelib
        self.builder_target_dir = osp.join(dirname, 'spyderlib', 'doc')
        try:
            setup_command.BuildDoc.run(self)
        except UnicodeDecodeError:
            print >>sys.stderr, "ERROR: unable to build documentation because Sphinx do not handle source path with non-ASCII characters. Please try to move the source package to another location (path with *only* ASCII characters)."        
        sys.path.pop(0)

cmdclass = {'build': MyBuild, 'build_doc': MyBuildDoc}


NAME = 'spyder'
LIBNAME = 'spyderlib'
from spyderlib import __version__
GOOGLE_URL = 'http://%s.googlecode.com' % NAME

setup(name=NAME,
      version=__version__,
      description='Scientific PYthon Development EnviRonment',
      long_description="""The spyderlib module provides powerful console and 
editor related widgets to your PyQt4 application. It also includes a 
Scientific Python development environment named 'Spyder', an alternative to
IDLE with powerful interactive features such as variable explorer (with 
GUI-based editors for dictionaries, lists, NumPy arrays, etc.), object 
inspector, online help, and a lot more.""",
      download_url='%s/files/%s-%s.zip' % (GOOGLE_URL, NAME, __version__),
      author="Pierre Raybaut",
      url=GOOGLE_URL,
      license='MIT',
      keywords='PyQt4 editor shell console widgets IDE',
      platforms=['any'],
      packages=get_subpackages(LIBNAME)+get_subpackages('spyderplugins'),
      package_data={LIBNAME:
                    get_package_data(LIBNAME, ('.mo', '.svg', '.png', '.css')),
                    'spyderplugins':
                    get_package_data('spyderplugins', ('.mo', '.svg', '.png'))},
      requires=["pyflakes (>0.3.0)", "rope (>0.9.0)", "sphinx (>0.6.0)",
                "PyQt4 (>4.3)"],
      scripts=[osp.join('scripts', fname) for fname in 
               (['spyder', 'spyder.bat'] if os.name == 'nt' else ['spyder'])],
      classifiers=['License :: OSI Approved :: MIT License',
                   'Operating System :: MacOS',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: OS Independent',
                   'Operating System :: POSIX',
                   'Operating System :: Unix',
                   'Programming Language :: Python :: 2.5',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Development Status :: 5 - Production/Stable',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Software Development :: Widget Sets'],
      cmdclass=cmdclass)
