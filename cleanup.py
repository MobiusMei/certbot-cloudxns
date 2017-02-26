#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import json
import sys
from cloudxns.api import *

if __name__ == '__main__':
    print 'CloudXNS API Version: ', Api.vsersion()
    api_key = os.environ['API_KEY']
    secret_key = os.environ['SECRET_KEY']
    CERTBOT_DOMAIN = os.environ['CERTBOT_DOMAIN']
    CERTBOT_VALIDATION = os.environ['CERTBOT_VALIDATION']
    api = Api(api_key=api_key, secret_key=secret_key)

    # api.set_debug(True)

    """
    功能 域名列表
    HTTP 请求方式 GET
    URL https://www.cloudxns.net/api2/domain
    :return: String
    """
    result = json.loads(api.domain_list())

    domain_id = None
    host_name = None
    for item in result['data']:
        suffix = item['domain'].rstrip('.')
        if ('.' + CERTBOT_DOMAIN).endswith('.' + suffix):
            domain_id = item['id']
            host_name = ('_acme-challenge.' + CERTBOT_DOMAIN[0:len(CERTBOT_DOMAIN) - len(suffix)]).rstrip('.')

            print 'Domain ID:', domain_id
            print 'Host Name:', host_name

    """
    功能 记录类型列表 
    HTTP 请求方式 GET
    URL https://www.cloudxns.net/api2/type
    :return: String
    """
    result = json.loads(api.record_list(domain_id))

    record_id = None
    for item in result['data']:
        if item['type'] == 'TXT' and item['host'] == host_name:
            record_id = item['id']

    if record_id:
        """
        功能 删除解析记录
        HTTP 请求方式 DELETE
        URL https://www.cloudxns.net/api2/record/:id/:domain_id
            请求参数：
                参数名称 类型 必填 描述
                record_id Integer 解析记录id
                domain_id Integer  域名 id
            :return: String
        """
        result = api.record_delete(record_id, domain_id)
        print result

