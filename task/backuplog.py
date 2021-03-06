# coding=utf8
from __future__ import with_statement
from optparse import OptionParser
from datetime import date
import sys, os, re
def parselocaldate(l):
    pat = '(?P<y>\d\d\d\d)(?P<m>\d\d)(?P<d>\d\d)' 
    m = re.match(pat, l)
    y = int(m.group('y'))
    mon = int(m.group('m'))
    d = int(m.group('d'))
    return date(y, mon, d)

def strpdate(str):
    pat = r'(?P<m>\d\d)-(?P<d>\d\d)-(?P<y>\d\d\d\d)'
    m = re.match(pat, str)
    y = int(m.group('y'))
    mon = int(m.group('m'))
    d = int(m.group('d'))
    return date(y, mon, d)

def match(f, options):
    if options.all: 
        return True
    pat  = r'(?P<d>\d\d-\d\d-\d\d\d\d)\.'
    pat += r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    pat += r'\.log(\s|$)'
    res = False
    m = re.match(pat, f)
    if m:
        res = True
        if options.before:
            d = m.group('d')
            d = strpdate(d)
            b = parselocaldate(options.before)
            res = d < b
    return res

'''
1.0:備份指定日期區間的log
1.1:加入備份快捷
1.2:備份檔案檔名其年月格式改為 201101 等 6 位數字表示 
'''
if __name__ == "__main__":
    usage = u"usage: %prog logpath [options]"
    parser = OptionParser(usage, version="%prog 1.2", 
             description=u"檢視、摘要、列印 syslog"
        )
    parser.add_option("-b", "--before", dest="before", 
                       help=u"列出指定日期前之日誌，例：20100911")

    parser.add_option("-a", "--all", action="store_true",
                      dest="all", 
                      help=u"列出指定根目錄之所有日誌檔，不作任何動作")

    parser.add_option("-t", "--tar", action="store_true",
                      dest="tar", 
                      help=u"加入壓縮檔")

    parser.add_option("-R", "--remove", action="store_true",
                      dest="remove", 
                      help=u"加入壓縮檔後刪除原檔案")

    parser.add_option("-f", "--file", dest="file", 
                      help=u"指定備份到何種檔案")

    parser.add_option("-H", "--HLTB", dest="HLTB", 
                      help=u"稅處備份快捷，inner 表內網，outer 表外網")

    (options, args) = parser.parse_args()

    from datetime import date

    if options.HLTB:
        logpath = r'\\99tt005\syslog'
        if options.HLTB == 'inner':
            logpath = r'\\99tt004\log'
         
        before = date(date.today().year, date.today().month, 1)
        from datetime import timedelta

        m = before - timedelta(days = 1)

        file = r'%s_%d%02d.logs.bak.tar' % (options.HLTB, 
                                               m.year, m.month)
        file = os.path.join('bak', file)
        if os.path.exists(file):
            print u'%s 已存在' % file
            sys.exit()

        cmd = '%s %s -tRf %s -b %s' % (__file__, logpath, file, 
                                      before.strftime('%Y%m%d')) 
        print cmd
        os.system(cmd)
        sys.exit()
    
    if len(args) < 1:
        print u'請指定日誌檔之根目錄'
        sys.exit()

    if not os.path.exists(args[0]):
        print u'日誌檔之根目錄不存在'
        sys.exit()       

    bak = r'%s.logs.bak.tar' % date.today().strftime('%Y%m%d')
    if options.file:
      bak = options.file

    if options.tar:
        import tarfile
        #import pdb;pdb.set_trace();
        tar = tarfile.TarFile(bak, 'w')
                
    #import pdb; pdb.set_trace()
    for f in os.listdir(args[0]):
        if match(f, options):
            p = os.path.join(args[0], f)
            print p
            if options.tar:
                tar.add(p)
                if options.remove:
                    os.remove(p)
    if options.tar:
        tar.close()
