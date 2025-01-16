import os

cwd = os.getcwd()                          # Current working directory

DIRS = {
    "CANDIE_DIR": f"{cwd}/.candie",                          # Candie directory

    "SRC_DIR": f"{cwd}/src",                                 # Source code directory
    "BUILD_DIR": f"{cwd}/build",                             # Build directory
    "INCLUDE_DIR": f"{cwd}/include",                         # Include directory

    "LIB_DIR": f"{cwd}/lib",                                 # Library directory
    "LIB_PKGCONFIG_DIR": f"{cwd}/lib/pkgconfig",             # Library pkgconfig directory

    "DEBUG_DIR": f"{cwd}/debug",                             # Debug build directory

    "DEBUG_LIB_DIR": f"{cwd}/debug/lib",                     # Debug library directory
    "DEBUG_LIB_PKGCONFIG_DIR": f"{cwd}/debug/lib/pkgconfig", # Debug library pkgconfig directory

    "DEBUG_BIN_DIR": f"{cwd}/debug/bin",                     # Debug binary directory
    "DEBUG_BIN_CACHE_DIR": f"{cwd}/debug/bin/cache",         # Debug binary cache directory
    "DEBUG_BIN_OUTPUT_DIR": f"{cwd}/debug/bin/output"        # Debug binary output directory
}

MODIF_LOG_FILE = f"{cwd}/.candie/log-file.json"               # Log file path
PROJ_CONFIG_FILE = f"{cwd}/proj-config.toml"                  # Project configuration file path

PKG_INDEX_FILE = f"{cwd}/.candie/pkg-index.json"              # Package index file path