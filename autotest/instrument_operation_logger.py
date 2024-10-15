#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''程序

@description
    说明
'''
# import logging


import logging
import time
# from logging.handlers import FileHandler
from logging import FileHandler


class InstrumentOperationLogger():
    def __init__(self, module_name_log):
        # 先初始化日志记录器
        self.logger = logging.getLogger(f'{module_name_log}')
        self.logger.setLevel(logging.INFO)
        log_file = f'{module_name_log}.log'

        file_handler = FileHandler(log_file, mode='a', encoding=None, delay=False)
        file_handler.setLevel(logging.INFO)

        # 定义日志格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # 将处理器添加到logger中
        self.logger.addHandler(file_handler)

        # 添加处理器到记录器
        self.logger.addHandler(file_handler)

        self.log_time()

    def log_time(self):
        current_time = time.localtime()

        # 格式化为 YYYY-MM-DD
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
        self.logger.info(formatted_time)

    def log_command(self, command):
        self.logger.info(command)

    def log_error(self, message):
        self.logger.error(message)
