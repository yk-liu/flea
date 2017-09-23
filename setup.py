#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from LEA import __version__ as version

maintainer = 'Ying-kai-Liu'
maintainer_email = '949482709@qq.com'
author = 'Ying-kai-Liu'
author_email = '949482709@qq.com'
description = "A List-based Evolution Algorithm Framework in Python"
# long_description = ''''''

install_requires = ['easygui',]

license = 'LICENSE'

name = 'LEA'
packages = ['LEA',]
platforms = ['linux', 'windows', 'macos']
url = 'https://github.com/PytLab/gaft'
# download_url = ''

classifiers = [
    'Development Status :: 1 - Alpha',
    'Topic :: Utilities',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
]

setup(author=author,
      author_email=author_email,
      description=description,
      license=license,
      install_requires=install_requires,
      maintainer=maintainer,
      name=name,
      packages=find_packages(),
      platforms=platforms,
      url=url,
      version=version)

