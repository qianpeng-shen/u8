# -*- coding:utf-8 -*-
import os
import logging
import time
root_path = os.getcwd()
log_path = root_path + '/lov'
exist_file = os.path.exists(log_path)
if not exist_file:
    os.makedirs(log_path)
print(log_path)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
# log_path = os.path.dirname(os.getcwd()) + '\web_project/lo/'
log_path = log_path + '/'
print(log_path)
log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
