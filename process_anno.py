import re
import pymysql
import networkx as nx
from collections import defaultdict

def get_all_annos():
    annos=[]
    conn = pymysql.connect(user='root',password='root',port=3306,db='poem_anno')
    cursor = conn.cursor()

    sql="SELECT anno FROM anno_table WHERE anno!=''"
    cursor.execute(sql)
    results=cursor.fetchall()
    for res in results:
        annos.append(res[0])

    cursor.close()
    conn.close()
    return annos

def extract_words_from_annos(annos):
    word_list=[]
    for anno in annos:
        old_anno=anno
        if '①' in anno:
            anno = anno.replace('①', '（1）')
            anno = anno.replace('②', '（2）')
            anno = anno.replace('③', '（3）')
            anno = anno.replace('④', '（4）')
            anno = anno.replace('⑤', '（5）')
            anno = anno.replace('⑥', '（6）')
            anno = anno.replace('⑦', '（7）')
            anno = anno.replace('⑧', '（8）')
            anno = anno.replace('⑨', '（9）')
            anno = anno.replace('⑩', '（10）')
        if '⑴' in anno:
            anno = anno.replace('⑴', '（1）')
            anno = anno.replace('⑵', '（2）')
            anno = anno.replace('⑶', '（3）')
            anno = anno.replace('⑷', '（4）')
            anno = anno.replace('⑸', '（5）')
            anno = anno.replace('⑹', '（6）')
            anno = anno.replace('⑺', '（7）')
            anno = anno.replace('⑻', '（8）')
            anno = anno.replace('⑼', '（9）')
            anno = anno.replace('⑽', '（10）')
            anno = anno.replace('⑾', '（11）')
            anno = anno.replace('⑿', '（12）')
            anno = anno.replace('⒀', '（13）')
            anno = anno.replace('⒁', '（14）')
            anno = anno.replace('⒂', '（15）')
            anno = anno.replace('⒃', '（16）')
            anno = anno.replace('⒄', '（17）')
            anno = anno.replace('⒅', '（18）')
            anno = anno.replace('⒆', '（19）')
            anno = anno.replace('⒇', '（20）')
        pattern = re.compile(r'（\d{1,2}）(.*?)：')  # （1）
        results = pattern.findall(anno)
        word_list.extend(results)

        pattern = re.compile(r'\(\d{1,2}\)(.*?)：')  # (1)
        results = pattern.findall(anno)
        word_list.extend(results)

        pattern = re.compile(r'\d{1,2}、(.*?)：')  # 1、
        results = pattern.findall(anno)
        word_list.extend(results)

        pattern = re.compile(r'\d{1,2}\.(.*?)：')  # 1.
        results = pattern.findall(anno)
        word_list.extend(results)

        pattern = re.compile(r'\[\d{1,2}\](.*?)：')  # [1]
        results = pattern.findall(anno)
        word_list.extend(results)

        pattern = re.compile(r'。([^\d。]+?)：')  # 在一条注释中的注释
        results = pattern.findall(anno)
        word_list.extend(results)

        pattern = re.compile(r'^([^\d]+?)：')
        results = pattern.findall(anno)
        word_list.extend(results)

    return word_list

def remove_noise(word_list):
    new_word_list=[]
    for word in word_list:
        if '《' in word:
            continue
        word=re.sub(r'（.*?）','',word)
        new_word_list.append(word)
    return new_word_list

