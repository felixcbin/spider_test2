# coding:utf-8
import csv
import pymysql


class csvHandler(object):
    def __init__(self, path):
        print('path:', path)
        self.f = open(path, 'w', encoding='utf-8')
        self.fw = csv.writer(self.f)
        self.head = False

    def write(self, keys, info):
        rowinfo = [info.get(key, ' ') for key in keys]
        print(rowinfo)
        if self.head:
            self.fw.writerow(rowinfo)
        else:
            self.fw.writerow(keys)
            self.fw.writerow(rowinfo)
            self.head = True

    def close(self):
        self.f.close()


class mysqlHandler(object):
    def __init__(self, host='139.9.45.198', user='root', passwd='', dbname='', tbname=''):
        self.dbcon = pymysql.connect(host, user, passwd, dbname, charset='utf8')
        self.cur = self.dbcon.cursor()
        self.tname = tbname
        self.id = 1

    def write(self, keys, info):
        # sql = 'insert into %s values' % self.tname
        sql = 'insert into %s values' % self.tname
        values = '(%s)' % (('%s,' * (len(keys)))[:-1])
        sql += values
        rowinfo = [info.get(key, ' ') for key in keys]
        # rowinfo.insert(0, self.id)
        # self.id += 1
        self.cur.execute(sql, rowinfo)
        self.dbcon.commit()

    def close(self):
        self.dbcon.close()


if __name__ == '__main__':
    # fcsv = csvHandler('D:/test.csv')
    # fcsv.write([], [])
    # fcsv.close()
    sql = mysqlHandler('139.9.45.198', 'root', '123456', 'spider', 'test')
    sql.write([0,1], {0:2, 1:'felix'})
    sql.close()
