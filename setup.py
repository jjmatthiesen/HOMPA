"""
HOMPA
A Python library for the calculation of the ideal proportion of home office
"""
from distutils.core import setup
from setuptools import find_packages

short_description = __doc__.split("\n")

try:
    with open("README.md", "r") as handle:
        long_description = handle.read()
except:
    long_description = "\n".join(short_description[2:])


setup(
  name = 'HOMPA',         # How you named your package folder (MyLib)
  packages = find_packages(),   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = short_description[0],   # Give a short description about your library
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Mark Colley',                   # Type in your name
  author_email = 'mark.colley@yahoo.de',      # Type in your E-Mail
  url = 'https://github.com/jjmatthiesen/HOMPA',   # Provide either the link to your github or to your website
  download_url = '',   # I explain this later on
  keywords = ['Home Office', 'Multi-Perspective'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
          'datetime',
          'warnings',
          'pathlib',
      ],
  include_package_data=True,
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
  ],
)
