
# SETUP section

The Setup section contains a required function named [__project()__](#project)

This section always executes first.
So you can check if the required dependecies for the project is installed or not and install them.

You can create global variables in the SETUP section that can be accessed from any section of the `Candie.build` file.

## project()
```py
project(
    name     : str,
    language : C | CPP,
    version  : str 
)
```
- `name`: A String value for the project<br>
- `language`: Provide either C or CPP, C for project which only uses c and you can use CPP for c++ or if the project uses both c and c++ files.<br>
- `version`: String value for version. it can be Schemantic, Calender-based, Incremental or custom.
