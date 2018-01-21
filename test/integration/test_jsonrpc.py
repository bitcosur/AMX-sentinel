import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from amerod import AmeroDaemon
from amero_config import AmeroConfig


def test_amerod():
    config_text = AmeroConfig.slurp_config_file(config.amero_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000ffd590b1485b3caadc19b22e6379c733355108f107a430458cdf3407ab6' # TODO: update
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c' # TODO: udpate

    creds = AmeroConfig.get_rpc_creds(config_text, network)
    amerod = AmeroDaemon(**creds)
    assert amerod.rpc_command is not None

    assert hasattr(amerod, 'rpc_connection')

    # Amero testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c # TODO: update
    # test commands without arguments
    info = amerod.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert amerod.rpc_command('getblockhash', 0) == genesis_hash
