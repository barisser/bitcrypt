##Bitcrypt
========

###Encrypted Messaging Built Into Bitcoin

Write encrypted messages in the language of Bitcoin.

-- Send encrypted messages to Bitcoin addresses
  - Only the holder of that address can decipher the message

-- Send an encrypted message provably as the owner of a given Bitcoin address.
  - You prove you own an address, while saying whatever you want, without losing any anonymity.

-- Bitcoin ECDSA key generation has been linked with an implementation of asymmetric ECDSA-based encryption.  I'm relying heavily on the work of others (see below).

My goal is for cleartext communication channels to also be cryptographically secure and linked to financial tools built on Bitcoin.

I would like Bitcoin public addresses to represent identity in general.  Whatever you want to do, your public key
should be your outward face.  

###Example Usage

import bitcrypt  

sender_keys = bitcrypt.generate_keys()  

receiver_keys = bitcrypt.generate_keys()  

sender_keys  
{'compressed_public_key': '02871247985bf1ff81e822f2be4022630480c2d957bb5c4fa2a418851f76902d7b', 'secret_exponent': '125ba31a2526f125ba31a2526f125ba31a2526f125ba31a2526f125ba31a2526', 'compressed_btc_address': '1EgiYDeTh1y9wB1QVpby66mQfMHYBQ5VSD', 'uncompressed_btc_address': '1LUo6fpakNZPC41KPAYu9VufayF7RbQWws', 'uncompressed_public_key': '04871247985bf1ff81e822f2be4022630480c2d957bb5c4fa2a418851f76902d7b1e7399b45eff41657b3daffd461f984109645f8638e57b7f6ae4c06d6f94d6c0'}  

message = bitcrypt.write_message(sender_keys['secret_exponent'], receiver_keys['uncompressed_public_key'], 'hello crazy world')  

message  
{'ciphertext': 'amoAAAKyJAAyCDhdzEKzSiPwhHjPeyXa+KH4qKpJmcHCCGZ/yXo5RgMuxC2po1k6pRCEER+ZItJKICXhPkw711fZWhYig4F7uQ==', 'sender_signature': {'message': '04871247985bf1ff81e822f2be4022630480c2d957bb5c4fa2a418851f76902d7b1e7399b45eff41657b3daffd461f984109645f8638e57b7f6ae4c06d6f94d6c0 0453d2454662132c80c97559114d9f2cd9036e77bc7537c1be2b4cc06441ba52a5c5a5d463e6e5e06d9a0925f356e172f79313339179949a9539cda121e7262af6 1417326232.34', 'signed': 'HFfK9srWKctKN9429r+4ubtc8DNctuepoZgUvp+k12nBQdbGVdSZ245c85iHv/ofHKSvXqNm/OBUcNyiKw1DXQ4='}, 'recipient_btc_address': '1JNQdqveVDzmKs7m22NY3bU69p4Auat6Te', 'sender_btc_address': '1LUo6fpakNZPC41KPAYu9VufayF7RbQWws', 'sender_public_key': '04871247985bf1ff81e822f2be4022630480c2d957bb5c4fa2a418851f76902d7b1e7399b45eff41657b3daffd461f984109645f8638e57b7f6ae4c06d6f94d6c0', 'recipient_public_key': '0453d2454662132c80c97559114d9f2cd9036e77bc7537c1be2b4cc06441ba52a5c5a5d463e6e5e06d9a0925f356e172f79313339179949a9539cda121e7262af6'}  

print bitcrypt.verify_message(message, receiver_keys['uncompressed_public_key'])  
True  

bitcrypt.read_message(message, receiver_keys['secret_exponent'], receiver_keys['uncompressed_public_key'])  
[True, 'hello crazy world']




####Things you could conceivably do with Bitcrypt

-- Log into websites with encrypted messages
-- Speak to financial counterparts as the cryptographically proven owner of certain financial assets.  Every message you write proves you own X bitcoins.  It also links you to
the full transactional history behind that address.


####Thanks to
"jackjack" - https://github.com/jackjack-jj/jeeq
Vitalik - https://github.com/vbuterin/pybitcointools

####I leaned heavily on these libraries.  They did most of the real work.  
