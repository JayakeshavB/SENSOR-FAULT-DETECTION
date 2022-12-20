from setuptools import setup, find_packages

__version__ = '0.0.1'

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()
    for package in install_requires:
        if package == '-e .':
            install_requires.remove(package)

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
    install_requires=install_requires
    )
