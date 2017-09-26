# -*- coding: utf-8 -*-
# @Time : 2017/1/1 17:51
# @Author : woodenrobot


from scrapy import cmdline


if __name__ == '__main__':
    name = 'keyword'
    cmd = 'scrapy crawl {0} --output=keywod.csv'.format(name)
    cmdline.execute(cmd.split())