def deal_with_anno(anno,num):
    if num==1: # ⑴
        anno = anno.replace('⑴', '（1）')
        anno = anno.replace('⑵', '（2）')
        anno = anno.replace('⑶', '（3）')
        anno = anno.replace('⑷', '（4）')
        anno = anno.replace('⑸', '（5）')
        anno = anno.replace('⑹', '（6）')
        anno = anno.replace('⑺', '（7）')
        anno = anno.replace('⑻', '（8）')
        anno = anno.replace('⑼', '（9）')
        anno = anno.replace('⑽', '（10）')
        anno = anno.replace('⑾', '（11）')
        anno = anno.replace('⑿', '（12）')
        anno = anno.replace('⒀', '（13）')
        anno = anno.replace('⒁', '（14）')
        anno = anno.replace('⒂', '（15）')
        anno = anno.replace('⒃', '（16）')
        anno = anno.replace('⒄', '（17）')
        anno = anno.replace('⒅', '（18）')
        anno = anno.replace('⒆', '（19）')
        anno = anno.replace('⒇', '（20）')
    elif num==2: # ①
        anno = anno.replace('①', '（1）')
        anno = anno.replace('②', '（2）')
        anno = anno.replace('③', '（3）')
        anno = anno.replace('④', '（4）')
        anno = anno.replace('⑤', '（5）')
        anno = anno.replace('⑥', '（6）')
        anno = anno.replace('⑦', '（7）')
        anno = anno.replace('⑧', '（8）')
        anno = anno.replace('⑨', '（9）')
        anno = anno.replace('⑩', '（10）')
        anno = anno.replace('⑪', '（11）')
        anno = anno.replace('⑫', '（12）')
        anno = anno.replace('⑬', '（13）')
        anno = anno.replace('⑭', '（14）')
        anno = anno.replace('⑮', '（15）')
        anno = anno.replace('⑯', '（16）')
        anno = anno.replace('⑰', '（17）')
        anno = anno.replace('⑱', '（18）')
        anno = anno.replace('⑲', '（19）')
        anno = anno.replace('⑳', '（20）')
    return anno

def filter_word_anno_dict(word_anno_dict):
    new_word_anno_dict=defaultdict(list)
    bad_words=['题注','此地']
    for word,anno in word_anno_dict.items():
        # if '，' in word or '《' in word or '》' in word or anno=='':
        if '，' in word or '《' in word or '》' in word or '“' in word or '”' in word or '‘' in word or '’' in word or '句' in word or (len(anno) == 1 and anno[0] == '') or word in bad_words:
            continue
        else:
            word=re.sub(r'\(.*?\)','',word)
            word=re.sub(r'（.*?）','',word)
            word = re.sub(r'\[.*?\]', '', word)
            word=re.sub('[^\u4e00-\u9fa5]+','',word)
            new_word_anno_dict[word]=anno
    return new_word_anno_dict

