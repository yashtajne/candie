
# In-Built functions

### List of in-built functions.<br>
- [fetch_content](#Fetch_Content)
- [run_command](#run_command)
- [copy_files](#copy_files)
- [copy_directory](#copy_directory)
- [grab_dependency](#grab_dependency)
- [grab_files](#grab_files)
- [grab_sources](#grab_sources)
- [grab_headers](#grab_headers)

<br>

## Fetch_Content()

Downloads a project from a remote (URL),
and executes the `BUILD` section of the candie file.

The URL must point to a __`.zip`__ file.
which contains the project.

```py
fetch_content(
    url   : str,
    place : str,
)
```
__@params__<br>
__url__ : URL of the project archive.<br>
__place__ : Directory where the archive will be placed and extracted. its set to `DOWNLOADS_DIR` by default.

<br>

## Run_Command()

Used to execute a command.

```py
run_command(
    *cmd           : str,
    directory      : str,
    shell          : bool,
    capture_output : bool,
) -> subprocess.CompletedProcess
```
__@params__<br>
__cmd__ : Command.<br>
__directory__ : Directory where the command will be executed.<br>
__shell__ : Execute through shell.<br>
__capture_output__ : Captures output.

__@returns__<br>
It returns a subprocess CompletedProcess object.

<br>

## Copy_Files()

Copies the provided list of files into a destination directory.

```py
copy_files(
    files     : list[str]
    directory : str
)
```

__@params__<br>
__files__ : List of file paths<br>
__directory__ : Directory where the files are supposed to be pasted<br>

<br>

## Copy_Directory()

Copies the contents of the source directory into a destination directory.

```py
copy_directory(
    source      : str
    destination : str
)
```

__@params__<br>
__source__ : Directory which will get copied<br>
__destination__ : Directory where the contents will be pasted<br>

<br>

## Grab_Dependency()

Used to find and get cflags and libs of a library.
It will search for the package in the provided directory which is `LOCAL_INSTALL_DIR` by default.
if not found there. it will search it in the system.

```py
grab_dependency(
    name      : str,
    debug     : bool,
    target    : Target,
    directory : str,
) -> dict
```

__@params__<br>
__name__ : Name of the package<br>
__target__ : Finds for specific target<br>
__debug__ : Find debug version of the package. its `False` by default.<br>
__directory__ : Directory where it will search for the pkgconfig files. it is set to `LOCAL_INSTALL_DIR` by default.

__@returns__<br>
It Returns a dict which contains cflags and libs.

<br>

## Grab_Files()

Used to get files paths of all the files with the provided file extention in the provided directory.

```py
grab_files(
    directory_path: str, 
    file_ext:       str
)
```

## Grab_Sources()

This will get the files paths of all the source files based of the project language from the provided directory.

```py
grab_sources(
    source_directory_path: str
)
```


## Grab_Headers()

This will get the files paths of all the header files based of the project language from the provided directory.

```py
grab_headers(
    source_directory_path: str
)
```
