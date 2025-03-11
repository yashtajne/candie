import os
import subprocess
import threading


from .printer import console

class ZigToolchain:
    def __init__(self, language: str, cache_dir: str):
        self.compiler = self.__get_compiler(language)
        self.cache_dir = cache_dir

        os.environ['ZIG_LOCAL_CACHE_DIR'] = self.cache_dir

    def compile(self,
            output: str,
            input_file: str,
            c_flags: list[str] = [],
        ) -> threading.Thread:
        if not input_file:
            print("Fatal Error: No input file")
            raise SystemExit
        compile_cmd = (['zig', self.__get_compiler(os.path.splitext(input_file)[1])] + c_flags + ['-o', output, '-c'] + [input_file])
        console.print('[ Compiling ]', os.path.basename(input_file))
        # console.print('[ command ]', ' '.join(compile_cmd))
        return threading.Thread(target=self.__rc, args=(compile_cmd,))

    def link(self,
            output: str,
            input_files: list[str],
            l_flags: list[str] = []
        ) -> None:
        if not input_files:
            print("Fatal Error: No input files")
            raise SystemExit
        link_cmd = (['zig', self.compiler] + input_files + l_flags + ['-o', output])
        console.print('[ Linking ]', len(input_files), 'files')
        # console.print('[ command ]', ' '.join(link_cmd))
        self.__rc(link_cmd)

    def archive(self,
            output: str,
            input_files: list[str],
            options: list[str]
        ) -> None:
        if not input_files:
            print("Fatal Error: No input files")
            raise SystemExit
        archive_cmd = (['zig', 'build-lib', '-lc', '-lstdc++'] + input_files + options + ['-femit-bin=' + output])
        console.print('[ Archiving ]', os.path.basename(output))
        # console.print('[ command ]', ' '.join(archive_cmd))
        self.__rc(archive_cmd)

    def __rc(self, cmd) -> None:
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            console.print("Error:", e.stderr.decode())

    def __get_compiler(self, determiner: str) -> str:
        return 'cc' if determiner == '.c' else 'c++'