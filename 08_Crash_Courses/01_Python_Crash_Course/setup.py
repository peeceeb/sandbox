'''
The setup.py file is an essential part of packaging and distributing Python projects. It
is used by setuptools to define the configuration of your project, such as metadata, dependencies and more
'''

from setuptools import find_packages, setup
from typing import List

def get_requirement()->List[str]:

    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            #Read lines from the file
            lines=file.readlines()
            #Process each line
            for line in lines:
                requirement=line.strip()
                ##ignore empty lines and -e.
                if requirement and requirement!= '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirement.txt file not found")

    return requirement_lst


setup(
    name="01_Test_Package",
    version="V1",
    author="Prasanna Bagal",
    author_email="bagal.prasanna@gmail.com",
    packages=find_packages(),
    install_requires=get_requirement()
)
        