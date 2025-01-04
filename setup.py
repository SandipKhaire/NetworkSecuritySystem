'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''

from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    Read the requirements.txt file and return the content as a list of strings
    """
    requirement_lst: List[str] = []

    try:
        with open('requirements.txt') as f:
            # Read Lines from the file
            lines = f.readlines()
            ## Process each line
            for line in lines:
                requirement = line.strip()
                ##ignore emtpy lines and -e .
                if requirement and requirement != '-e .' :
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("Requirements file not found")

    return requirement_lst
               
setup( 
    name='my_package', 
    version='0.0.1', 
    author='Sandip Khaire',
    author_email= 'spkhaire007@gmail.com',
    packages=find_packages(), 
    install_requires=get_requirements()
)