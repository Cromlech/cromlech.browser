# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


version = '1.0+crom'

install_requires = [
    'grokker',
    'setuptools',
    'zope.interface',
    ]

tests_require = [
    'beautifulsoup4 > 4.4.5',
    'pytest',
    ]

setup(name='cromlech.browser',
      version=version,
      description="Cromlech Web Framework browser components definitions.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='Cromlech Dolmen Framework',
      author='The Dolmen team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://gitweb.dolmen-project.org/',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['cromlech',],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
