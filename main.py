import toml
import requests
import asyncio
# from time import sleep


def get_toml_data(file_path) -> dict:
    try:
        # Load TOML file
        with open(file_path, 'r') as file:
            toml_data = toml.load(file)

            return toml_data

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")


class DnsList:

    def get_white_list(self):
        with open(self.path_to_whitelist, 'r') as file_reader:
            self.white_list = file_reader.read()

    def get_toml_data(self, file_path) -> dict:
        try:
            # Load TOML file
            with open(file_path, 'r') as file:
                toml_data = toml.load(file)

                return toml_data

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"Error: {e}")

    def no_dupes(self, list1: list) -> list:
        set_1 = set(list1)
        list_no_dupes = [item for item in self.full_list if item not in set_1]
        return list(list_no_dupes)

    def join_lists(self, list1: list, list2: list) -> list:
        no_dupes_list = self.no_dupes(list2)
        return list(set(list1).union(set(no_dupes_list)))

    def has_hash(self, item):
        return isinstance(item, str) and item.startswith("#")

    def whitelist_filter(self, item):
        return any(word in item for word in self.white_list)

    def filter_condition(self, item):
        return not (self.has_hash(item) or self.whitelist_filter(item))

    def filter_list(self, list1):
        return list(filter(self.filter_condition, list1))

    async def async_requests_get(self, url: str) -> list:
        r = requests.get(url)
        if r.status_code == 200:
            list_response = r.text.split('\n')
            return list_response
        else:
            return []

    async def print_to_file(self, section: str, values: dict) -> bool:
        print(f"Section: {section}")
        list_name = f"sorted_list_{section}.txt"
        self.section_list = []
        self.full_list_dict[section] = []
        with open(list_name, 'w+') as file:
            for key, value in values.items():
                print(f"Section: {section} | URL: {value}")
                new_list = await self.async_requests_get(value)
                joined_list = self.join_lists(
                    self.section_list,
                    new_list)
                self.section_list = self.filter_list(joined_list)
            self.full_list.extend(self.section_list)
            file.writelines(map(lambda x: x + '\n', self.section_list))
        return True

    async def do_the_loop(self) -> bool:
        print("Starting loop")
        # Iterate through the TOML data
        tasks = [self.print_to_file(
            section,
            values) for section, values in self.toml_data.items()]
        print("Waiting for the loop to finish")
        await asyncio.gather(*tasks)
        print("Finished!")
        return True

    def __init__(self, path_to_file: str, path_to_whitelist: str):
        self.full_list_dict = {}
        self.path_to_file = path_to_file
        self.path_to_whitelist = path_to_whitelist
        self.toml_data = self.get_toml_data(self.path_to_file)
        self.full_list = []


if __name__ == "__main__":
    dns_lister = DnsList("raw_lists.toml", "whitelist.txt")
    asyncio.run(dns_lister.do_the_loop())
    #finish_check = dns_lister.do_the_loop()
