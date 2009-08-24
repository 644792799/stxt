#!/usr/bin/python
# -*- encoding: utf-8 -*-

# Author: ����(Chowroc)
# Date: 2006-06-10

# 2006-06-06: ȷ�������ļ�������ʽ����ʵ�� get ����
# 2006-06-07: �Եݹ�ʵ�ֱ����滻
# 2007-02-02: ����

"""�ó������һ����ƽ�淽ʽ��ʾ�����������ļ���ȡ�û�����������á�
��Чѡ��У��Ӧ������Ӧ�ó����Լ������飬
ctree ֻ�����ȡ���ã�����һЩ�����Ľ���

* �����ļ���ʽ����(�ɲο� sysctl �� sysctl.conf �� postfix �� main.cf)��
fs_backup.format = "bid, btime, archive, type, list, host";
fs_backup.default = "full"; # comment
# more comment
# ��ʹ�� = �ָ�����ֵ�ԣ�ʹ�� "" ����ֵ��ʹ�� ; �ָ���¼
# ʹ�� # ע�ͣ����в���Ӱ��

* ѡ���ֵ��֧�ֶ���ģʽ��
test.long.value = "The value of the options
also support
multilines mode";

* ʹ�ñ�����
fs_backup.datadir = "/var/task/fs_backup";
fs_backup.tagfile = "$datadir/.tag";
# ��ʹ�þ���·����
# fs_backup.tagfile = "${fs_backup.datadir}/.tag";
# ������·��Ҫʹ�� {}

* ���ļ���ȡ����(δʵ��)���Ե����ĺ����򷽷�ʵ�ֽϺã�Ҳ���Ժ�����ʽ�ȽϺã���Ϊ�ɹ��ⲿ����

* ͨ���ʹ�� ��������ʽ(δʵ��)��ע���������֧������

* ��������֧��(δʵ��)

* һѡ���ֵ֧�֣�ʹ�ò���ָ��(δʵ��)

* ���� python ���ݽṹ������֧��(δʵ��)

* ���� shell ����֧��(δʵ��)

* ����ʱ�����֧�֣��� date ����� date -d '1 days ago' +%Y%m%d ��Ч��(δʵ��)

* �ṩӦ�ó���ʹ�� -o $option ʱ���õĽ�������(δʵ��)

* ֧�ִӱ�׼�������(δʵ��)

* ֧�ֲ���""�ŵ����(δʵ��)

* ֧�ֽ���ģʽ(δʵ��)

* ֧�� list ����(�൱�� ls)����ݹ�ģʽ(δʵ��)

* ֧������ģʽ��(������ǽ���)��ĳһѡ������ò���(δʵ��)

* ֧�� file faker(δʵ��)��

* !!! ���Դ��� list��Ҳ���Դ��� dict����ÿ��Դ���һ�� Class Config ��Ϊ������"""

import re
import os
import getopt
import sys

import logger
from pathtools import *

program = os.path.basename(sys.argv[0])
resplit = re.compile(r';\s*\n|;\s*(?!\\)#*.*\n|^\s*$|^\s*#.*$', re.M)
### separator = r';\s*\n|;\s*(?!\\)#*.*\n|^[\s\t]*$|^\s*#.*$'
# ^\s*$, empty line; ^\s*(?\\)#.*$, comment line
# rematch = re.compile(r'^\s*(.+)\s*(?!\\)=\s*(?!\\)"(.+)(?!\\)"\s*')

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'gsp:k:vh', 
			['config=', 'get', 'set', 'prefix=', 'key=', 'only-value', 'help'])

		confile = args[0]
		action = ''
		optmap = {}
		prefix = ''
		showopt = True
		for o, v in opts:
			if o in ['-g', '--get']:
				action = 'get'
			if o in ['-s', '--set']:
				action = 'set'
			if o in ['-p', '--prefix']:
				prefix = v
			if o in ['-k', '--key']:
				optmap[v] = ''
			if o in ['-v', '--only-value']:
				showopt = False
			if o in ['-h', '--help']:
				print usage
				sys.exit(0)

		# ctobj = CTree(confile, optmap, prefix)
		ctobj = CTree()
		if action == 'get':
			optmap = ctobj.get(confile, prefix, optmap)
		elif action == 'set':  pass
		else:
			print 'Empty or wrong action(get/set)'
			print usage
			sys.exit(0)

		if prefix:  prefix += '.'
		for key in optmap.keys():
			if showopt:  print '%s%s = "%s"' % (prefix, key, optmap[key])
			else:  print '%s' % optmap[key]

	except getopt.GetoptError, goEx:
		strerr = "getopt error: %s, %s" % (goEx.opt, goEx.msg)
		sys.stderr.write('%s\n' % strerr)
		# outlog.error(strerr)
		sys.exit(1)

	except IndexError:
		strerr = "Lack of config file name"
		print strerr
		# outlog.info(strerr)
		print usage
		sys.exit(0)

	except CTreeEx, ctEx:
		ctEx.logError(logerr=outlog)

