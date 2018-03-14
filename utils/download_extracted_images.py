import argparse
import hashlib
import os

import requests

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file", help="Path to the images file list to download.")
    parser.add_argument("output_folder", help="Path to location where the images will be stored.")

    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        for line in file.readlines()[88544:]: # start at 1141 to resume, remove this after
            try:
                url = line.strip()

                dirname = args.output_folder

                if not os.path.isdir(dirname):
                    os.mkdir(dirname)

                try:
                    print('Downloading {}'.format(url))
                    r = requests.get(url)
                    response_main_type, sub_type = r.headers['Content-Type'].split('/')
                    response_sub_type = sub_type.split(';')[0]

                    if r.status_code == 200 and response_main_type == 'image':
                        image_data = requests.get(url).content
                        digest = hashlib.md5(image_data).hexdigest()
                        file_name = os.path.join(dirname, digest)
                        with open(file_name + "." + response_sub_type, 'wb') as output_file:
                            output_file.write(image_data)
                        with open('urls_digest_dic.txt', mode='a') as output_dic:
                            output_dic.writelines('{} {}'.format(digest, url))
                except OSError as error:
                    print(url, error)
                except KeyError as error:
                    print(url, error)
            except ValueError as error:
                print(line, error)
