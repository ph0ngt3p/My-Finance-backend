from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
	name = 'My Finance',
	version = '0.0.5',
	author = 'Tuan Dzung',
	author_email = 'zun1903@gmail.com',
	description = ('My Finance project backend'),
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/ph0ngt3p/My-Finance-backend',
	packages=find_packages(),
	test_suite='nose2.collector.collector'
)