def get_word_anno_dict(annos):
    count=0
    chinese_punc=['。','”','？','；']
    word_anno_dict=defaultdict(list)
    for anno in annos:
        # print(anno)
        anno=anno.replace(' ','')
        if '注解'==anno[:2]:
            anno=anno[2:]
        if '⑴'==anno[0]:
            anno=deal_with_anno(anno,1)
        elif '①'==anno[0]:
            anno=deal_with_anno(anno,2)
        if '(1)'==anno[:3]:
            anno = re.sub(r'\((\d{1,2})\)', '\n(\1)', anno)
            items=[item for item in anno.split('\n') if item!='']
            for item in items:
                if ')' not in item or '：' not in item:
                    continue
                start_index=item.index(')')
                middle_index=item.index('：')
                word=item[start_index+1:middle_index]
                anno=item[middle_index+1:]
                i=0
                while '：' in anno[i:]:
                    index=anno.find('：',i)
                    if anno[index+1]!='“' and anno[index-1]!='》':
                        index2=index-1
                        while index2>=0 and anno[index2] not in chinese_punc:
                            index2-=1
                        new_word=anno[index2+1:index]
                        new_anno=anno[index+1:]
                        anno=anno[:index2+1]
                        if anno!='':
                            word_anno_dict[word].append(anno)
                        word=new_word
                        anno=new_anno
                        i=0
                    else:
                        i=index+1
                if anno!='':
                    word_anno_dict[word].append(anno)
        elif '（1）'==anno[:3]:
            anno=re.sub(r'（(\d{1,2})）','\n（\1）',anno)
            # anno=anno.replace('（','\n（')
            items=[item for item in anno.split('\n') if item!='']
            for item in items:
                if '）' not in item or '：' not in item:
                    continue
                start_index=item.index('）')
                middle_index=item.index('：')
                word=item[start_index+1:middle_index]
                anno=item[middle_index+1:]
                i=0
                while '：' in anno[i:]:
                    index=anno.find('：',i)
                    if index==len(anno)-1:
                        break
                    if anno[index+1]!='“' and anno[index-1]!='》':
                        index2=index-1
                        while index2>=0 and anno[index2] not in chinese_punc:
                            index2-=1
                        new_word=anno[index2+1:index]
                        new_anno=anno[index+1:]
                        anno=anno[:index2+1]
                        if anno!='':
                            word_anno_dict[word].append(anno)
                        word=new_word
                        anno=new_anno
                        i=0
                    else:
                        i=index+1
                if anno!='':
                    word_anno_dict[word].append(anno)
        elif '〔1〕'==anno[:3]:
            anno=re.sub(r'〔(\d{1,2})〕','\n〔\1〕',anno)
            # anno=anno.replace('（','\n（')
            items=[item for item in anno.split('\n') if item!='']
            for item in items:
                if '〕' not in item or '：' not in item:
                    continue
                start_index=item.index('〕')
                middle_index=item.index('：')
                word=item[start_index+1:middle_index]
                anno=item[middle_index+1:]
                i=0
                while '：' in anno[i:]:
                    index=anno.find('：',i)
                    if index==len(anno)-1:
                        break
                    if anno[index+1]!='“' and anno[index-1]!='》':
                        index2=index-1
                        while index2>=0 and anno[index2] not in chinese_punc:
                            index2-=1
                        new_word=anno[index2+1:index]
                        new_anno=anno[index+1:]
                        anno=anno[:index2+1]
                        if anno!='':
                            word_anno_dict[word].append(anno)
                        word=new_word
                        anno=new_anno
                        i=0
                    else:
                        i=index+1
                if anno!='':
                    word_anno_dict[word].append(anno)
        elif '1.'==anno[:2]:
            anno = re.sub(r'(\d{1,2})\.', '\n\1.', anno)
            items = [item for item in anno.split('\n') if item != '']
            for item in items:
                if '.' not in item or '：' not in item:
                    continue
                start_index = item.index('.')
                middle_index = item.index('：')
                word = item[start_index + 1:middle_index]
                anno = item[middle_index + 1:]
                i = 0
                # print(word,anno)
                while '：' in anno[i:]:
                    index = anno.find('：', i)
                    if anno[index + 1] != '“' and anno[index-1]!='》':
                        index2 = index - 1
                        while index2>=0 and anno[index2] not in chinese_punc:
                            index2 -= 1
                        new_word = anno[index2 + 1:index]
                        new_anno = anno[index + 1:]
                        anno = anno[:index2 + 1]
                        if anno!='':
                            word_anno_dict[word].append(anno)
                        word = new_word
                        anno = new_anno
                        i = 0
                    else:
                        i = index + 1
                if anno!='':
                    word_anno_dict[word].append(anno)
        elif '1、'==anno[:2]:
            anno = re.sub(r'(\d{1,2})、', '\n\1、', anno)
            items = [item for item in anno.split('\n') if item != '']
            for item in items:
                if '、' not in item or '：' not in item:
                    continue
                start_index = item.index('、')
                middle_index = item.index('：')
                word = item[start_index + 1:middle_index]
                anno = item[middle_index + 1:]
                i = 0
                while '：' in anno[i:]:
                    index = anno.find('：', i)
                    if anno[index + 1] != '“' and anno[index - 1] != '》':
                        index2 = index - 1
                        while index2>=0 and anno[index2] not in chinese_punc:
                            index2 -= 1
                        new_word = anno[index2 + 1:index]
                        new_anno = anno[index + 1:]
                        anno = anno[:index2 + 1]
                        if anno!='':
                            word_anno_dict[word].append(anno)
                        word = new_word
                        anno = new_anno
                        i = 0
                    else:
                        i = index + 1
                if anno!='':
                    word_anno_dict[word].append(anno)
        elif '[1]'==anno[:3]:
            anno = re.sub(r'\[(\d{1,2})\]', '\n[\1]', anno)
            items = [item for item in anno.split('\n') if item != '']
            for item in items:
                if ']' not in item or '：' not in item:
                    continue
                start_index = item.index(']')
                middle_index = item.index('：')
                word = item[start_index + 1:middle_index]
                anno = item[middle_index + 1:]
                i = 0
                while '：' in anno[i:]:
                    index = anno.find('：', i)
                    if anno[index + 1] != '“' and anno[index - 1] != '》':
                        index2 = index - 1
                        while index2>=0 and anno[index2] not in chinese_punc:
                            index2 -= 1
                        new_word = anno[index2 + 1:index]
                        new_anno = anno[index + 1:]
                        anno = anno[:index2 + 1]
                        if anno!='':
                            word_anno_dict[word].append(anno)
                        word = new_word
                        anno = new_anno
                        i = 0
                    else:
                        i = index + 1
                if anno!='':
                    word_anno_dict[word].append(anno)
        else:
            if '：' in anno:
                index=anno.index('：')
                word=anno[:index]
                anno=anno[index+1:]
                i = 0
                while '：' in anno[i:]:
                    index = anno.find('：', i)
                    if anno[index + 1] != '“' and anno[index-1]!='》':
                        index2 = index - 1
                        while index2>=0 and anno[index2] not in chinese_punc:
                            index2 -= 1
                        new_word = anno[index2 + 1:index]
                        new_anno = anno[index + 1:]
                        anno = anno[:index2 + 1]
                        if anno!='':
                            word_anno_dict[word].append(anno)
                        word = new_word
                        anno = new_anno
                        i = 0
                    else:
                        i = index + 1
                if anno!='':
                    word_anno_dict[word].append(anno)
        # if count==2000:
        #     break
        # count += 1
    word_anno_dict=filter_word_anno_dict(word_anno_dict)
    with open('tmp.txt','w',encoding='utf-8') as f:
        for word,anno in word_anno_dict.items():
            # if len(word)>1 and len(word)<5:
            f.write('{}:{}\n'.format(word,'|'.join(anno)))
            # print('{}:{}\n'.format(word,'|'.join(anno)))
    return word_anno_dict