if __name__ == '__main__':
	outlog = logger.get(program)
	usage = """program usage: %s [OPTIONS] config-file
	OPTIONS:
	-g|--get, ȡ������ѡ��
	-s|--set, ��������ѡ��
	-p|--prefix, ����ѡ���ǰ׺(Ĭ��Ϊ��)
	-k|--key, ����'prefix.key' ��Ϊʵ�ʵ�ѡ���
	-v|--only-value, ֻ��ӡѡ��ֵ
	-h|--help""" % program

	main()
	# try:
	#	main()
	# except CTreeEx, ctEx:
	#	ctEx.logError(logerr=outlog)
	# except Exception, Ex:  print Ex.__str__; outlog.error(Ex.__str__)
	# catch all
else:
	outlog = logger.get(__name__)
	usage = """module usage: %s""" % __name__

class CTreeEx:
	def __init__(self, errno=1, strerr='CTree,Exception'):
		self.errno = int(errno)
		self.strerr = str(strerr)
	# def logError(self):
	def logError(self, logerr=outlog):
		print >> sys.stderr, self.strerr
		if self.errno == 1:  logerr.error(self.strerr)
		elif self.errno == 127:  logerr.critical(self.strerr)

class CTree:
	def __init__(self):
		# self.confile = confile
		self.confile = ''
		self.prefix = ''
		self.optmap = {}

	def get(self, confile, prefix, optmap={}, flags=[]):
		# if type(confile) is file:
		#	self.confile = confile
		# else:
		#	self.confile = open(confile)
		self.confile = confile
		if prefix:
			self.prefix = prefix
		if optmap:
			if type(optmap) is list:
				optmap = dict(map(None, optmap, []))
			self.optmap = optmap
		self.prefix = normalize(self.prefix)
		if self.prefix:  self.prefix += '.'
		optemp = {}
		keymap = {}

		try:
			# self.config = resplit.split(self.confile.read())
			self.config = resplit.split(open(confile).read())
		except IOError, strerr:
			strerr = 'IOError: %s' % strerr
			raise CTreeEx(strerr=strerr)
		except TypeError, strerr:
			strerr = 'TypeError: %s' % strerr
			raise CTreeEx(strerr=strerr)

		try:
			for line in self.config:
				### print 'DEBUG: BOL, %s, EOL' % line
				# �˴� line ָһ�� key/value �ԣ�ʵ�ʿ����Ƕ���(����ģʽ)
				## mo = rematch.match(line, re.M|re.S)
				mo = re.match(r'^\s*(.+)\b\s*(?!\\)=\s*(?!\\)"(.+)(?!\\)"\s*', line, re.M|re.S)
				if not mo:  continue
				option = mo.group(1)
				keys = self.optmap.keys()
				# if option in [ self.prefix + key for key in self.optionmap.keys() ]:
				value = mo.group(2)
				for key in keys:
					### print '%s, %s' % (key, option)
					if 'r' in flags or 'regexp' in flags:
					# ģʽƥ��
						komo = re.match(self.prefix + key, option)
						if komo: keys.append(basename(option))
					elif option == self.prefix + key:
					# �ҵ�ƥ��
						self.optmap[key] = value
					else:  continue
					# δ�ҵ�ƥ��
					mo = re.match(r'\${\b(.+)\b}|\$(\w+)', value)
					if mo:
					# ���ڱ���
						if mo.group(1):  tk = mo.group(1)
						elif mo.group(2):  tk = self.prefix + mo.group(2)
						optemp[tk] = ''
						keymap[key] = tk
					break
			if optemp:
				### self.get(optemp, self.prefix, flags) ??????
				### cttemp = CTree(self.confile, optemp); cttemp.get()
				# *** file.tell() or make use of lines(self.config)? ***
				cttemp = CTree()
				optemp = cttemp.get(self.confile, self.prefix, optemp)
				# �ݹ�����Խ��ͱ���
				# ��Ϊʲôֱ�ӵ��������У�
				for key in keymap.keys():
					tk = keymap[key]
					if not optemp[tk]:
						strerr = 'No variable option ${%s} found in the configuration.' % tk
						raise CTreeEx(strerr=strerr)
					self.optmap[key] = re.sub(r'\${\b.+\b}|\$\w+', optemp[tk], self.optmap[key])

			return optmap
		except TypeError, strerr:
			raise CTreeEx(strerr=strerr)
