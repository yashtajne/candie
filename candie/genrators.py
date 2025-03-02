import os

from pathlib import Path


from . import STATIC, SHARED, PROJECT, CACHE_DIR, LOCAL_INSTALL_DIR
from .utils import Get_Logs, Update_Logs, HEX_Encode, HEX_Decode, Generate_Library_Name, Generate_PkgConfig_File, Copy_Files



class Executable:
    def __init__(self,
            name: str, 
            *sources: str, 
            dependencies: list[dict] = [], 
            c_args: list[str] = [],
            link_args: list[str] = [],
            make_out_dir: str = '.',
        ):
        self.name = name
        self.sources = {str(Path(src).resolve()) for src in sources}

        self.cflags: set[str] = set(c_args)
        self.lflags: set[str] = set(link_args)

        for dependency in dependencies:
            self.link_against(dependency)

        self.make_out_dir = make_out_dir if os.path.isdir(make_out_dir) else None

        self.__make()

    def set_cflags(self, *cflags: str):
        self.cflags.update(cflags)
        return self

    def set_lflags(self, *lflags: str):
        self.lflags.update(lflags)
        return self
    
    def add_source(self, *source: str):
        self.sources += source
        return self
    
    def link_against(self, dependency: dict):
        if dependency:
            self.cflags.add(dependency.get('cflags', ''))
            self.lflags.add(dependency.get('libs', ''))
        else:
            print("Error: invalid dependency")
        return self

    def __make(self):
        input_files = []
        for source in self.sources:
            if not os.path.isfile(source):
                print(f"Error: {source} does not exist")
                continue
            PROJECT['compiler'].compile(
                output=(cached_filename := f"{CACHE_DIR}/{HEX_Encode(os.path.abspath(source))}.o"),
                input_file=source,
                c_flags=list(self.cflags)
            )
            if os.path.isfile(cached_filename):
                input_files.append(cached_filename)
        PROJECT['compiler'].link(
            output=f"{self.make_out_dir}/{self.name}",
            input_files=input_files,
            l_flags=[lflag for lflags in self.lflags for lflag in lflags.split()]
        )


class Library:
    def __init__(self, 
            name: str, 
            lib_type: str, 
            *sources: str, 
            make_out_dir: str = '.', 
            build_out_dir: str = '.'
        ):
        self.name = name
        self.sources = sources

        self.lib_type = STATIC if lib_type not in [STATIC, SHARED] else lib_type

        self.make_out_dir = make_out_dir
        self.build_out_dir = build_out_dir

        self.requirements: list[str] = list()

        self.cflags: set[str] = set()
        self.lflags: set[str] = set()

    def set_cflags(self, *cflags: str):
        self.cflags.update(cflags)
        return self

    def set_lflags(self, *lflags: str):
        self.lflags.update(lflags)
        return self
    
    def add_source(self, *source: str):
        self.sources += source
        return self
    
    def link_against(self, dependency: dict):
        if dependency:
            self.requirements.append(dependency.get('name', ''))
            self.cflags.add(dependency.get('cflags', ''))
            self.lflags.add(dependency.get('libs', ''))
        else:
            print("Error: invalid dependency")
        return self
    
    def make(self):
        output_path = f"{self.make_out_dir}/{Generate_Library_Name(self.name, self.lib_type)}"
        input_files = []
        for source in self.sources:
            PROJECT['compiler'].compile(
                output=(cached_filename := f"{CACHE_DIR}/{HEX_Encode(os.path.abspath(source))}.o"),
                input_file=source,
                c_flags=list(self.cflags)
            )
            if os.path.isfile(cached_filename):
                input_files.append(cached_filename)

            # print({
            #     "source": source,
            #     "cache": cached_filename
            # })
        
        if self.lib_type == STATIC:
            PROJECT['compiler'].archive(
                output=output_path,
                input_files=input_files
            )
        elif self.lib_type == SHARED:
            self.lflags.add('-shared')
            PROJECT['compiler'].link(
                output=output_path,
                input_files=input_files,
                l_flags=list(self.lflags)
            )


class Package:
    def __init__(self, name: str, *libraries: Library, install_dir: str = LOCAL_INSTALL_DIR):
        self.name = name
        self.description = ''
        self.version = '0.0.0'
        self.url = ''

        if not os.path.isdir(install_dir):
            os.makedirs(install_dir)

        self.install_dir = install_dir
        self.libraries = libraries
    
    def install_headers(self, *headers: str):
        Copy_Files(headers, f"{self.install_dir}/include")
        return self

    def make(self):
        pkgconfig_dir = f"{self.install_dir}/lib/pkgconfig"
        if not os.path.isdir(pkgconfig_dir):
            os.makedirs(pkgconfig_dir)

        for library in self.libraries:
            # print(library)
            library.make_out_dir = f"{self.install_dir}/lib"
            library.make()
        
        with open(os.path.join(pkgconfig_dir, self.name + '.pc'), 'w') as dotpcfile:
            dotpcfile.write(Generate_PkgConfig_File(
                name=self.name,
                description=self.description,
                version=self.version,
                url=self.url,
                requires=[req for lib in self.libraries for req in lib.requirements],
                cflags=[],
                libs=[('-l' + lib.name) for lib in self.libraries]
            ))