def find_new_words(word_anno_dict):
    G=nx.Graph()
    # seed_words=['送别','离别','别离']
    seed_words=['西域','塞外','新疆','打仗','战争','军事']
    # seed_words=['他乡','异乡','游子','羁旅','客居']

    # seed_words=['地名']
    # seed_words=['重阳']
    # seed_words=['除夕']
    # seed_words=['首饰']
    # seed_words=['洞庭湖']
    # seed_words=['游览胜地']
    # seed_words=['在今']
    # seed_words=['建安']
    word_set=set()
    for i in range(len(seed_words)):
        word_set.add(seed_words[i])
        for j in range(i+1,len(seed_words)):
            G.add_edge(seed_words[i],seed_words[j])

    extend_words=[]
    for seed in seed_words:
        # count=0
        for word, anno_list in word_anno_dict.items():
            if seed in '|'.join(anno_list) and word not in word_set and len(word)>1:
                # count+=1
                G.add_edge(seed, word)
                extend_words.append(word)
                word_set.add(word)
        # print(seed,count)
    print(extend_words)

    # while len(extend_words)!=0:
    #     seed_words=extend_words
    #     extend_words=[]
    #     for seed in seed_words:
    #         count=0
    #         for word,anno_list in word_anno_dict.items():
    #             if seed in '|'.join(anno_list) and word not in word_set and len(word)>1:
    #                 count+=1
    #                 G.add_edge(seed,word)
    #                 extend_words.append(word)
    #                 word_set.add(word)
    #         if count>0:
    #             print(seed,count)

    nx.write_gml(G,'graphs/anno_graph.gml')
    with open('graphs/anno_graph_nodes.csv','w',encoding='utf-8') as f:
        f.write(':ID,name,:LABEL\n')
        node_id_dict={}
        for i,node in enumerate(G.nodes()):
            node_id_dict[node]=i
            f.write('{},{},node\n'.format(i,node))
    with open('graphs/anno_graph_edges.csv','w',encoding='utf-8') as f:
        f.write(':START_ID,:END_ID,:TYPE\n')
        for edge in G.edges():
            start_id=node_id_dict[edge[0]]
            end_id=node_id_dict[edge[1]]
            f.write('{},{},R\n'.format(start_id,end_id))


if __name__ == '__main__':
    annos=get_all_annos()
    word_anno_dict=get_word_anno_dict(annos)
    find_new_words(word_anno_dict)
    # word_list=extract_words_from_annos(annos)
    # word_list=remove_noise(word_list)
    # word_freq_dict=defaultdict(int)
    # for word in word_list:
    #     word_freq_dict[word] += 1
    # with open('tmp.txt','w',encoding='utf-8') as f:
        # for word in word_freq_dict:
        #     if word_freq_dict[word]>=2 and len(word)>1:
        #         f.write('{}\n'.format(word))
        # for anno in annos:
        #     f.write('{}\n'.format(anno))