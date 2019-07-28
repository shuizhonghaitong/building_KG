import pymysql
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

if __name__ == '__main__':
    annos=get_all_annos()
