
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

In the project directory.
+ It keeps track of source (.c, .cpp) files.
+ Recompiles the files that has been modified or newly added.
+ Caches the files which has been compiled so it does not have to compile it again if its not modified.

### Project structure.

The `candie create <project_name>` will create the project in the directory where you run the command.

```
├── .candie/           # Dont edit these files
│   ├── pkg-index.json/
│   └── log-file.json/ 
├── include/           # Header files
├── lib/               # Libraries
│   └── pkgconfig/
├── debug/
│   ├── lib/           # Debug libraries
│   │   └── pkgconfig/
│   └── bin/
│       ├── cache/     # Cached object files
│       └── output/    # Debug binary
├── build/             # Release binary
├── src/               # Source files
└── candie-proj.conf   # Config file
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

To build the project for multiple platforms. you can add more targets to the project config file [Build] table.

```toml
[Project]
name = "example-app"
description = "example project"
version = "0.0.1"

[Build]
windows = "x86_64-windows"    # for 64 bit windows
linux = "x86_64-linux"        # for 64 bit linux
macos = "aarch64-macos"       # for ARM 64 macos

[requirements]
packages = []
```


#### ...