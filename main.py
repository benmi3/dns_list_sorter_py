import toml
import requests
from time import sleep

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


def file_write_filter(cur_section: str, cur_line: str) -> bool:
    if not cur_line.startswith("#"):
        print(f"section: {cur_section} \nLine: {cur_line}")
        list_name = f"sorted_list_{cur_section}.text"
        with open(list_name) as file_print:
            file_print.write(f"\n{cur_line}")
        return True
    else:
        return False


def main():

    path_to_file = "raw_lists.toml"
    toml_data = get_toml_data(path_to_file)
    white_list = ['google.com',]

    def filter_condition(item):
        return not (isinstance(item, str) and (item.startswith("#") or any(word in item for word in white_list)))

    # Iterate through the TOML data
    for section, values in toml_data.items():
        print(f"Section: {section}")
        list_name = f"sorted_list_{section}.txt"
        section_list = []
        with open(list_name, 'w+') as file:
            for key, value in values.items():
                r = requests.get(value)
                if r.status_code == 200:
                    print(r.status_code)
                    new_list = r.text.split('\n')
                    section_list = list(set(section_list).union(set(new_list)))
                    section_list = list(filter(filter_condition, section_list + new_list))
                else:
                    print(f"Failed to retrieve content. Status code: {r.status_code}")
            file.writelines(map(lambda x: x + '\n', section_list))



if __name__ == "__main__":
    main()
