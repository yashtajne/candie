from setuptools import setup, find_packages

setup(
    name='candie.kit',
    version='1.3.0',
    packages=find_packages(),
    py_modules=["main"],
    include_package_data=True,
    install_requires=['typer', 'pkgconfig', 'requests'],
    entry_points={
        'console_scripts': [
            'candie=main:start',
        ],
    },
    author='Yash Tajne',
    # author_email='',
    description='A CLI Build tool for C/C++ Projects',
    url='https://github.com/yashtajne/candie',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT License',
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)