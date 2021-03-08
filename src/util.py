import h5py
import json
import tensorflow as tf
from types import SimpleNamespace
import numpy as np
import random
import os, sys
import logging

log = logging.getLogger(__name__)
def save_file(fpath, txt):
    with open(fpath, 'w') as f:
        log.info(f"Saving {txt} to : {fpath}")
        f.write(txt)

def config_writer(fpath, obj):
    with open(fpath, 'w') as f:
        log.info(f"Saving configuration Config.py as json: outfile -> {fpath}.")
        json.dump(obj.__dict__, f)

def config_loader(fpath):
    with open(fpath, 'r') as f:
        return json.load(f, object_hook=lambda d: SimpleNamespace(**d))

def load_json(fpath):
    with open(fpath, 'r') as f:
        return json.load(f)

def latexify(s):
    return s.replace('_', '\_').replace('%', '\%')

def print_dct(dct):
    for k, v in dct.items():
        log.info(f"{latexify(k)} & {v} \\\\")

def inititialize_dirs(config):
    for directory in config.dirs:
        dir_path = os.path.join(sys.path[0], directory)
        if not os.path.exists(dir_path):
            log.info(f"Making dir {dir_path}")
            os.mkdir(dir_path)

def get_random_val(mode, val=None, std_dev=None, config=None, size=None):
    """Generates a uniformally distributed random variable, or a gaussian random variable centered at 0 by dafault.

    Args:
        mode (str): the random generation type
        val (float, optional): the bound for uniform number generation
        std_dev (float, optional): the standard devation for guassian function. Defaults to None.
        config (config.Config, optional): the configuration class for the training environment . Defaults to None.

    Returns:
        [type]: [description]
    """
    if mode == config.uniform:
        return np.random.uniform(-1*val, val)
    elif mode == config.normal:
        return np.random.normal(0, std_dev, size=size)
    