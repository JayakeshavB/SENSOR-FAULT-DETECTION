from setuptools import setup, find_packages
from typing import List

__version__ = '0.0.1'

REQUIREMENT_FILE_NAME="requirements.txt"

HYPHEN_E_DOT = "-e ."


def get_requirements_list() -> List[str]:
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
        return requirement_list

setup(
    name='sensor_fault_detector',
    version=__version__,
    description='Sensor Fault Detector',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JayakeshavB/SENSOR-FAULT-DETECTION',
    author='JayakeshavB',
    author_email='jayakeshav10807@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements_list()
    )
