# -*- coding:utf-8 -*-
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

tree = et.parse('aa.xml')
root = tree.getroot()
bb = 0
for i in root :
    # print(i.find('id').text)
    if i.find('entry'):
        e = i.find('entry')
        bb += 1
        # print(e.find('isosid').text)

print(bb)