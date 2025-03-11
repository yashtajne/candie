
# Generators


There are 3 types of generators.<br>
1. [executable()](#executable)
2. [library()](#library)
3. [package()](#package)

Executable and Package are the two main generators that you should mostly use.

## Executable()

Creates an Executable file.

```py
executable(
    name = 'MyExe',
    *(
        './path/to/src/file.c'
        './path/to/src/file.cpp'
    ),
    dependencies = [],
    c_args = [],
    link_args = [],
    triplet = NATIVE,
    make_out_dir = '.'
).create(debug = False)
```

### parameters

- `name`: name of the executable file

- `dependencies`: a list of names of the packages. 

- `c_args`: list of compiler arguments 

- `link_args`: list of linker arguments 

- `triplet`: target triplet, its NATIVE by default

- `make_out_dir`: output directory

### methods

- `link_against(dep: Dependency)`: You can provide a dependency to link with.

- `create(debug: bool = False)`: This method creates the executable.
the `debug` param will add debugging symbols to the executable.

## Library()

Creates a Library. It can either be a static archive or a shared object based of the `lib_type` parameter.

> __`!important`__ This will not create a pkgconfig file. 

```py
library(
    name = 'MyLib',
    lib_type = STATIC,
    *(
        './path/to/src/file.c'
        './path/to/src/file.cpp'
    ),
    dependencies = [
        'example'
    ],
    c_args = [],
    triplet = NATIVE,
    make_out_dir = '.'
).create()
```

### parameters

- `name`: name of the library file

- `dependencies`: a list of names of the packages. 

- `c_args`: list of compiler arguments 

- `triplet`: target triplet, its NATIVE by default

- `make_out_dir`: output directory

### methods

- `link_against(dep: Dependency)`: You can provide a dependency to link with.

- `create(debug: bool = False)`: This method creates the library.
the `debug` param will add debugging symbols to the library.

## Package()

A Package can consist of multiple libraries.
It can generate a pkgconfig file for the libraries.

```py
package(
    name = 'MyPkg',
    *(
        library(
            'MyLib1',
            STATIC,
            *grab_sources('./src1')
        ),
        library(
            'MyLib2',
            STATIC,
            *grab_sources('./src2')
        )
    ),
    triplet: str = NATIVE,
    install_dir: str = LOCAL_INSTALL_DIR,
    cflags: list[str] = [],
    description: str = '',
    version: str = '0.0.0',
    url: str = ''
).create(debug = True)
```

### parameters

- `name`: name of the Package

- `cflags`: Compiler flags that will be added to the pkgconfig file

- `triplet`: target triplet, its NATIVE by default

- `install_dir`: output directory

- `description`: description of the Package

- `version`: version of the Package

- `url`: url of the Package



### methods

- `create(debug: bool = False)`: This method creates all the libraries.
the `debug` param will add debugging symbols to the libraries.