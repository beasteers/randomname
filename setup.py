import setuptools

USERNAME = 'beasteers'
NAME = 'randomname'

setuptools.setup(
    name=NAME,
    version='0.1.5',
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
    tests_require=['pytest'],
    license='MIT License',
    keywords='random name generator docker container github repo '
             'word list noun adjective verb',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
