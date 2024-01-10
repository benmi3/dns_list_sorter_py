import toml
import asyncio
import httpx
import time

import concurrent.futures

start_time = time.time()


class DnsList:

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

    def filter_urls(self, input_list):
        s = tuple(["#", "!", ":"])
        return list(filter(lambda x: not x.startswith(s) and x not in self.white_list + self.full_list, input_list))

    def filter_list(self, list1):
        return self.filter_urls(list1)

    async def get_list(self, client, url):
        r = await client.get(url)
        if r.status_code == 200:
            return r.text.split('\n')
        else:
            return []

    async def iterate_through_urls(self, section: str, values: dict) -> bool:
        async with httpx.AsyncClient() as client:
            tasks = []
            for _, url in values.items():
                print(f"Sendt Request to: {url}")
                tasks.append(asyncio.ensure_future(self.get_list(client, url)))

            new_list = await asyncio.gather(*tasks)
            self.full_list_dict[section] = new_list[0]
        return True

    async def actually_print(self):
        for key in self.full_list_dict.keys():
            list_name = f"sorted_list_{key}.txt"
            print(f"Sorting: {key}")
            self.section_list = self.filter_list(self.full_list_dict[key])
            self.full_list.extend(self.section_list)
            print(f"Now printing {key} to {list_name}")
            with open(list_name, 'w+') as file:
                file.writelines(map(lambda x: x + '\n', self.section_list))

    async def print_to_file(self, key: str) -> bool:
        list_name = f"sorted_list_{key}.txt"
        print(f"Sorting: {key}")
        self.full_list_dict[key] = self.filter_list(self.full_list_dict[key])
        self.full_list.extend(self.full_list_dict[key])
        print(f"Now printing {key} to {list_name}")
        with open(list_name, 'w+') as file:
            for item in self.full_list_dict[key]:
                file.write(str(item) + "\n")
            #file.writelines(map(lambda x: x + '\n', self.full_list_dict[key]))


    async def do_the_loop(self) -> bool:
        print("Starting loop")
        print("Iterate through toml data\nRequsting data from urls")
        tasks = []
        for section, values in self.toml_data.items():
            tasks.append(self.iterate_through_urls(section, values))
        print("Waiting for the loop to finish")
        await asyncio.gather(*tasks)
        print("Filter through lists\nPrinting the lists to files")
        #await self.actually_print()
        # #------------------------------------------------------
        prints = []
        for key in self.full_list_dict.keys():
            prints.append(self.print_to_file(key))

        await asyncio.gather(*prints)

        # #------------------------------------------------------
        print("Finished!")
        return True

    def __init__(self, path_to_file: str, path_to_whitelist: str):
        self.full_list_dict = {}
        self.path_to_file = path_to_file
        self.path_to_whitelist = path_to_whitelist
        self.toml_data = self.get_toml_data(self.path_to_file)
        self.full_list = []
        self.white_list = open(self.path_to_whitelist).read().split('\n')
        print(self.white_list)


if __name__ == "__main__":
    dns_lister = DnsList("raw_lists.toml", "white_list.txt")
    asyncio.run(dns_lister.do_the_loop())
    print(f"Time used to execute:\n{time.time() - start_time}")
