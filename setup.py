from setuptools import setup, find_packages

setup(
    name='candie.kit',
    version='1.1.0',
    packages=find_packages(),
    py_modules=[],
    include_package_data=True,
    install_requires=["typer", "toml"],
    entry_points={
        'console_scripts': [
            'candie=candie.cli:candie_exec',
        ],
    },
    author='Yash Tajne',
    # author_email='',
    description='A CLI Build tool for C/C++ projects',
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