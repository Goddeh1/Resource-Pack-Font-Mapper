import os
import json
import shutil

def retrieve_png_files(folder):
    png_files = [f for f in os.listdir(folder) if f.endswith('.png')]
    return sorted(png_files, key=lambda x: int(os.path.splitext(x)[0]))

def generate_json(file_path, png_files):
    json_data = {
        "providers": []
    }
    char_code = 0x1000
    for png_file in png_files:
        if char_code > 0x1FFF:
            print("Error: Unicode character range exceeded.") #temporary solution but probs not good for scalability
            return
        json_data["providers"].append({
            "type": "bitmap",
            "file": f"{file_path}/{png_file}".replace("\\", "/"),
            "chars": [chr(char_code)],
            "ascent": 121,  # cba
            "height": 128   # cba
        })
        char_code += 1
    output_filename = os.path.basename(os.path.normpath(file_path))
    output_folder = f"exports/{output_filename}"
    os.makedirs(output_folder, exist_ok=True)
    with open(f"{output_folder}/{output_filename}.json", "w") as json_file:
        json.dump(json_data, json_file, indent=2)
    for png_file in png_files:
        src_file = os.path.join("import", png_file)
        dst_file = os.path.join(output_folder, png_file)
        shutil.move(src_file, dst_file)

def main():
    folder = "import"
    png_files = retrieve_png_files(folder)
    file_path = input("Resource pack file path pls: ")

    generate_json(file_path, png_files)

if __name__ == "__main__":
    main()
