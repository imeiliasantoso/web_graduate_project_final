#! /usr/bin/env python2

import re
import json


def convert():
    parentName = "URL_of_Anchor"
    tmplist = [{"name": parentName, "parentid": ''}]
    fr = open('/Users/imeiliasantoso/web_graduate_project5/predict_page/balance_bank_5.txt', 'r')
    namelist = []
    for i, line in enumerate(fr):
        state1 = line.find('Number of Leaves')
        state2 = line.find('Size of the tree')
        if i > 2 and state1 < 0 and state2 < 0 and len(line) > 4:
            line = (line.replace('\r', '').replace('\n', ''))
            if line.find('|   ') < 0:
                line = line.replace('|   ', '')
                tmplist.append({"name": line, "parentid": parentName})
                namelist = [line]

            else:
                num = line.count('|   ')

                line = line.replace('|   ', '')
                tmplist.append({"name": line, "parentid": namelist[num - 1]})

                if len(namelist) < num + 1:
                    namelist.append(line)
                else:
                    namelist[num] = line
                    # print (num,namelist)
    source = tmplist

    def getChildren(name=''):
        sz = []
        for obj in source:
            if obj["parentid"] == name:

                sp = obj["name"].split(':')
                if len(sp) == 2:
                    sp1 = sp[1]
                    sp11 = sp1[:(sp1.find('('))]
                    m = re.match(".*\((.*)\).*", sp1)
                    number = m.group(1)
                    sz.append({'name': sp[0], "number": float(number.split('/')[0])})
                else:
                    m = re.match(".*\((.*)\).*", obj["name"])
                    if m is not None:
                        number = m.group(1)
                        sz.append({"name": obj["name"], "number": float(number), "children": getChildren(obj["name"])})
                    else:
                        sz.append({"name": obj["name"], "children": getChildren(obj["name"])})


                        # sz.append({"name":obj["name"],"children":getChildren(obj["name"])})
        return sz

    tmpdict = {"name": parentName, "children": getChildren(name=parentName)}

    print (json.dumps(tmpdict, indent=2))

    with open("/Users/imeiliasantoso/web_graduate_project5/predict_page/balance_bank_5.json", 'w') as json_file:
        json_file.write(json.dumps(tmpdict, indent=2, ensure_ascii=False))
