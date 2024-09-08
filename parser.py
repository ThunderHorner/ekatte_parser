import os
import json


def read_first_line(file_path):
    with open(file_path) as f:
        return f.readline().strip()


def process_directory(base_dir):
    data = {}
    for region in sorted(os.listdir(base_dir)):
        region_dir = os.path.join(base_dir, region)
        region_file = os.path.join(region_dir, 'oblast.txt')

        if not os.path.isdir(region_dir) or not os.path.exists(region_file):
            continue

        region_name = read_first_line(region_file).split(',')[2]

        for municipality in sorted(os.listdir(region_dir)):
            muni_dir = os.path.join(region_dir, municipality)
            muni_file = os.path.join(muni_dir, 'obshtina.txt')

            if not os.path.isdir(muni_dir) or not os.path.exists(muni_file):
                continue

            muni_name = read_first_line(muni_file).split(',')[2]

            for settlement_file in sorted(os.listdir(muni_dir)):
                if settlement_file.endswith('.txt') and settlement_file != 'obshtina.txt':
                    settlement_path = os.path.join(muni_dir, settlement_file)
                    settlement_name = read_first_line(settlement_path).split(',')[0]
                    data.setdefault(region_name, {}).setdefault(muni_name, []).append(settlement_name)

    return data


if __name__ == '__main__':
    result = process_directory('ekatte_db')
    with open('data.json', 'w', encoding='utf-8') as f:
        # json dump is used here for memory efficiency user iterencode instead of encode
        json.dump(result, f, ensure_ascii=False, indent=4)
