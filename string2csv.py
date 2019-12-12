import os
import argparse
import re
import csv

# convert strings.xml to csv for android
def xml_2_csv(file_name):
    keys = []
    values = []

    lines = [line.rstrip('\n').strip() for line in open(file_name)]

    for line in lines:
        # Find key
        key = re.search(r'<string name=\"(.*?)\">', line)
        if key != None:
            standard = re.sub(' +', ' ', key.group(1))
            real_key = key.group(1).split(' ')[0].replace('\"', '')
            keys.append(real_key)

        # Find value
        value = re.search(r'\">(.*?)</string>', line)
        if value != None:
            values.append(value.group(1))

    print("keys length: ", len(keys))
    print("values length: ", len(values))

    data = []
    if len(keys) == len(values):
        for i in range(0, len(keys)):
            data.append([keys[i], values[i]])

    return data

# convert Localizable.strings to csv for ios
def strings_2_csv(file_name):
    keys = []
    values = []

    lines = [line.rstrip('\n').strip() for line in open(file_name)]
    for line in lines:
        # Find key
        key = re.search(r'\"(.*?)\"', line)
        if key != None:
            standard = re.sub(' +', ' ', key.group(1))
            real_key = key.group(1).split(' ')[0].replace('\"', '')
            keys.append(real_key)

        # Find value
        value = re.search(r'\=(.*?)\"\;', line)
        if value != None:
            standard = value.group(1).strip().strip('\"')
            real_value = re.sub(r'^"|"$', '', standard)
            values.append(real_value)

    print("keys length: ", len(keys))
    print("values length: ", len(values))

    data = []
    if len(keys) == len(values):
        for i in range(0, len(keys)):
            data.append([keys[i], values[i]])

    return data


def make_csv(file_name, data):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONE, quotechar='', escapechar='\\')
        writer.writerow(['Key', 'Value'])
        for item in data:
            writer.writerow(item)
    print('Done.\nFile ' + file_name + ' created.')


def get_string_files():
    files = []
    # r = root, d = directories, f = files
    for r, d, f in os.walk('./'):
        for file in f:
            if file.endswith('.strings') or file.endswith('.xml'):
                files.append(os.path.join(r, file))
    return files

def csv_from_android(file_name):
    data = xml_2_csv(file_name)
    make_csv(file_name[0:-4] + '.csv', data)

def csv_from_ios(file_name):
    data = strings_2_csv(file_name)
    make_csv(file_name[0:-8] + '.csv', data)

# Example:
#   python3 string2csv.py -f Localizable.strings
#   python3 string2csv.py -f strings.xml
#   python3 string2csv.py -f both

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--name", required=True, help="name of file with extension")
    args = vars(ap.parse_args())

    file_name = args['name']

    if file_name.endswith('.strings'):
        csv_from_ios(file_name)
    elif file_name.endswith('.xml'):
        csv_from_android(file_name)
    elif 'both' == file_name:
        files = get_string_files()
        for item in files:
            if item.endswith('.strings'):
                csv_from_ios(item)
            else:
                csv_from_android(item)
