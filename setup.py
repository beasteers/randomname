import setuptools

USERNAME = 'beasteers'
NAME = 'randomname'

setuptools.setup(
    name=NAME,
    version='0.1.2',
    description='Generate random adj-noun names like docker and github.',
    long_description=open('README.md').read().strip(),
    long_description_content_type='text/markdown',
    author='Bea Steers',
    author_email='bea.steers@gmail.com',
    url='https://github.com/{}/{}'.format(USERNAME, NAME),
    packages=setuptools.find_packages(),
    package_data={NAME: ['wordlists/**/*.txt']},
    entry_points={'console_scripts': ['{name}={name}:main'.format(name=NAME)]},
    install_requires=['fire'],
    license='MIT License',
    keywords='random name generator docker container github repo '
             'word list noun adjective verb')
