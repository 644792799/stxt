# coding=utf
import os, sys, unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.booker_lexer import lexer

class UnitTest(unittest.TestCase):
    def setUp(self):
        lexer.begin('INITIAL')

    def testFOOTNOTE(self):
        case = r'.. [#] this is a footnote'
        lexer.input(case)
        lexer.lineno = 1
        t = lexer.token()
        self.assertEqual(1, t.lexer.lineno)
        self.assertEqual('FOOTNOTE', t.type)
        self.assertEqual('this is a footnote', t.value.value)
        
        case = '''.. [KDE1989] Knuth, Donald E., *The TeXbook*, Reading,
Massachusetts: Addison-Wesley, 1989.'''
        lexer.input(case)
        lexer.lineno = 1
        t = lexer.token()
        self.assertEqual(1, t.lexer.lineno)
        self.assertEqual('CITATION', t.type)
        self.assertEqual('Knuth, Donald E., *The TeXbook*, Reading,', 
                          t.value.value)

        t = lexer.token()
        self.assertEqual(2, t.lexer.lineno)
        self.assertEqual('LINE', t.type)

    def testINSERT(self):
        case = r'table[test]'
        lexer.input(case)
        lexer.lineno = 1
        t = lexer.token()
        self.assertEqual(1, t.lexer.lineno)
        self.assertEqual('INSERT', t.type)
        self.assertEqual('table', t.node_type)
        self.assertEqual('test', t.name)
    
    def testHEAD(self):
        case = 'image[name].this is a image title'
        lexer.input(case)
        tok = lexer.token()
        self.assertEqual(tok.type, 'IMAGE')
        self.assertEqual(tok.value.name, 'name')
        self.assertEqual(tok.value.title, 'this is a image title')

        case = 'question[name].this is a question title'
        lexer.input(case)
        tok = lexer.token()
        self.assertEqual('QUESTION', tok.type,)

        case = 'define[name].this is a define title'
        lexer.input(case)
        tok = lexer.token()
        self.assertEqual('DEFINE', tok.type)

        case = 'theorem[name].this is a theorem title'
        lexer.input(case)
        tok = lexer.token()
        self.assertEqual('THEOREM', tok.type)

        case = 'proof.'
        lexer.input(case)
        tok = lexer.token()
        self.assertEqual(tok.type, 'PROOF')

        case = 'answer.'
        lexer.input(case)
        tok = lexer.token()
        self.assertEqual(tok.type, 'ANSWER')
    
    def testSEP(self):
        case = '''=========
---------
~~~~~~~~~
*********
^^^^^^^^^
::
====== ======
'''
        lexer.input(case)
        t = lexer.token()
        self.assertEqual('H1SEP', t.type)

        t = lexer.token()
        self.assertEqual('H2SEP', t.type)

        t = lexer.token()
        self.assertEqual('H3SEP', t.type)

        t = lexer.token()
        self.assertEqual('H4SEP', t.type)

        t = lexer.token()
        self.assertEqual('H5SEP', t.type)

        t = lexer.token()
        self.assertEqual('CODESEP', t.type)

        t = lexer.token()
        self.assertEqual('TABLESEP', t.type)

    def testEMPTYLINE(self):
        case = '''
    
'''
        lexer.input(case)
        t = lexer.token()
        self.assertEqual(2, t.lexer.lineno)
        self.assertEqual('EMPTYLINE', t.type)

        t = lexer.token()
        self.assertEqual(3, t.lexer.lineno)
        self.assertEqual('EMPTYLINE', t.type)

    def testInclude(self):
        case = r'<d:\stxt\lib\db\sql.stx>'
        lexer.input(case)
        self.assertRaises(IOError, lexer.token)

        case = r'<test.stx>'
        lexer.input(case)
        tok = lexer.token()
        self.assertEqual('test.stx', tok.lexer.file)
        self.assertEqual('LINE', tok.type)
        tok = lexer.token()
        self.assertEqual('H1SEP', tok.type)

        # lexer.input should reset include_lexer as None
        case = '普通行'
        lexer.input(case)
        t = lexer.token()
        self.assertEqual(1, t.lexer.lineno)
        self.assertEqual('LINE', t.type)

    def testOL(self):        
        case = '''#. 普通條列
  1. 一層縮排條列
    #. 二層縮排條列
      12. 三層縮排條列
        3. 四層縮排條列
          #. 五層縮排條列
        '''
        lexer.input(case)
        lexer.lineno = 1
        t = lexer.token()
        self.assertEqual(1, t.lexer.lineno)
        self.assertEqual('OL', t.type)
        self.assertEqual('#', t.value.number)
        self.assertEqual('普通條列', t.value.value)

        t = lexer.token()
        self.assertEqual(2, t.lexer.lineno)
        self.assertEqual('L1OL', t.type)
        self.assertEqual('1', t.value.number)
        self.assertEqual('一層縮排條列', t.value.value)

        t = lexer.token()
        self.assertEqual(3, t.lexer.lineno)
        self.assertEqual('L2OL', t.type)
        self.assertEqual('#', t.value.number)
        self.assertEqual('二層縮排條列', t.value.value)

        t = lexer.token()
        self.assertEqual(4, t.lexer.lineno)
        self.assertEqual('L3OL', t.type)
        self.assertEqual('12', t.value.number)
        self.assertEqual('三層縮排條列', t.value.value)

        t = lexer.token()
        self.assertEqual(5, t.lexer.lineno)
        self.assertEqual('L4OL', t.type)
        self.assertEqual('3', t.value.number)
        self.assertEqual('四層縮排條列', t.value.value)

        t = lexer.token()
        self.assertEqual(6, t.lexer.lineno)
        self.assertEqual('L5OL', t.type)
        self.assertEqual('#', t.value.number)
        self.assertEqual('五層縮排條列', t.value.value)

 
    def testLI(self):        
        case = '''* 普通條列
  * 一層縮排條列
    * 二層縮排條列
      * 三層縮排條列
        * 四層縮排條列
          * 五層縮排條列
        '''
        lexer.input(case)
        lexer.lineno = 1
        t = lexer.token()
        self.assertEqual(1, t.lexer.lineno)
        self.assertEqual('LI', t.type)
        self.assertEqual('普通條列', t.value.value)

        t = lexer.token()
        self.assertEqual(2, t.lexer.lineno)
        self.assertEqual('L1LI', t.type)
        self.assertEqual('一層縮排條列', t.value.value)

        t = lexer.token()
        self.assertEqual(3, t.lexer.lineno)
        self.assertEqual('L2LI', t.type)
        self.assertEqual('二層縮排條列', t.value.value)

        t = lexer.token()
        self.assertEqual(4, t.lexer.lineno)
        self.assertEqual('L3LI', t.type)
        self.assertEqual('三層縮排條列', t.value.value)

        t = lexer.token()
        self.assertEqual(5, t.lexer.lineno)
        self.assertEqual('L4LI', t.type)
        self.assertEqual('四層縮排條列', t.value.value)

        t = lexer.token()
        self.assertEqual(6, t.lexer.lineno)
        self.assertEqual('L5LI', t.type)
        self.assertEqual('五層縮排條列', t.value.value)

    def testLine(self):        
        case = '''普通行
  一層縮排
    二層縮排
      三層縮排
        四層縮排
          五層縮排
        '''
        lexer.input(case)
        lexer.lineno = 1
        t = lexer.token()
        self.assertEqual(1, t.lexer.lineno)
        self.assertEqual('LINE', t.type)
        self.assertEqual('普通行', t.value.value)
        self.assertEqual(0, t.value.level)

        t = lexer.token()
        self.assertEqual(2, t.lexer.lineno)
        self.assertEqual('LINE', t.type)
        self.assertEqual('一層縮排', t.value.value)
        self.assertEqual(1, t.value.level)

        t = lexer.token()
        self.assertEqual(3, t.lexer.lineno)
        self.assertEqual('LINE', t.type)
        self.assertEqual('二層縮排', t.value.value)
        self.assertEqual(2, t.value.level)

        t = lexer.token()
        self.assertEqual(4, t.lexer.lineno)
        self.assertEqual('LINE', t.type)
        self.assertEqual('三層縮排', t.value.value)
        self.assertEqual(3, t.value.level)

        t = lexer.token()
        self.assertEqual(5, t.lexer.lineno)
        self.assertEqual('LINE', t.type)
        self.assertEqual('四層縮排', t.value.value)
        self.assertEqual(4, t.value.level)

        t = lexer.token()
        self.assertEqual(6, t.lexer.lineno)
        self.assertEqual('LINE', t.type)
        self.assertEqual('五層縮排', t.value.value)
        self.assertEqual(5, t.value.level)

if __name__ == '__main__':
     unittest.main()
#    tests = unittest.TestSuite()
#    tests.addTest(UnitTest("testEMPTYLINE"))
#    tests.addTest(UnitTest("testLine"))
#    tests.addTest(UnitTest("testLI"))
#    tests.addTest(UnitTest("testHSEP"))
#    tests.addTest(UnitTest("testINSERT"))
#    runner = unittest.TextTestRunner()
#    runner.run(tests)