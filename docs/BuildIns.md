
# In-Built functions

### List of in-built functions.<br>
- [run_command](#run_command)
- [grab_dependency](#grab_dependency)
- [grab_files](#grab_files)
- [grab_sources](#grab_sources)
- [grab_headers](#grab_headers)


## Run_Command()

Used to execute a shell command.

```
run_command(
    *cmd:           str,
    dir:            str  = PROJECT_ROOT,
    shell:          bool = False,
    capture_output: bool = False
)
```


## Grab_Dependency()

Used to find and get cflags and libs of a library.

```
grab_dependency(
    library_name:   str,
    debug:          bool = False,
    triplet:        str  = NATIVE,
    dependency_dir: str  = None
)
```

## Grab_Files()

Used to get files paths of all the files with the provided file extention in the provided directory.

```
grab_files(
    directory_path: str, 
    file_ext:       str
)
```

## Grab_Sources()

This will get the files paths of all the source files based of the project language from the provided directory.

```
grab_sources(
    source_directory_path: str
)
```


## Grab_Headers()

This will get the files paths of all the header files based of the project language from the provided directory.

```
grab_headers(
    source_directory_path: str
)
```
