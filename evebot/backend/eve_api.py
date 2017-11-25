#!/usr/bin/python3

from evebot import config
import requests


class EveAPI(object):

    def __init__(self,
        baseurl,
        args = None):
        self.base_url = baseurl
        self._args = {}
        self.args = args
        self.content = None
        self.result = None
        self.json = None

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        if not args:
            self._args = {}
            self._args['datasource'] = 'tranquility'
        elif 'datasource' not in args:
            self._args['datasource'] = 'tranquility'
            self._args.update(args)
        else:
            self._args.update(args)

    def try_request(self, resource):
        url = self.base_url
        url += '/%s' % resource
        arg_list = []
        for k, v in self.args.items():
            arg = '%s=%s' % (k, v)
            arg_list.append(arg)
        url += '?%s' %('&'.join(arg_list))
        self.url = url
        self.result = requests.get(url)
        #do some checking on the responce code
        self.json = self.result.json()
        return self.json

    def getall(self, resource):
        results = []
        while True:
            current_page = self.args.get('page')
            if current_page:
                next_page = current_page +=1
                self.args{'page': next_page}
            page_content = self.try_request(resource)
            if page_content:
                results.extend(page_content)
            else:
                break
        return results

    #do we want an iter?