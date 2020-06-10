# -*- coding: UTF-8 -*-
import os, re, json
from operator import itemgetter
from pypinyin import lazy_pinyin, NORMAL

vocab_dict = {("</bos>", ""): 0, ("</eos>", ""): 0}
prefix = "../sina_news_gbk/2016-"
suffix = "_con.txt"
tablefile = "../拼音汉字表_12710172/一二级汉字表.txt"
tablestr = ""
objectpath = "../sina_news_vocab"
#objectpath = "./vocab_poem"
beginid = 2
endid = 12


# 读取一二级汉字表
def read_char():
    global tablestr
    with open(tablefile, encoding="gbk") as f:
        tablestr = f.read()


# 读取语料
# 句子的分割以一个标点符号为标志，而不是句号
def read_save_vocab():
    global vocab_dict
    read_char()
    filename = ""
    count = 0
    print("Begin read corpus file...")
    for fileid in range(beginid, endid+1):
        if fileid < 10:
            filename = prefix + "0" + str(fileid) + suffix
        else:
            filename = prefix + str(fileid) + suffix
        if os.path.exists(filename):
            print("Begin read file " + filename + " ...")
            with open(filename, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    pinyinline = lazy_pinyin(line, style=NORMAL, errors='ignore')
                    # print(line, pinyinline)
                    i = 0
                    # sentence = modify(json.loads(line, encoding="gbk")["html"])
                    for ch in line:
                        if ch in tablestr:
                            count += 1
                            vocab_dict[(ch, pinyinline[i])] = vocab_dict.get((ch, pinyinline[i]), 0) + 1
                            i += 1
                        elif ch == "B":
                            vocab_dict[("</bos>", "")] += 1
                        elif ch == "E":
                            vocab_dict[("</eos>", "")] += 1
    # 排序
    vocab_dict = sorted(vocab_dict.items(), key=itemgetter(1), reverse=True)
    vocab2id = {}
    rank = 0
    if not os.path.exists(objectpath):
        os.mkdir(objectpath)
    # 保存词频统计文件
    print("Begin save vocab file...")
    with open(objectpath+"/vocab.txt", mode="w+", encoding="utf-8") as f:
        f.write(str(count) + "\n")
        # print(vocab_dict)
        for rank, item in enumerate(vocab_dict):
            vocab2id[item[0]] = rank# 编号
            f.write(str(item[0]) + " " + str(item[1]) + "\n")
    # 保存vocab2id 映射表
    print("Save vocab2id...")
    with open(objectpath+"/vocab2id.json", "w+", encoding="utf-8") as f:
        f.write(str(vocab2id))
        # json.dump(vocab2id, f)
    # 保存语料文件
    print("Begin save corpus file...")
    with open(objectpath+"/corpus.txt", mode="w+", encoding="utf-8") as f:
        for fileid in range(beginid, endid+1):
            if fileid < 10:
                filename = prefix + "0" + str(fileid) + suffix
            else:
                filename = prefix + str(fileid) + suffix
            if os.path.exists(filename):
                print("Begin save id file " + filename + " ...")
                with open(filename, "r", encoding="utf-8") as g:
                    f.write(str(vocab2id[("</bos>", "")]) + " ")
                    for line in g.readlines():
                        #sentence = modify(json.loads(line, encoding="gbk")["html"])
                        pinyinline = lazy_pinyin(line, style=NORMAL, errors='ignore')
                        i = 0
                        for ch in line:
                            if ch in tablestr and (ch, pinyinline[i]) in vocab2id:
                                f.write(str(vocab2id[(ch, pinyinline[i])]) + " ")
                                i += 1
                        f.write("\n")
