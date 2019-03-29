import pybitcointools
from Crypto.Cipher import AES
from Crypto import Random
import random
import base64
from pycoin import encoding
import key_scraping
import time
import util

p = 2**256 - 2**32 - 977
Gx=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
g= (Gx, Gy)

time_threshold=1000

def inverse(x, p):
    inv1 = 1
    inv2 = 0
    while p != 1 and p!=0:
        inv1, inv2 = inv2, inv1 - inv2 * (x / p)
        x, p = p, x % p

    return inv2

def dblpt(pt, p):
    if pt is None:
        return None
    (x, y)= pt
    if y==0:
        return None

    # Calculate 3*x^2/(2*y)  modulus p
    slope= 3*pow(x, 2, p)*inverse(2*y, p)

    xsum= pow(slope, 2, p)-2*x
    ysum= slope*(x-xsum)-y
    return (xsum%p, ysum%p)

def addpt(p1, p2, p):
    if p1 is None or p2 is None:
        return None
    (x1, y1)= p1
    (x2, y2)= p2
    if x1==x2:
        return dblpt(p1, p)

    # calculate (y1-y2)/(x1-x2)  modulus p
    slope=(y1-y2)*inverse(x1-x2, p)
    xsum= pow(slope, 2, p)-(x1+x2)
    ysum= slope*(x1-xsum)-y1
    return (xsum%p, ysum%p)

def ptmul(pt, a, p):
    scale= pt
    acc=None
    while a:
        if a&1:
            if acc is None:
                acc= scale
            else:
                acc= addpt(acc, scale, p)
        scale= dblpt(scale, p)
        a >>= 1
    return acc

def isoncurve(pt, p):
    (x, y)= pt
    return (y**2 - x**3 - 7)%p == 0

def integer_to_point(n):
    return ptmul(g, n, p)

def point_to_key(pt):
    x = str(hex(int(pt[0])))
    y = str(hex(int(pt[1])))
    public_key = '04' + x[2:len(x)-1] + y[2:len(y)-1]
    return public_key

def key_to_point(public_key):
    public_key = str(public_key)[2:len(str(public_key))]
    x = int(public_key[0:64], 16)
    y = int(public_key[64:128], 16)
    return (x, y)

def point_to_address(pt):
    public_key = point_to_key(pt)
    address = pybitcointools.pubkey_to_address(public_key)
    return address

def integer_to_address(n):
    a=g
    a = ptmul(a, n, p)
    return point_to_address(a)

def integer_to_string(n):
    c=''
    while n>0:
        d=n%256
        n=(n-d)/256
        c=c+chr(d)
    return c

def create_common_key(received_pt, my_private_integer):
    new_point = ptmul(received_pt, my_private_integer, p)
    point_int = new_point[0]*new_point[1]
    point_string = base64.b64encode(integer_to_string(point_int))
    return point_string[0:32]

def generate_IV():
    a=base64.b64encode(Random.new().read(100))  #uses pycrypto not random.  The IV is sent in cleartext anyway.
    return a[0:16]

def encrypt(key, message, IV):
    mode = AES.MODE_CBC
    encryptor = AES.new(key, mode, IV)
    time_string = str(int(time.time()))
    time_string = (16-len(time_string)%16)*'0'+time_string
    message = message+(16-len(message)%16)*" "+time_string
    ciphertext = encryptor.encrypt(message)
    return base64.b64encode(ciphertext)

def decrypt(key, ciphertext, IV):
    mode = AES.MODE_CBC
    decryptor = AES.new(key, mode, IV)
    plain = decryptor.decrypt(base64.b64decode(ciphertext))
    return plain

def assemble_message_pubkey(text, pubkey, my_private_integer):
    message = {}
    their_key = pubkey
    their_point = key_to_point(their_key)
    my_public_point = integer_to_point(my_private_integer)
    key = create_common_key(their_point, my_private_integer)
    iv = generate_IV()

    message['point_x'] = my_public_point[0]
    message['point_y'] = my_public_point[1]
    message['iv'] = iv
    message['ciphertext'] = encrypt(key, text, iv)
    return message, True

def assemble_message(text, their_pubkey, my_private_integer):
    message = {}
    their_point = key_to_point(their_pubkey)
    my_public_point = integer_to_point(my_private_integer)
    key = create_common_key(their_point, my_private_integer)
    iv = generate_IV()

    message['point_x'] = my_public_point[0]
    message['point_y'] = my_public_point[1]
    message['iv'] = iv
    message['ciphertext'] = encrypt(key, text, iv)
    return message

def decrypt_message(message, my_private_key):
    my_private_integer = encoding.wif_to_secret_exponent(my_private_key)
    their_point = (message['point_x'], message['point_y'])
    key = create_common_key(their_point, my_private_integer)
    text = decrypt(key, message['ciphertext'], message['iv'])
    time_string = text[len(text)-16:len(text)]
    try:
        time_reported = int(time_string)
    except:
        return '', False
    if time.time() - time_reported < time_threshold:
        return text[0:len(text)-16], True
    else:
        print "message too late"
        return '', False

def write_message_for_address(text, their_address, my_private_key):
    try:
        my_private_integer = encoding.wif_to_secret_exponent(my_private_key)
    except:
        print 'invalid private key'
        my_private_integer = 'invalid'
    if not my_private_integer == 'invalid':
        their_pubkey = key_scraping.get_pubkey_on_address(their_address)
        if their_pubkey[1]==True:
            their_pubkey = their_pubkey[0]
            message = assemble_message(text, their_pubkey, my_private_integer)
            return message
        else:
            print "Cannot find their public key from Blockchain record"
            return ''
    else:
        return ''
