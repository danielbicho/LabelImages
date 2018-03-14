import json
import os

import requests


class LabelWriter:
    def __init__(self, file_path='data/classification.txt'):
        self.file_path = file_path

    def write(self, url, classification):
        with open(self.file_path, mode='a') as writer:
            writer.write("{} {}\n".format(url, classification))


class ImageReader:
    def process(self):
        raise NotImplementedError("Should have implemented this")

    def next(self):
        raise NotImplementedError("Should have implemented this")


class ImageReaderFileSystem(ImageReader):
    def __init__(self, input_path='/home/dbicho/output'):
        self.input_path = input_path
        self.images = self.process()

    def process(self):
        file_list = []
        for file in os.listdir(self.input_path):
            file_list.append('file://' + os.path.join(self.input_path, file))
        return file_list

    def next(self):
        if self.images:
            return self.images.pop()
        else:
            return None


class ImageReaderSolr(ImageReader):
    """
        query examples  =   imgSrc:*<keywords>*
                            imgAlt:*<keywords>*
    """

    def __init__(self, solr_collection='http://p28.arquivo.pt:8983/solr/Europe', query='*:*', start_number=0):
        self.solr_collection = solr_collection
        self.query = query
        self.parameters = 'fl=imgWidth,mimeType,imgHeight,digest,imgSrc,timestamp,collection&group.field=digest&group=true&rows=1000'

        self.solr_full_query = "{}/select?q={}&{}".format(self.solr_collection, self.query, self.parameters)
        self.start_number = start_number
        self.total_number = 0
        self.digest_set = set()
        self.images = self.process()

    def process(self):
        r = requests.get(self.solr_full_query + '&start=' + str(self.start_number))
        content = r.json()
        result_list = []

        self.total_number = content['grouped']['digest']['matches']

        if content.get('error', None):
            return None
        else:
            for group in content['grouped']['digest']['groups']:
                if group['doclist']['docs'][0]['digest'] not in self.digest_set:
                    if group['doclist']['docs'][0]['imgWidth'] > 150 and group['doclist']['docs'][0]['imgHeight'] > 150:
                        ra = requests.get(
                            "http://arquivo.pt/wayback/{}/{}".format(group['doclist']['docs'][0]['timestamp'],
                                                                     group['doclist']['docs'][0]['imgSrc']))

                        if ra.status_code == 200:
                            self.digest_set.add(group['doclist']['docs'][0]['digest'])
                            result_list.append(
                                "http://arquivo.pt/wayback/{}/{}".format(group['doclist']['docs'][0]['timestamp'],
                                                                         group['doclist']['docs'][0]['imgSrc']))
        return result_list

    def next(self):
        if self.images:
            return self.images.pop()
        else:
            self.start_number += 1000
            self.images = self.process()
            if self.images:
                return self.images.pop()
            else:
                return None


# class ImageReaderTextAPI(ImageReader):
#     def __init__(self, api_endpoint='http://arquivo.pt/textsearch', query='*:*', offset=0):
#         self.api_endpoint = api_endpoint
#         self.query = query
#         self.parameters = ""
#         self.offset = offset
#         self.total_number = 2000  # hardcoded because arquivo.pt limitations, open issue
#         self.digest_set = set()
#         self.images = self.process()
#
#     def process(self):
#         r = requests.get("{}?{}&{}".format(self.api_endpoint, self.query, self.parameters))
#         content = r.json()
#         result_list = []
#
#     def next(self):
#         pass


# TODO generators cannot be persisted with pickle, how to use it in the webapp labeling logic?
class ImageReaderCDX(ImageReader):
    def __init__(self, cdx_path='data/EAWP9.cdxj'):
        self.cdx_path = cdx_path
        self.images = self.process()

    def process(self):
        with open(self.cdx_path, mode='r') as f:
            for line in f.readlines():
                cdx_record = json.loads(line[line.find('{"url'):])
                meta_record = line[:line.find('{"url')]
                timestamp = meta_record.split(' ')[1]
                mime = cdx_record["mime"]
                status = cdx_record["status"]
                if mime.split('/')[0] == 'image':
                    result = "http://arquivo.pt/wayback/{}/{} {} {}".format(timestamp, cdx_record['url'],
                                                                            cdx_record['length'],
                                                                            cdx_record['digest'])
                    yield result

    def next(self):
        for image in self.images:
            return image
