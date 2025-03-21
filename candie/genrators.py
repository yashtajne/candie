import os

from pathlib import Path


from . import STATIC, SHARED, PROJECT, LOCAL_INSTALL_DIR, NATIVE, Target, Arg
from .utils import Generate_PkgConfig_File, Copy_Files, Grab_Dependency, Generate_Library_Name
from .printer import Print_Error


class Executable:
    def __init__(self,
            name: str, 
            *sources: str,
            dependencies: list[str] = [],
            c_args: list[Arg] = [],
            link_args: list[Arg] = [],
            target: Target = NATIVE,
            make_out_dir: str = '.',
        ):
        self.name = name
        self.sources = {str(Path(src).resolve()) for src in sources}

        # Dependencies 
        self.dependencies = dependencies

        # Compiler arguments
        self.c_args = c_args
        self.link_args = link_args

        if not isinstance(target, Target):
            raise TypeError('target must be an instance of Target')

        self.triplet = target
        
        # Directories
        self.make_out_dir = make_out_dir
        if not os.path.isdir(make_out_dir):
            os.makedirs(make_out_dir)

    @property
    def c_args(self):
        return self._c_args

    @c_args.setter
    def c_args(self, value):
        if not isinstance(value, list) or not all(isinstance(arg, Arg) for arg in value):
            raise TypeError("c_args must be a list of Arg instances")
        self._c_args = value

    @property
    def link_args(self):
        return self._link_args

    @link_args.setter
    def link_args(self, value):
        if not isinstance(value, list) or not all(isinstance(arg, Arg) for arg in value):
            raise TypeError("link_args must be a list of Arg instances")
        self._link_args = value
    
    def link_against(self, dependency: dict):
        if dependency:
            self.c_args.append(dependency.get('cflags', ''))
            self.link_args.append(dependency.get('libs', ''))
        else:
            Print_Error(f"({dependency}) Dependecny not found!")
        return self

    def create(self, debug: bool = False):
        # Setting triplet
        self.c_args.append('-target')
        self.c_args.append(self.triplet)

        # Add debugging symbols
        if debug: self.c_args.append('-g') 

        # Dependencies
        for dependency in self.dependencies:
            self.link_against(Grab_Dependency(dependency, debug=debug, triplet=self.triplet))

        # Build the Executable
        PROJECT['compiler'].link(
            output=f"{self.make_out_dir}/{self.name}",
            input_files=list(self.sources),
            l_flags=self.c_args + [lflag for lflags in self.link_args for lflag in lflags.split()]
        )

        return self


class Library:
    def __init__(self, 
            name: str, 
            type: str, 
            *sources: str,
            dependencies: list[str] = [],
            c_args: list[Arg] = [],
            link_args: list[Arg] = [],
            target: Target = NATIVE,
            make_out_dir: str = '.',
        ):
        self.name = name
        self.sources = {str(Path(src).resolve()) for src in sources}
        
        if type not in [SHARED, STATIC]:
            raise TypeError("invalid library type provided")

        self.lib_type = type

        if not isinstance(target, Target):
            raise TypeError('target must be an instance of Target')

        self.triplet = target

        # Output directory
        self.make_out_dir = make_out_dir

        # Dependencies
        self.requirements: list[str] = []
        for dependency in dependencies:
            self.requirements.append(dependency.get('name', ''))
            self.link_against(dependency)

        # Compiler arguments
        self.c_args = c_args
        self.link_args = link_args

    @property
    def c_args(self):
        return self._c_args

    @c_args.setter
    def c_args(self, value):
        if not isinstance(value, list) or not all(isinstance(arg, Arg) for arg in value):
            raise TypeError("c_args must be a list of Arg instances")
        self._c_args = value

    @property
    def link_args(self):
        return self._link_args

    @link_args.setter
    def link_args(self, value):
        if not isinstance(value, list) or not all(isinstance(arg, Arg) for arg in value):
            raise TypeError("link_args must be a list of Arg instances")
        self._link_args = value

    def link_against(self, dependency: dict):
        if dependency:
            self.requirements.append(dependency.get('name', ''))
            self.c_args.append(dependency.get('cflags', ''))
            self.link_args.append(dependency.get('libs', ''))
        else:
            Print_Error(f"({dependency}) Dependecny not found!")
        return self

    def create(self, debug: bool = False):
        libdir = os.path.join(self.make_out_dir, 'debug', 'lib') if debug else os.path.join(self.make_out_dir, 'lib')
        if not os.path.isdir(libdir):
            os.makedirs(libdir)
                
        # output path
        output_path = os.path.join(libdir, Generate_Library_Name(self.name, self.lib_type, self.triplet))

        # setup target
        self.c_args.append('-target')
        self.c_args.append(self.triplet)

        # Strip debugging symbols
        if not debug and self.lib_type == STATIC:
            self.c_args.append('-fstrip')
        elif not debug and self.lib_type == SHARED:
            self.c_args.append('--strip-debug')   
        elif debug and self.lib_type == SHARED:
            self.c_args.append('-g')

        # Create library file
        if self.lib_type == STATIC:
            PROJECT['compiler'].archive(
                output=output_path,
                input_files=list(self.sources),
                options=self.c_args + [lflag for lflags in self.link_args for lflag in lflags.split()]
            )
        elif self.lib_type == SHARED:
            self.lflags.append('-shared')
            PROJECT['compiler'].link(
                output=output_path,
                input_files=list(self.sources),
                l_flags=self.c_args + [lflag for lflags in self.link_args for lflag in lflags.split()]
            )

        return self


class Package:
    def __init__(self, 
            name: str,
            *libraries: Library,
            target: Target = NATIVE,
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

        if not isinstance(target, Target):
            raise TypeError('target must be an instance of Target')

        self.triplet = target

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