# Variables

These are the variables which are predefined and can be accessed in the Candiefile

+ [Target](#target)
+ [TARGETS](#targets)
+ [Arg](#arg)
+ [C_ARGS](#c_args)
+ [LINK_ARGS](#link_args)

<br>

## Target

The Target class is used for creating a Target.
```py
Target(
    cpu : str,
    os  : str,
    abi : str,
)
```

__cpu__ : cpu of target [required option].<br>
__os__ : os of the target.<br> 
__abi__ : abi of the target. 

### TARGETS 

List of Targets

```py
TARGETS = [
    (NATIVE := Target('native')),

    (X86_WINDOWS    := Target('x86',     'windows')),
    (X64_WINDOWS    := Target('x86_64',  'windows')),
    (ARM64_WINDOWS  := Target('aarch64', 'windows')),

    (X86_LINUX      := Target('x86',     'linux')),
    (X64_LINUX      := Target('x86_64',  'linux')),
    (ARM64_LINUX    := Target('aarch64', 'linux')),

    (ARM64_MACOS    := Target('aarch64', 'macos')),
    (X86_MACOS      := Target('x86',     'macos')),
    (X64_MACOS      := Target('x86_64',  'macos'))
]
```

<br>

## Arg

The Arg class is used for creating an Argument.
Argument is used to pass in while compilation or linking phase.

```py
Arg(
    arg: str
)
```
__arg__ : argument.

There are predefined arguments already created so you dont have to create each one manually.
But if you cant find your specific arg. then yu can create it using this class.

<br>

### C_ARGS

This is a list of compiler arguments.

```py
C_ARGS = [

    # Optimization
    (O0 := Arg('-O0')),
    (O1 := Arg('-O1')),
    (O2 := Arg('-O2')),
    (O3 := Arg('-O3')),
    (OS := Arg('-Os')),
    (OZ := Arg('-Oz')),

    # Warning and error
    (W_ALL      := Arg('-Wall')),
    (W_EXTRA    := Arg('-Wextra')),
    (W_ERROR    := Arg('-Werror')),
    (W_PEDANTIC := Arg('-Wpedantic')),

    # Standard version c
    (STD_C89     := Arg('-std=c89')),
    (STD_C90     := Arg('-std=c90')),
    (STD_GNU89   := Arg('-std=gnu89')),
    (STD_C99     := Arg('-std=c99')),
    (STD_GNU99   := Arg('-std=gnu99')),
    (STD_C11     := Arg('-std=c11')),
    (STD_GNU11   := Arg('-std=gnu11')),
    (STD_C17     := Arg('-std=c17')),
    (STD_GNU17   := Arg('-std=gnu17')),
    (STD_C23     := Arg('-std=c23')),
    (STD_GNU23   := Arg('-std=gnu23')),

    # Standard version c++
    (STD_CPP98   := Arg('-std=c++98')),
    (STD_GNUPP98 := Arg('-std=gnu++98')),
    (STD_CPP03   := Arg('-std=c++03')),
    (STD_GNUPP03 := Arg('-std=gnu++03')),
    (STD_CPP11   := Arg('-std=c++11')),
    (STD_GNUPP11 := Arg('-std=gnu++11')),
    (STD_CPP014  := Arg('-std=c++14')),
    (STD_GNUPP14 := Arg('-std=gnu++14')),
    (STD_CPP17   := Arg('-std=c++17')),
    (STD_GNUPP17 := Arg('-std=gnu++17')),
    (STD_CPP20   := Arg('-std=c++20')),
    (STD_GNUPP20 := Arg('-std=gnu++20')),
    (STD_CPP23   := Arg('-std=c++23')),
    (STD_GNUPP23 := Arg('-std=gnu++23')),
]
```

<br>

### LINK_ARGS

This is a list of linker arguments.

```py
LINK_ARGS = [

    # Optimiztion & Size reduction
    (WL_O1          := Arg('-Wl,-O1')),
    (WL_O2          := Arg('-Wl,-O2')),
    (WL_ASNEEDED    := Arg('-Wl,--as-needed')),
    (WL_GC_SECTIONS := Arg('-Wl,--gc-sections')),
    (WL_STRIP_ALL   := Arg('-Wl,--strip-all')),
    (WL_STRIP_DEBUG := Arg('-Wl,--strip-debug')),
    (WL_ICF_SAFE    := Arg('-Wl,--icf=safe')),

    # For Performance
    (WL_HASH_STYLE_GNU := Arg('-Wl,--hash-style=gnu')),
    (WL_NO_KEEP_MEMORY := Arg('-Wl,--no-keep-memory')),
    (WL_THREADS        := Arg('-Wl,--threads')),

    # Debugging & Profiling
    (WL_EXPORT_DYNAMIC := Arg('-Wl,--export-dynamic')),
    (WL_PRINT_MAP      := Arg('-Wl,--print-map')),
    (WL_VERBOSE        := Arg('-Wl,--verbose')),
    (WL_WARN_COMMON    := Arg('-Wl,--warn-common')),
]
```