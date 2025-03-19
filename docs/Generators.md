
# Generators


There are 3 types of generators.<br>
1. [executable()](#executable)
2. [library()](#library)
3. [package()](#package)

<br>

## Executable()

Creates an Executable file.

```py
executable(
    name         : str,
    *sources     : str.
    dependencies : list[str] = [],
    c_args       : list[Arg] = [],
    link_args    : list[Arg] = [],
    target       : Target    = NATIVE,
    make_out_dir : str       = PROJECT_ROOT
)
```

__name__ : Name of the executable file.<br>
__sources__ : Source file paths.<br>
__dependencies__ : List of dependency names.<br>
__c_args__ : Compiler Arguments.<br>
__link_args__ : Linker Arguments.<br>
__target__ : Target platform triplet. Its NATIVE by default<br>
__make_out_dir__ : The directory where the executable will be placed after compilation. Its set to PROJECT_ROOT by default.

<br>

## Library()

Creates a Library. It can either be a static archive or a shared object based of the `lib_type` parameter.

> __`!important`__ This will not create a pkgconfig file. 

```py
library(
    name         : str,
    type         : STATIC | SHARED,
    *sources     : str,
    dependencies : list[str] = [],
    c_args       : list[Arg] = [],
    link_args    : list[Arg] = [],
    target       : Target    = NATIVE,
    make_out_dir : str       = PROJECT_ROOT
)
```

__name__ : Name of the library file.<br>
__type__ : Type of library. put `STATIC` for static and `SHARED` for dynamic.<br>
__sources__ : Source file paths.<br>
__dependencies__ : List of dependency names.<br>
__c_args__ : Compiler Arguments.<br>
__link_args__ : Linker Arguments.<br>
__target__ : Target platform triplet. Its NATIVE by default<br>
__make_out_dir__ : The directory where the library file will be placed after compilation. Its set to PROJECT_ROOT by default.

<br>

## Package()

A Package can consist of multiple libraries.
It can generate a pkgconfig file for the libraries.

```py
package(
    name         : str,
    *libraries   : Library,
    target       : Target    = NATIVE,
    install_dir  : str       = LOCAL_INSTALL_DIR,
    cflags       : list[str] = [],
    description  : str       = '',
    version      : str       = '0.0.0',
    url          : str       = ''
)
```
__name__ : Name of the package file.<br>
__libraries__ : Libraries in the package.<br>
__target__ : Target platform triplet. Its `NATIVE` by default<br>
__install_dir__ : The directory where the libraries will be installed. its set to the projects install directory `LOCAL_INSTALL_DIR`<br>
__cflags__ : List of compilation flags. that whould be added to the cflags label in the pkgconfig file of the package.<br>
__description__ : Description of the package<br>
__version__ : Version of the package.<br>
__url__ : URL of the package.<br>