from django.shortcuts import render

from django.http import HttpResponse

from random import choice
from hashlib import md5
from Crypto.Cipher import AES
from base64 import b64encode
import json

def index(request):
    zen_of_py = """The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!"""

    seed = choice(range(1000,9999))
    passphrase = md5(str(seed ** 2 % 4877).encode()).hexdigest()[0x8:0x18]
    seed_to_return = b64encode(str(seed).encode())
    
    # construct a aes object
    aes = AES.new(passphrase.encode(), AES.MODE_ECB)

    # padding
    data = zen_of_py.encode()
    len_to_pad = 16 - len(data) % 16
    data_padded = data +  len_to_pad * len_to_pad.to_bytes(1, 'little')

    # encrypt
    data_encrypted = aes.encrypt(data_padded)
    rdata = json.dumps({'result':b64encode(data_encrypted).decode()})
    resp = HttpResponse(rdata)
    resp['content-type']= "application/json; charset=utf-8"
    resp['encrypted'] = seed_to_return

    #  (this is vulnerable)
    resp['Access-Control-Allow-Origin'] = request.META.get('HTTP_ORIGIN')

    return resp
