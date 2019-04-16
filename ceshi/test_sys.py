# -*- coding:utf-8 -*-
import argparse
import sys
import yaml
import configparser

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-fna', '--filename-arguments', type=yaml.load)
    data = "{location: warehouse A, site: Gloucester Business Village}"
    ans = parser.parse_args()
    if ans.fna is not None:

    print( ans.filename_arguments['site'])
    # if len(sys.argv) != 2:
    #     print("kkk")
    # else:
    #     with open(sys.argv[1],'r') as ymfile:
    #         cfg = ymfile.read()
    #     with open('config.ini','w') as content:
    #         content.write(cfg)
    #     cf = configparser.ConfigParser()
    #     cf.read('config.ini')
    #     secs = cf.sections()
    #     print(cf.items('db'))





