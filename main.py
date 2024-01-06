import toml
import request

def iterate_toml_file(file_path) -> dict:
    try:
        # Load TOML file
        with open(file_path, 'r') as file:
            toml_data = toml.load(file)

        # Iterate through the TOML data
        for section, values in toml_data.items():
            print(f"Section: {section}")
            for key, value in values.items():
                print(f"  {key}: {value}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")




def main():
    path_to_file = "raw_lists.toml"
    toml_data = get_toml_data(path_to_file)

    # Iterate through the TOML data
    for section, values in toml_data.items():
        print(f"Section: {section}")
        list_for_sorting = []
        for key, value in values.items():
            

        for key, value in values.items():
            print(f"  {key}: {value}")



# list of names
names = ['Jessa', 'Eric', 'Bob']

# open file in write mode
with open(r'/sales.txt', 'w') as fp:
    for item in names:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')
