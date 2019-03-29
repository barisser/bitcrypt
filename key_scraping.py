import requests
import json
import pybitcointools


def get_address_info_blockchaininfo(public_address):
    api_url = 'https://blockchain.info/address/'+str(public_address)+'?format=json'
    addressdata = requests.get(api_url).content
    addressdata = json.loads(addressdata)
    return addressdata


def get_txs_on_address(public_address):
    return get_address_info_blockchaininfo(public_address)['txs']


def get_txs_from_address(public_address):
    txs = get_txs_on_address(public_address)
    out_txs = []
    for tx in txs:
        for inp in tx['inputs']:
            if 'prev_out' in inp:
                if 'addr' in inp['prev_out']:
                    prev_addr = inp['prev_out']['addr']
                    if prev_addr == public_address:
                        out_txs.append(tx)
    return out_txs


def get_pubkey_on_address(public_address):  #only sometimes works
    try:
        txs = get_txs_from_address(public_address)
        found=False
        pubkey=''
        for tx in txs:
            if not found:
                for inp in tx['inputs']:
                    if 'script' in inp:
                        script = inp['script']
                        if len(script)>130:
                            potential_key = script[len(script)-130:len(script)]
                            hashed_key = pybitcointools.pubkey_to_address(potential_key)
                            if hashed_key == public_address:
                                found=True
                                pubkey=potential_key

                            potential_key2= script[len(script)-66:len(script)]
                            #print potential_key2
                            hashed_key2=pybitcointools.pubkey_to_address(potential_key2)
                            if hashed_key2 == public_address:
                                found=True
                                pubkey = potential_key2


        return pubkey, found
    except:
        print "cannot get pubkey on address"
        return '', False
