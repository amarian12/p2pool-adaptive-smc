from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
    smartcoin=math.Object(
        PARENT=networks.nets['smartcoin'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//15, # shares
        REAL_CHAIN_LENGTH=24*60*60//15, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=5, # blocks
        IDENTIFIER='defadefaced0ced0'.decode('hex'),
        PREFIX='d0cededefafac0ce'.decode('hex'),
        P2P_PORT=29983,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=8960,
        BOOTSTRAP_ADDRS=''.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-alt',
	VERSION_CHECK=lambda v: v >= 90000,
    ),
    globalboosty=math.Object(
        PARENT=networks.nets['globalboosty'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//15, # shares
        REAL_CHAIN_LENGTH=24*60*60//15, # shares
        TARGET_LOOKBEHIND=60, # shares
        SPREAD=3, # blocks
        IDENTIFIER='cf90e29bc82c60e7'.decode('hex'),
        PREFIX='ee87ca7f6c700ee8'.decode('hex'),
        P2P_PORT=39962,
        MIN_TARGET=0,
        MAX_TARGET=2**256//10000 - 1,
        PERSIST=False,
        WORKER_PORT=8966,
        BOOTSTRAP_ADDRS='bsty.altmine.net:7226 stratum-eu.altmine.net:7226 litecoin-p2pool.com:7226'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-bsty',
        VERSION_CHECK=lambda v: True,
    ),

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
