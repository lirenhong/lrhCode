from collections import OrderedDict
nd = {"a":{"a1":1, "a2":2},"b":{"b1":5, "b2":3}, "c":{"c1":10, "c2":23}}

def s(t):
    m = max(t.items(), key=lambda x:x[1])[1]
    print m
    return m
s = sorted(nd.items(), key=lambda x:s(x[1]), reverse=True)
s = OrderedDict(s)
print s
for k, v in s.items():
    s[k] = sorted(v.items(), key=lambda x:x[1], reverse=True)

print s
