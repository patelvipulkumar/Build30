import hashlib
a = hashlib.sha256('hello world'.encode('utf-8')).hexdigest()
b = hashlib.sha256('hello world!'.encode('utf-8')).hexdigest()
print(a)
print(b)
print('length:', len(a), 'same:', a == b)
print('python hash:', hash('hello world'))