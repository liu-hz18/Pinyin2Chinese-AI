#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from zhon.hanzi import punctuation

punctuation += "0123456789ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.%!()【】（）.．/~`●■★\n\t\r"


def modify(sentence):
    if len(sentence) > 0 and sentence[-1] in (r"[%s]+" % punctuation):
        sentence = sentence[:-1]
    return "B" + re.sub(r"[%s]+" % punctuation, "EB", sentence.lstrip("原标题：")) + "E"


def readFile(name):
    print(name)
    try:
        with open(name + ".txt", 'r', encoding="gbk", errors="ignore") as f:
            lines = f.readlines()
            for line in lines:
                sentence = modify(json.loads(line, encoding="gbk")["html"])
                with open(name + "_con.txt", 'a+', encoding='utf-8') as fin:
                    fin.write(sentence + "\n")
        return None
    except:
        print("error occured when reading file" + name + " File not exist ? ")
        return None


if __name__ == '__main__':
    prefix = "../sina_news_gbk/2016-"
    filename = ["02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]
    for name in filename:
        readFile(prefix + name)