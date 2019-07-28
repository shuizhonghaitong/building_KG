import os
import re
import json
from collections import defaultdict

def process_comment(comment):
    anno_list=[]
    if '| ：' in comment:
        comment=comment.split('| ：')[0].strip()
        if comment:
            comment=comment[1:]
            comment = comment.replace('①', '（1）')
            comment = comment.replace('②', '（2）')
            comment = comment.replace('③', '（3）')
            comment = comment.replace('④', '（4）')
            comment = comment.replace('⑤', '（5）')
            comment = comment.replace('⑥', '（6）')
            comment = comment.replace('⑦', '（7）')
            comment = comment.replace('⑧', '（8）')
            comment = comment.replace('⑨', '（9）')
            comment = comment.replace('⑩', '（10）')
            items=comment.split('\r\n')
            for item in items:
                pattern = re.compile(r'（\d{1,2}）(.*?)：') # （1）
                results = pattern.findall(item)
                anno_list.extend(results)

                pattern = re.compile(r'〔\d{1,2}〕(.*?)：') # 〔1〕
                results = pattern.findall(item)
                anno_list.extend(results)

                pattern = re.compile(r'\[\d{1,2}\](.*?)：') # [1]
                results = pattern.findall(item)
                anno_list.extend(results)

                pattern = re.compile(r'\d{1,2}、(.*?)：') # 1、
                results = pattern.findall(item)
                anno_list.extend(results)

                pattern = re.compile(r'\(\d{1,2}\)(.*?)：') # (1)
                results = pattern.findall(item)
                anno_list.extend(results)

                pattern=re.compile(r'。([^\d。]+?)：') # 在一条注释中的注释
                results=pattern.findall(item)
                anno_list.extend(results)

                pattern=re.compile(r'^([^\d]+?)：')
                results=pattern.findall(item)
                anno_list.extend(results)
    # else:
    #     comment = comment.replace('①', '（1）')
    #     comment = comment.replace('②', '（2）')
    #     comment = comment.replace('③', '（3）')
    #     comment = comment.replace('④', '（4）')
    #     comment = comment.replace('⑤', '（5）')
    #     comment = comment.replace('⑥', '（6）')
    #     comment = comment.replace('⑦', '（7）')
    #     comment = comment.replace('⑧', '（8）')
    #     comment = comment.replace('⑨', '（9）')
    #     comment = comment.replace('⑩', '（10）')
    #
    #     pattern = re.compile(r'（\d{1,2}）(.*?)：')  # （1）
    #     results = pattern.findall(comment)
    #     anno_list.extend(results)
    #
    #     pattern = re.compile(r'〔\d{1,2}〕(.*?)：')  # 〔1〕
    #     results = pattern.findall(comment)
    #     anno_list.extend(results)
    #
    #     pattern = re.compile(r'\[\d{1,2}\](.*?)：')  # [1]
    #     results = pattern.findall(comment)
    #     anno_list.extend(results)
    #
    #     pattern = re.compile(r'\d{1,2}、(.*?)：')  # 1、
    #     results = pattern.findall(comment)
    #     anno_list.extend(results)
    #
    #     pattern = re.compile(r'\(\d{1,2}\)(.*?)：')  # (1)
    #     results = pattern.findall(comment)
    #     anno_list.extend(results)
    #     #
    #     # pattern = re.compile(r'。([^\d。]+?)：')  # 在一条注释中的注释
    #     # results = pattern.findall(comment)
    #     # anno_list.extend(results)
    #     #
    #     # pattern = re.compile(r'^([^\d]+?)：')
    #     # results = pattern.findall(comment)
    #     # anno_list.extend(results)
    anno_list = list(set(anno_list))

    return anno_list

def filter(anno_list):
    new_anno_list=[]
    for anno in anno_list:
        if len(anno)>10:
            continue
        anno=anno.strip()
        anno=re.sub(r'\(.*\)','',anno)
        anno=re.sub(r'（.*）','',anno)
        new_anno_list.append(anno)
    return new_anno_list


def extract_annotation_words():
    count=0
    word_freq_dict=defaultdict(int)
    filenames = os.listdir('唐')
    for name in filenames:
        with open('唐/' + name, 'r', encoding='utf-8') as f:
            poet_info = json.load(f)
            dynasty = poet_info['dynasty']
            author = poet_info['author']
            poems = poet_info['poems']
            for poem in poems:
                title = poem['title']
                content = poem['content']
                if poem['comment'] != '':
                    anno_list=process_comment(poem['comment'])
                    anno_list=filter(anno_list)
                    if len(anno_list)!=0:
                        count+=1
                    for word in anno_list:
                        word_freq_dict[word]+=1
    with open('tmp.txt','w',encoding='utf-8') as f:
        for word in word_freq_dict:
            if len(word)>=2:
                f.write('{}\n'.format(word))
    print(count)
                        # if word[-1]=='句':
                        #     print(word)



if __name__ == '__main__':
    extract_annotation_words()