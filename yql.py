#!/usr/bin/env python3

import requests
import json
import random


class YQL:
    yql_url = 'http://query.yahooapis.com/v1/public/yql'
    yql_debug = True
    yql_diagnostics = True
    yql_table_uri = 'https://raw.githubusercontent.com/jabemp/yql/main/tables'
    yql_cache_buster = True

    def prepare_yql_statement(self, custom_table_name, criteria):

        full_table_uri = '{}/{}'.format(self.yql_table_uri, custom_table_name)

        if self.yql_cache_buster:
            full_table_uri += '?t={}'.format(random.randrange(1, 65535, 1))

        where_clause = ' where {}'.format(criteria) if criteria else ''
        statement = 'use \'{}\' as index; select * from index{}'.format(full_table_uri, where_clause)
        return statement

    def run_yql_statement(self, query):

        query_string = {
            'q': query,
            'debug': str(self.yql_debug).lower(),
            'diagnostics': str(self.yql_diagnostics).lower(),
            'format': 'json'}

        print('Querying url: {}'.format(self.yql_url))
        print('With params: {}'.format(query_string))
        result = requests.get(self.yql_url, params=query_string)
        print('HTTP: {}'.format(result.status_code))
        print('Response body:')
        print(json.dumps(result.json()))
        return result.json()


def main():
    y = YQL()
    query = y.prepare_yql_statement('<tablename>.xml', 'date = "<yy.mm.dd>"')
    y.run_yql_statement(query)


if __name__ == "__main__":
    main()
