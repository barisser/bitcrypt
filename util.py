import hashlib
import base58
import pybitcointools

b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

# Hash pairs of items recursively until a single value is obtained
def merkle(hashList):
    if len(hashList) == 1:
        return hashList[0]
    newHashList = []
    # Process pairs. For odd length, the last is skipped
    for i in range(0, len(hashList)-1, 2):
        newHashList.append(hash2(hashList[i], hashList[i+1]))
    if len(hashList) % 2 == 1: # odd, hash last item twice
        newHashList.append(hash2(hashList[-1], hashList[-1]))
    return merkle(newHashList)

def hash2(a, b):
    # Reverse inputs before and after hashing
    # due to big-endian / little-endian nonsense
    a1 = a.decode('hex')[::-1]
    b1 = b.decode('hex')[::-1]
    h = hashlib.sha256(hashlib.sha256(a1+b1).digest()).digest()
    return h[::-1].encode('hex')

def ripehash(hexstring):
    a=hexstring.decode('hex')
    b=hashlib.sha256(a).hexdigest()
    c=b.decode('hex')
    m=hashlib.new('ripemd160')
    m.update(c)
    return m.hexdigest()

def script_to_pubkey(script):
    #ASSUMING ITS PAY TO PUBKEY HASH SCRIPT
    return script[len(script)-130:len(script)]

def script_to_destination_address(script):
    return pybitcointools.pubkey_to_address(script_to_pubkey(script))

def base58encode(hex_payload): #not assuming using '0', should be included in payload
  return base58.b58encode(hex_payload.decode('hex'))
