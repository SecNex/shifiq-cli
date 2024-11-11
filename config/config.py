import configparser
import json

from rich.console import Console
from rich.table import Table

console = Console()

class Configuration:
    def __init__(self, path: str) -> None:
        self.path = path

    def __read(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config.read(self.path)
        return config
    
    def list_sections(self) -> list:
        __config = self.__read()
        return __config.sections()
    
    def get_section(self, section: str) -> dict:
        __config = self.__read()
        return dict(__config[section])
    
    def add_section(self, section: str) -> None:
        __config = self.__read()
        __config.add_section(section)
        self.__save()

    def present_section(self, section: str) -> bool:
        __config = self.__read()
        return __config.has_section(section)
    
    def get(self, section: str, key: str) -> str:
        __config = self.__read()
        return __config[section][key]
    
    def set(self, section: str, key: str, value: str) -> None:
        __config = self.__read()
        __config[section][key] = value
        self.__save()
    
    def remove(self, section: str, key: str ) -> None:
        __config = self.__read()
        __config.remove_option(section, key)
        self.__save()

    def present(self, section: str, key: str) -> bool:
        __config = self.__read()
        return __config.has_option(section, key)
    
    def present_keys(self, section: str, keys: list) -> bool:
        __config = self.__read()
        for key in keys:
            if not __config.has_option(section, key):
                return False
        return True

    def __save(self) -> None:
        with open(self.path, "w") as file:
            self.config.write(file)
    
class Items:
    def __init__(self, path: str) -> None:
        self.path = path
        self.items = self.__read()
        self.de = self.items["de"]
        self.en = self.items["en"]
        self.de_len = len(self.de)
        self.en_len = len(self.en)
    
    def __read(self) -> dict:
        with open(self.path, "r") as file:
            return json.load(file)
        
    def generate(self) -> None:
        with open(self.path, "w") as file:
            json.dump({
                "de": [],
                "en": []
            }, file)
    
    def get(self, language: str) -> list:
        __items = self.__read()
        return __items[language]
    
    def add(self, language: str, title: str, link: str, type: str, position: int = 0) -> dict:
        item = {
            "title": title,
            "link": link,
            "type": type
        }
        __items = self.__read()

        if language not in __items:
            __items[language] = []
    
        if position > 0:
            __items[language].insert(position - 1, item)
        else:
            __items[language].append(item)

        with open(self.path, "w") as file:
            json.dump(__items, file)

        item["language"] = language
        return item

    def remove(self, language: str, id: int) -> None:
        __items = self.__read()
        if 0 < id <= len(__items[language]) + 1:
            __items[language].pop(id - 1)
            with open(self.path, "w") as file:
                json.dump(__items, file)
        else:
            console.print(f"❌ Invalid ID: {id}.", style="red")

    def edit(self, id: int, language: str, title: str = None, link: str = None, type: str = None) -> None:
        __items = self.__read()
        __new = __items[language][id - 1]
        if title is not None:
            __new["title"] = title
        if link is not None:
            __new["link"] = link
        if type is not None:
            __new["type"] = type
        __items[language][id - 1] = __new
        with open(self.path, "w") as file:
            json.dump(__items, file)
        table = Table()
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Link", style="green")
        table.add_column("Type", style="yellow")
        table.add_row(str(id), __new["title"], __new["link"], __new["type"])

        console.print(table)
        print()

    def clear(self) -> None:
        __items = self.__read()
        __items = {
            "de": [],
            "en": []
        }
        with open(self.path, "w") as file:
            json.dump(__items, file)

if __name__ == "__main__":
    config = Configuration("config/edgesight.conf")
    for section in config.list_sections():
        for key, value in config.get_section(section).items():
            print(f"[{section}] {key}: {value}")