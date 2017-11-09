from setuptools import setup
from setuptools import find_packages
def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='ppipe',
    version='0.2.0',
    packages=find_packages(),
    package_data={'ppipe': ['logconfig.json','aoi.json','wrs_grid.csv']},
    url='https://github.com/samapriya/Planet-GEE-Pipeline',
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ),
    author='Samapriya Roy',
    author_email='samapriya.roy@gmail.com',
    description='Planet API Pipeline & Google Earth Engine Batch Assets Manager with Addons',
    entry_points={
        'console_scripts': [
            'ppipe=ppipe.ppipe:main',
        ],
    },
)
