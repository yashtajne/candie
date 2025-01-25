
# Candie 

A simple build tool for C/C++ projects that eliminates the need of using Makefiles.

> !__Important Note__ <br>
> It needs `zig` and `vcpkg` installed in  your system. If not installed most of its features wont work.


### Installation

Run this command in you terminal, to install using the python pip package manager.

```sh
pip install candie.kit
```

### What it does.

It can compile/build the project. No need of MakeFiles. It can search for all the (.c & .cpp) files the src directory of the project.
It basically runs compile, linking commands for you.

#### How it works
+ It keeps track of source (.c, .cpp) files.
+ Recompiles the files that has been modified or newly added.
+ Caches the files which has been compiled so it does not have to compile it again if its not modified.

### Project structure.

The `candie create <project_name>` will create the project in the directory where you run the command.

```
├── .candie/           # Dont edit these files
│   ├── pkg-index.json
│   ├── pkg-index.json
│   └── cache/ 
├── include/           # Include files
├── lib/               # Libraries
│   └── pkgconfig/
├── debug/
│   ├── lib/           # Debug libraries
│   │   └── pkgconfig/
│   └── bin/           # Debug binary
├── build/             # Release binary
├── src/               # Source files
└── proj-config.toml   # Config file
```

You can create .c and .cpp files in the src directory.

### Make & Run.

You can create an executable for debugging by running the `candie make` command.
Then run that executable by running `candie run` command.

### Packages.

Adding and Removing vcpkg packages is pretty easy.

`candie add <package_name>` add the package.<br>
`candie remove <package_name>` remove the package.

It will just copy the include and lib files of the package from the vcpkg installed directory to the project directory.

### Build.

To build the project for multiple platforms. you can add more targets to the project config file `[Build]` table.

#### Project config file `proj-config.toml` structure

```toml
[project]
name = "myapp"
description = "example description"
version = "0.0.1"

[debug]     # additional flags for debugging
Cflags = [ "-Wall", "-Wextra", "-g",] # compiler flags
Lflags = [ "-Wl,--no-undefined",] # linker flags

[build]     # additional flags for build release
flags = [ "-Wl,--no-undefined",] 

[[build.target]]    # for 64 bit windows machine
arch = "x86_64"
os = "windows"

[[build.target]]    # for 64 bit linux machine
arch = "x86_64"
os = "linux"

[[build.target]]    # for 64 bit ARM mac os
arch = "aarch64"
os = "macos"

[requirements]              # this will be added by build tool you dont have to edit these
[[requirements.package]]    # installed packages will be listed like this
name = "package-name"
description = "package-description"
url = "package-website-url"
version = "package-version"
```


#### ...