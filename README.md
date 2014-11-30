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

####Things you could conceivably do with Bitcrypt

-- Log into websites with encrypted messages
-- Speak to financial counterparts as the cryptographically proven owner of certain financial assets.  Every message you write proves you own X bitcoins.  It also links you to
the full transactional history behind that address.


####Thanks to
"jackjack" - https://github.com/jackjack-jj/jeeq
Vitalik - https://github.com/vbuterin/pybitcointools

####I leaned heavily on these libraries.  They did most of the real work.  
