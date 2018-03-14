import requests

with open('keywords.tuga.txt', mode='r') as f:
    for line in f.readlines():
        offset = 0
        print('Query Keyword: {}'.format(line.strip()))
        while offset <= 2000:  # it should be total_items
            # query TextSearchAPI
            r = requests.get('http://arquivo.pt/textsearch?q={}&itemsPerSite=1&offset={}'.format(line.strip(), offset))
            content = r.json()
            total_items = content['total_items']
            number_of_items = len(content['response_items'])

            print('Fetching URLs within offset {}-{}...'.format(offset, offset + 50))
            for item in content['response_items']:
                with open('urls.tuga.txt', mode='a') as output:
                    output.writelines(item['linkToNoFrame'] + '\n')

            if number_of_items != 50:
                break

            offset += 50
