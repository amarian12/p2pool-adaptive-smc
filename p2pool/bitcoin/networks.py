import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

def get_boost_subsidy(height):
    if height < 17291:
        return 347 * 100000000
    halvings = height // 240000
    if halvings >= 64:
        return 0
    return (50 * 100000000) >> halvings

nets = dict(
    smartcoin=math.Object(
        P2P_PREFIX='defaced0'.decode('hex'), #pchmessagestart
        P2P_PORT=19983,
        ADDRESS_VERSION=63, #pubkey_address
        RPC_PORT=58583,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'smartcoin' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 16*100000000,
#        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('xcoin_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('xcoin_hash').getPoWHash(data)),
        BLOCK_PERIOD=120, # s
        SYMBOL='SMC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'smartcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/smartcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.smartcoin'), 'smartcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://lavastorm.net:2750/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://lavastorm.net:2750/address/',
        TX_EXPLORER_URL_PREFIX='http://lavastorm.net:2750/tx/',
#        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
	SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.0001e8,
    ),
    globalboosty=math.Object(
        P2P_PREFIX='a2b2e2f2'.decode('hex'),
        P2P_PORT=19962,
        ADDRESS_VERSION=77,
        RPC_PORT=8225,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'globalboostaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: get_boost_subsidy(height+1),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('yescrypt_hash').getHash(data, 80)),
        BLOCK_PERIOD=600, # s
        SYMBOL='BSTY',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'GlobalBoost-Y') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/GlobalBoost-Y/') if platform.system() == 'Darwin' else os.path.expanduser('~/.globalboosty'), 'globalboost.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://bsty.explorer.ssdpool.com:9095/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://bsty.explorer.ssdpool.com:9095/address/',
        TX_EXPLORER_URL_PREFIX='http://bsty.explorer.ssdpool.com:9095/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//10000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
