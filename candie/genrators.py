import os

from pathlib import Path


from . import STATIC, SHARED, PROJECT, LOCAL_INSTALL_DIR, TRIPLETS, NATIVE
from .utils import Generate_PkgConfig_File, Copy_Files, Grab_Dependency, Generate_Library_Name
from .printer import Print_Error


class Executable:
    def __init__(self,
            name: str, 
            *sources: str,
            dependencies: list[dict] = [],
            c_args: list[str] = [],
            link_args: list[str] = [],
            triplet = NATIVE,
            make_out_dir: str = '.',
        ):
        self.name = name
        self.sources = {str(Path(src).resolve()) for src in sources}

        # Dependencies 
        self.dependencies = dependencies

        # Compiler arguments
        self.cflags: list[str] = c_args
        self.lflags: list[str] = link_args

        # Triplet
        if triplet not in TRIPLETS:
            Print_Error(f"Invalid Triplet. ({triplet})")
            raise SystemExit
        self.triplet = triplet
        
        # Directories
        self.make_out_dir = make_out_dir
        if not os.path.isdir(make_out_dir):
            os.makedirs(make_out_dir)
    
    def link_against(self, dependency: dict):
        if dependency:
            self.cflags.append(dependency.get('cflags', ''))
            self.lflags.append(dependency.get('libs', ''))
        else:
            print("Error: invalid dependency")
        return self

    def create(self, debug: bool = False):
        # Setting triplet
        self.cflags.append('-target')
        self.cflags.append(self.triplet)

        # Add debugging symbols
        if debug: self.cflags.append('-g') 

        # Dependencies
        for dependency in self.dependencies:
            self.link_against(Grab_Dependency(dependency, debug=debug, triplet=self.triplet))

        # Build the Executable
        PROJECT['compiler'].link(
            output=f"{self.make_out_dir}/{self.name}",
            input_files=list(self.sources),
            l_flags=self.cflags + [lflag for lflags in self.lflags for lflag in lflags.split()]
        )

        return self


class Library:
    def __init__(self, 
            name: str, 
            lib_type: str, 
            *sources: str,
            dependencies: list[dict] = [],
            c_args: list[str] = [],
            triplet = NATIVE,
            make_out_dir: str = '.',
        ):
        self.name = name
        self.sources = {str(Path(src).resolve()) for src in sources}
        self.lib_type = STATIC if lib_type not in [STATIC, SHARED] else lib_type

        # Triplet
        if triplet not in TRIPLETS:
            Print_Error(f"Invalid Triplet. ({triplet})")
            raise SystemExit
        self.triplet = triplet

        # Output directory
        self.make_out_dir = make_out_dir

        # Dependencies
        self.requirements: list[str] = []
        for dependency in dependencies:
            self.requirements.append(dependency.get('name', ''))
            self.link_against(dependency)

        # Compiler arguments
        self.cflags: list[str] = c_args

    def link_against(self, dependency: dict):
        if dependency:
            self.requirements.append(dependency.get('name', ''))
            self.cflags.append(dependency.get('cflags', ''))
            self.lflags.append(dependency.get('libs', ''))
        else:
            print("Error: invalid dependency")
        return self

    def create(self, debug: bool = False):
        libdir = os.path.join(self.make_out_dir, 'debug', 'lib') if debug else os.path.join(self.make_out_dir, 'lib')
        if not os.path.isdir(libdir):
            os.makedirs(libdir)
                
        # output path
        output_path = os.path.join(libdir, Generate_Library_Name(self.name, self.lib_type, self.triplet))

        # setup target
        self.cflags.append('-target')
        self.cflags.append(self.triplet)

        # Strip debugging symbols
        if not debug: self.cflags.append('-fstrip')

        # Create library file
        if self.lib_type == STATIC:
            PROJECT['compiler'].archive(
                output=output_path,
                input_files=list(self.sources),
                options=self.cflags
            )
        elif self.lib_type == SHARED:
            self.lflags.append('-shared')
            PROJECT['compiler'].link(
                output=output_path,
                input_files=list(self.sources),
                l_flags=self.cflags
            )

        return self


class Package:
    def __init__(self, 
            name: str,
            *libraries: Library,
            triplet: str = NATIVE,
            install_dir: str = LOCAL_INSTALL_DIR,
            cflags: list[str] = [],
            description: str = '',
            version: str = '0.0.0',
            url: str = ''
        ):
        self.name = name
        self.description = description
        self.version = version
        self.url = url
        self.cflags = cflags

        # Triplet
        if triplet not in TRIPLETS:
            Print_Error(f"Invalid Triplet. ({triplet})")
            raise SystemExit
        self.triplet = triplet

        # Directories
        self.install_dir = os.path.join(install_dir, self.triplet)
        if not os.path.isdir(self.install_dir):
            os.makedirs(self.install_dir)

        # Libraries
        self.libraries = libraries
    
    def install_headers(self, *headers: str):
        Copy_Files(headers, f"{self.install_dir}/include")
        return self

    def create(self, debug: bool = False):
        pkgconfig_dir = f"{self.install_dir}{'/debug/lib/pkgconfig' if debug else '/lib/pkgconfig'}"
        if not os.path.isdir(pkgconfig_dir):
            os.makedirs(pkgconfig_dir)

        # Make libraries
        for library in self.libraries:
            library.make_out_dir = self.install_dir
            library.triplet = self.triplet
            library.create(debug=debug)
        
        # Write pkgconfig file
        with open(os.path.join(pkgconfig_dir, self.name + '.pc'), 'w') as dotpcfile:
            dotpcfile.write(Generate_PkgConfig_File(
                name=self.name,
                description=self.description,
                version=self.version,
                url=self.url,
                requires=[req for lib in self.libraries for req in lib.requirements],
                cflags=self.cflags,
                libs=[('-l' + lib.name) for lib in self.libraries],
                debug=debug
            ))

        return self