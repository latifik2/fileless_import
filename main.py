import requests
from zipfile import ZipFile
from io import BytesIO
import sys
import imp
from pprint import pprint

url = "http://192.168.222.129:8000/colorama.zip"

r = requests.get(url)
zip_bytes = BytesIO(r.content)
zip_file = ZipFile(zip_bytes)
test = []
# print(requests.__path__)
# print(requests.__package__)
# for module in sys.modules:
#     test.append(module)
# pprint(sorted(test))

# try:
#     print(zip_file.getinfo("requests/123.py"))
# except:
#     print("TEST")

class MyImporter():

    def __init__(self):
        self.parts = None
        self.fs_path = None
        self.path = None
        self.submodule = None
        self.is_package = None

    def find_module(self, fullname, path=None):
        self.parts = fullname.split('.')
        self.path = '/'.join(self.parts)
        self.submodule = self.parts[-1]

        for suffix, is_package in (('.py', False), ('/__init__.py', True)):
            self.fs_path = self.path + suffix
            try:
                zip_file.getinfo(self.fs_path)
                print(f"Success! Entry {self.fs_path} was found")
                self.is_package = is_package
                return self
            except:
                print(f"Warn! No entry found in zip with name {self.fs_path}")
                continue
        return None
    
    def load_module(self, fullname):
        source_code = self.__get_code()
        module = sys.modules.setdefault(fullname, imp.new_module(fullname))
        module.__file__ = "<%s>" % self.__class__.__name__
        module.__loader__ = self

        if self.is_package:
            module.__path__ = []
            module.__package__ = fullname
        else:
            module.__package__ = fullname.rpartition('.')[0]

        exec(source_code, module.__dict__)
        return module

    def __get_code(self):
        return zip_file.read(self.fs_path).decode()


my_imp = MyImporter()
my_imp.find_module("colorama")
print(my_imp.load_module("colorama"))

sys.meta_path.append(my_imp)

# import colorama