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
    功能 获取解析记录列表
    HTTP 请求方式 GET
    URL https://www.cloudxns.net/api2/record/:domain_id?host_id=0&offset=:offset&row_num=:row_num
    URL 参数说明
        domain_id:域名 id
        host_id:主机记录 id(传 0 查全部)
        offset:记录开始的偏移，第一条记录为 0，依次类推,默认取 0
        row_num:要获取的记录的数量， 比如获取 30 条， 则为 30,最大可取 2000
        条,默认取 30 条.
    :return:
        code int 请求状态，详见附件 code 对照表
        message String 操作信息，提示操作成功或错误信息
        total int 总记录条数
        offset int 记录开始的偏移
        row_num int 要获取的记录的数量
        data array 记录列表
            record_id: 解析记录 id
            host_id:主机记录 id
            host：主机记录名
            line_id：线路 ID
            line_zh：中文名称
            line_en：英文名称
            mx：优先级
            Value：记录值
            Type：记录类型
            Status：记录状态(ok 已生效 userstop 暂停)
            create_time：创建时间
            update_time：更新时间
    """
    result = json.loads(api.record_list(domain_id,0,0,2000))

    record_id = None
    for item in result['data']:
        if item['type'] == 'TXT' and item['host'] == host_name:
            record_id = item['record_id']

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

