from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]


setup(name='power_project',
      version='0.0.0',
      author='John Riecken',
      install_requires=requirements,
      packages=find_packages()
      )
