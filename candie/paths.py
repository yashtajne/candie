import os

cwd = os.getcwd()                          # Current working directory


PROJ_CONFIG_FILE = f"{cwd}/proj-config.toml"                 # Project configuration file path
PROJ_DIRS = {
    "CANDIE_DIR": f"{cwd}/.candie",                          # Candie directory
    "CACHE_DIR": f"{cwd}/.candie/cache",                     # cache directory

    "SRC_DIR": f"{cwd}/src",                                 # Source code directory
    "BUILD_DIR": f"{cwd}/build",                             # Build directory
    "INCLUDE_DIR": f"{cwd}/include",                         # Include directory

    "LIB_DIR": f"{cwd}/lib",                                 # Library directory
    "LIB_PKGCONFIG_DIR": f"{cwd}/lib/pkgconfig",             # Library pkgconfig directory

    "DEBUG_DIR": f"{cwd}/debug",                             # Debug build directory

    "DEBUG_LIB_DIR": f"{cwd}/debug/lib",                     # Debug library directory
    "DEBUG_LIB_PKGCONFIG_DIR": f"{cwd}/debug/lib/pkgconfig", # Debug library pkgconfig directory

    "DEBUG_BIN_DIR": f"{cwd}/debug/bin",                     # Debug binary directory
}

# PKG_CONFIG_FILE = f"{cwd}/pkg-config.toml"                  # Package configuration file path
# PKG_DIRS = {
#     "CANDIE_DIR": f"{cwd}/.candie",                          # Candie directory
#     "CACHE_DIR": f"{cwd}/.candie/cache",                     # cache directory

#     "SRC_DIR": f"{cwd}/test/src",                            # Source code directory
#     "INCLUDE_DIR": f"{cwd}/include",                         # Include directory

#     "LIB_DIR": f"{cwd}/lib",                                 # Library directory
#     "LIB_PKGCONFIG_DIR": f"{cwd}/lib/pkgconfig",             # Library pkgconfig directory

#     "DEBUG_DIR": f"{cwd}/debug",                             # Debug build directory

#     "DEBUG_LIB_DIR": f"{cwd}/debug/lib",                     # Debug library directory
#     "DEBUG_LIB_PKGCONFIG_DIR": f"{cwd}/debug/lib/pkgconfig", # Debug library pkgconfig directory

#     "PACKAGE_DIR": f"{cwd}/package",                         # package directory
#     "PACKAGE_HEADERS_DIR": f"{cwd}/package/HEADERS",         # Package include files 
# }


MODIF_LOG_FILE = f"{cwd}/.candie/log-file.json"               # Log file path
PKG_INDEX_FILE = f"{cwd}/.candie/pkg-index.json"              # Package index file path