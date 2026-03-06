import os
import json
import pandas as pd
import hashlib

data = 'hello world'

encoded = data.encode('utf-8')
hash_object = hashlib.sha256(encoded)

print(hash_object.hexdigest())