#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@todo:
    - theme_path in config file
"""

from __future__ import print_function, unicode_literals

import os
import sys
import shutil
import logging
from os import path as osp
from pprint import pprint

from simiki.configs import parse_configs
from simiki.log import logging_init
from simiki.utils import check_path_exists, copytree

class InitSite(object):

    def __init__(self, config_file):
        self.config_file = config_file
        if not check_path_exists(self.config_file):
            logging.error("{} not exists".format(self.config_file))
            sys.exit(1)
        self.configs = parse_configs(self.config_file)
        self.current_dir = os.getcwd()

    def get_conf(self):
        dst_config_file = osp.join(self.current_dir, "_config.yml")
        if check_path_exists(dst_config_file):
            logging.warning("{} already exists! if you want overwrite it, " \
                        "please remove it first".format(dst_config_file))
        try:
            shutil.copyfile(self.config_file, dst_config_file)
            logging.info("Creating config file: {}".format(dst_config_file))
        except (shutil.Error, IOError), e:
            logging.error(str(e))

    def install_theme(self):
        # TODO copy non-html files and directorys
        src_theme = osp.join(self.current_dir, "themes/{}/css".format(self.configs["theme"]))
        dst_theme = osp.join(self.current_dir, "output/css")
        if osp.exists(dst_theme):
            shutil.rmtree(dst_theme)

        copytree(src_theme, dst_theme)
        logging.info("Installing theme: {}".format(self.configs["theme"]))

    def init_site(self):
        content_path = osp.join(self.current_dir, self.configs["source"])
        output_path = osp.join(self.current_dir, self.configs["destination"])
        theme_path = osp.join(self.current_dir, "themes")
        for path in (content_path, output_path, theme_path):
            if osp.exists(path):
                logging.warning("{} exists".format(path))
            else:
                os.mkdir(path)
                logging.info("Creating directory: {}".format(path))

        src_theme = osp.join(os.path.dirname(__file__), "themes")
        if osp.exists(theme_path):
            shutil.rmtree(theme_path)

        copytree(src_theme, theme_path)
        logging.info("Copying themes: {}".format(theme_path))

        self.get_conf()
        self.install_theme()

if __name__ == "__main__":
    logging_init(logging.DEBUG)
    BASE_DIR = os.getcwd()
    if len(sys.argv) == 1:
        config_file = osp.join(BASE_DIR, "_config.yml")
    elif len(sys.argv) == 2:
        config_file = osp.join(BASE_DIR, sys.argv[1])
    else:
        logging.error("Usage: `python -m simiki.configs [config.yml]'")
        sys.exit(1)
        
    i = InitSite(config_file)
    i.init_site()
