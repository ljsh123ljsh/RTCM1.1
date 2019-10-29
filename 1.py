from re import search

x = 'abcdefg'
m = search('t', x)
print(m)
if m is None:
    print('d')
else:
    print('f')