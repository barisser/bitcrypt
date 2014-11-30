import jeeq
import pybitcointools
import time

def generate_keys():
    keys = jeeq.generate_keys()
    secret_exponent = keys[0]
    compressed_public_key = keys[1]
    uncompressed_public_key = keys[2]
    compressed_btc_address = keys[3][0]
    uncompressed_btc_address = keys[3][1]
    results = {}
    results['secret_exponent'] = secret_exponent
    results['compressed_public_key'] = compressed_public_key
    results['uncompressed_public_key'] = uncompressed_public_key
    results['compressed_btc_address'] = compressed_btc_address
    results['uncompressed_btc_address'] = uncompressed_btc_address
    return results

def secret_exponent_to_uncompressed_public_key(secret_exponent):
    return pybitcointools.privtopub(secret_exponent)

def hex_public_key_to_address(hex_public_key):
    return jeeq.public_key_to_bc_address(hex_public_key.decode('hex'))

def encrypt_message(public_key, message):
    return jeeq.encrypt_message(public_key.decode('hex'), message)

def decrypt_message(private_key, ciphertext):
    decrypted = jeeq.decrypt_message(private_key.decode('hex'), ciphertext)
    if len(decrypted)>1:
        return decrypted[0]
    else:
        return -1

def make_signature(sender_public_key, receiver_public_key, sender_secret_exponent):
    string = str(sender_public_key)+" "+str(receiver_public_key)
    string = string + " " + str(time.time())
    answer = {}
    answer['signed'] = pybitcointools.ecdsa_sign(string, sender_secret_exponent)
    answer['message'] = string
    return answer

def write_message(secret_exponent_signer, public_key_recipient, message_text):
    public_key_sender = pybitcointools.privkey_to_pubkey(secret_exponent_signer)
    message={}
    message['sender_public_key'] = secret_exponent_to_uncompressed_public_key(secret_exponent_signer)   #uncompressed
    message['sender_btc_address'] = hex_public_key_to_address(message['sender_public_key'])   #uncompressed
    message['recipient_public_key'] = public_key_recipient   #uncompressed
    message['recipient_btc_address'] = hex_public_key_to_address(public_key_recipient) #uncompressed
    message['ciphertext'] = encrypt_message(public_key_recipient, message_text)   #encrypted for recipient
    message['sender_signature'] = make_signature(public_key_sender, public_key_recipient, secret_exponent_signer)
    return message

def verify_message(message, my_uncompressed_public_key):
    my_uncompressed_bitcoin_address = pybitcointools.pubtoaddr(my_uncompressed_public_key)
    veracity = True
    #verify sender key to address
    calculated_sender_address = pybitcointools.pubtoaddr(message['sender_public_key'])
    if calculated_sender_address != message['sender_btc_address']:
        veracity = False

    if veracity:
    #check that the message is for me
        calculated_my_address = pybitcointools.pubtoaddr(message['recipient_public_key'])
        if calculated_my_address != my_uncompressed_bitcoin_address:
            veracity = False
        if message['recipient_public_key'] != my_uncompressed_public_key:
            veracity = False

    if veracity:
        #check signature
        signature_message = message['sender_signature']['message']
        message_contents = signature_message.split(' ')
        sign_sender_public_key = message_contents[0]
        sign_recipient_public_key = message_contents[1]
        timestamp = float(message_contents[2])

        #check that public keys match
        if sign_sender_public_key != message['sender_public_key']:
            veracity = False
        if sign_recipient_public_key != my_uncompressed_public_key:
            veracity = False
        #check timestamp somehow??

        #check signed portion
        sig = message['sender_signature']['signed']
        signature_veracity = pybitcointools.ecdsa_verify(signature_message, sig, message['sender_public_key'])

        if signature_veracity == False:
            veracity = False

    return veracity

def read_message(message, my_private_key, my_public_key):
    veracity = verify_message(message, my_public_key)
    if veracity:
        #actually decrypt message
        plaintext = decrypt_message(my_private_key, message['ciphertext'])

        return [veracity, plaintext]
    else:
        return [veracity, '']
