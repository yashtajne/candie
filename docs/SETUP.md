
# SETUP section

The Setup section contains a required function named `project()`


You can create global variables in the SETUP section that can be from in any section of the `Candie.build` file.


## project()
```py
project(
    name     = 'project_name',
    language =  CPP,
    version  = '1.0.0' 
)
```
- `name`: A String value for the project<br>
- `language`: Provide either C or CPP, C for project which only uses c and you can use CPP for c++ or if the project uses both c and c++ files.<br>
- `version`: String value for version. it can be Schemantic, Calender-based, Incremental or custom.
