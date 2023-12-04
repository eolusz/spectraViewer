#!/usr/bin/env python
import shutil
from os.path import dirname, join, realpath

from setuptools import find_packages, setup

ROOT_FOLDER = dirname(realpath(__file__))
VERSION_FILE_PATH = join(ROOT_FOLDER, '_version.py')


scm_version = {'write_to': VERSION_FILE_PATH}


setup(name='SpectraViewer',
      use_scm_version=scm_version,
      author='ardana-lamas',
      author_email='ardana-lamas',
      description='',
      long_description='',
      url='',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      },
      package_data={},
      requires=[],
      )


# copy to subpaths with Karabo class files

shutil.copy(join(ROOT_FOLDER, '_version.py'),
            join(ROOT_FOLDER, "src/spectraViewer"))

