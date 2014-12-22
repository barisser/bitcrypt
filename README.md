##Bitcrypt
========

###Encrypted Messaging Built Into Bitcoin

Write encrypted messages in the language of Bitcoin.

-- Send encrypted messages to Bitcoin addresses
  - Only the holder of that address can decipher the message

-- Send an encrypted message provably as the owner of a given Bitcoin address.
  - You prove you own an address, while saying whatever you want, without losing anonymity.

###Highlights

-- Diffie-Helman Key Exchange to create a secret shared key

-- Symmetric Encryption with AES-CBC with the shared key for encrypted messaging

-- Scrapes the public key for the receiving address from the Blockchain record.
  This will not always yield a result.  Only addresses that have signed pay-to-pubkeyhash scripts will yield a public key.  Uses Blockchain.info for now; could use bitcoind directly if necessary.

-- Encrypted time threshold to mitigate replay attacks.  


###Present Status

-- This is a prototype only.  This is not a finished product and should not be
used for serious security.  

-- Everything is unreviewed.  Please feel free to offer constructive feedback.

-- There are some issues with padding that I would like feedback on.  I'm not sure what level of secure padding is necessary.

-- Also the way in which I map the calculated shared secret point to a key for AES should be checked for any predictable weaknesses to outsiders.

###Design Philosophy

-- Use existing tools that are strong.  

-- Rely on the most simplistic approach to minimize risks I'm not aware of.




My goal is for cleartext communication channels to also be cryptographically secure and linked to financial tools built on Bitcoin.

I would like Bitcoin public addresses to represent identity in general.  Whatever you want to do, your public key
should be your outward face.  

###Dependencies

- PyCrypto.  I'm relying on this for AES encryption.

- Vitalik's pybitcointools.  This is a helpful utility.

- Richard Kiss's PyCoin library.  I'm only using this in converting private keys to secret exponents.  I was too lazy to do this myself.

- It touches the Blockchain.info API for scraping public keys.  This is non-essential.  It's an ancillary utility.  Blockchain.info could be easily replaced with something pointing towards Bitcoind, or any other API.

- For some of the Elliptic Curve operations, I've copied some code from https://gist.github.com/nlitsme/c9031c7b9bf6bb009e5a for convenience.  All that occurs here is Elliptic Curve addition, multiplication, etc.  This code does not originate any private keys; it is purely mechanical.  

###Example Usage

>>> from bitcrypt import *
>>> message = write_message_for_address('hi', '1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm', '5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAvUcVfH')

(this is the public address corresponding with secret exponent = 1 and private key for secret exponent = 2)

>>> message
{'ciphertext': 'n/9zUY0FfAYusbO5RhtP5meHztOuh5HM9PUG5YUqCWE=', 'point_x': 89565891926547004231252920425935692360644145829622209833684329913297188986597L, 'point_y': 12158399299693830322967808612713398636155367887041628176798871954788371653930L, 'iv': 'NnfufNoLc8OgcWYq'}

(the x and y coordinates are the public key point for ME, ie, the public address corresponding to secret exponent = 2 )

>>> decrypted = decrypt_message(message, '5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf')

(use the private key corresponding to the receiving address, ie, secret_exponent = 1)

>>> decrypted
('hi              ', True)


####Things you could conceivably do with Bitcrypt

-- Log into websites with encrypted messages
-- Speak to financial counterparts as the cryptographically proven owner of certain financial assets.  Every message you write proves you own X bitcoins.  It also links you to
the full transactional history behind that address.
-- Control Devices on the Blockchain with encrypted commands

##Example Usage
