# Candie.kit

A Simple C/C++ Build tool.<br>
It Uses Zig as a drop-in compiler for compiling .c and .cpp files.

### List of contents<br>
- [Installation](#installation)
- [Getting started](#getting-started)
- [Documentation](#documentation)
<!-- - Examples -->


## Installation

Candie.kit is is available on [PyPI](https://pypi.org/project/candie.kit) so it can be installed with this command.
```sh
pip install candie.kit
```

### candie CLI

After installation you can run this command to get help.
or verify that its successfully installed.
```
candie --help
```

## Getting started

Every project must contain a Build Instruction file, Named `Candie.build` and this file should always be placed in the project root directory.

project/<br>
├── main.c<br>
├── greet.c<br>
└── Candie.build

So create this file for your project.
The `Candie.build` file can contain sections of code. 

A Section can be created like this [SECTION_NAME] section name should be UPPERCASE.
[SETUP] is a required section.

Example __Candie.build__ file 👇️
```py
[SETUP]

PROJ_NAME = 'your_project_name'

project(
    name = PROJ_NAME, 
    language = C, 
)


[BUILD]

executable(
    PROJ_NAME,
    './main.c',
    './greet.c'
).create()

```

You can either provide the source file paths manually or use the `grab_sources()` function
and provide the directory path of the src files.

Call the `create()` method to create the executable, You can provide `.create(debug = True)` to add debugging symbols to the executable.

finally, run this command to execute the build section.
```sh
candie build
```
This will create a executable named `'your_project_name'`<br>
Here, Example project [simple-exe](./examples/simple-exe/)

## Documentation

- [SETUP section](./docs/SETUP.md)
- [Generators](./docs/Generators.md)
- [InBuilt functions](./docs/BuildIns.md)

<!-- 
## Examples

+ [Simple console app]()
+ [String formatter package]() -->


## License

This project is licensed under the [Apache 2.0 License](LICENSE).  

<br>

<p align="center">Made with 🧡 by Yash Tajne</p>