from distutils.core import setup

setup(
	name='pyidl',
	version='0.0.1',
	author='Maluuba',
	author_email='contact@maluuba.com',
	packages=['pyidl', 'pyidl.parser', 'pyidl.generator'],
	url='http://github.com/apetresc/IDLGenerator',
	license='LICENSE',
	description='A parser and code generation library for Thrift IDL files',
	long_description=open('README.md').read(),
	install_requires=[
		'ply >= 3.4'
	]
)