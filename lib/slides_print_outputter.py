# coding=utf-8
from __future__ import with_statement
import sys, os, re, unittest, stxt_parser
dir = ''
file = ''
template = ''
def disp(tree):
    return globals()['f_' + tree.type](tree)

def to_slides(_dir, _file):
    # make doctree
    global dir
    global file
    global template
    dir = _dir
    file = _file
    with open(r'd:\stxt\template\slides.html') as tfn:
        template = tfn.read()

    d = stxt_parser.parser.read(file)
    d.number_children()
    d.count_occurence()

    html = '<h2>投影片索引</h2>\n'
    for sect1 in d.children:
        html += '<h3><a href="%s">%s%s</a></h3>\n' % \
               (f_filename(sect1), f_section_number(sect1), sect1.title)
        disp(sect1)
    # write index.html
    fn = r'd:\stxt\structedtext\%s\index.html' % dir
    with open(fn, 'w') as f:
        f.write(template % \
                {'title': '投影片索引', 
                 'content': html
                })

def f_sect1(tree):
    global dir, template
    html = '<h2>%s</h2>\n' % tree.title

    sect2s = [sect2 for sect2 in tree.children if sect2.type == 'sect2']
    for sect2 in sect2s:
        html += disp(sect2)

    fn = r'd:\stxt\structedtext\%s\print_%s' % (dir, f_filename(tree))
    with open(fn, 'w') as f:
        f.write(template % \
                {'title': tree.title, 
                 'content': html
                })
    print 'produce %s' % fn

def f_sect2(tree):
    global dir, template
    html = '<h2>%s</h2>\n' % tree.title
    html += '<div id="content">'
    for c in tree.children:
        html += disp(c)
    html += '</div>'
    return html

def f_sect3(tree):
    html = '<h3>%s%s</h3>\n'% (f_section_number(tree), tree.title)
    for c in tree.children:
        html += disp(c)
    return html

def f_code(tree):
    return '<pre>%s</pre>\n' % tree.value

def f_table(tree):
    html = '<h4>表%s：%s</h4>\n'%(tree.occurence,    tree.title)
    if tree.children:
        html += '<table>\n'
        for row in tree.children:
            html += '<tr>\n' 
            for col in row.children:
                html += '<td>%s</td>\n' % col.value.encode('utf8')
            html += '</tr>\n' 
        html += '</table>\n'
    else:
        html += '<pre>%s</pre>\n' % tree.value 
    return html

def f_image(tree):
    html = '<img src="images/%s" alt="%s"' % (tree.name, tree.title)
    html += '<h4>%s</h4>\n' % tree.title
    return html

def f_para(tree):
    return '<p>\n' + tree.value + '</p>\n'

def f_l2para(tree):
    return '<p>\n' + tree.value + '</p>\n'

def f_list(tree):
    html = '<ul>\n'
    for c in tree.children:
        html += '<li>\n' + c.value 
        for np in c.children:
            html += disp(np)
        html += '</li>\n'
    html += '</ul>\n'
    return html

def f_olist(tree):
    html = '<ol>\n'
    for c in tree.children:
        html += '<li>' + c.value
        for np in c.children:
            html += disp(np)
        html += '</li>\n'
    html += '</ol>\n'
    return html

def f_dlist(tree):
    html = '<dl>\n'
    for c in tree.children:
        html += '<dt>%s</dt>\n' % c.value
        html += '<dd>'
        for np in c.children:
            html += disp(np)
        html += '</dd>'
    html += '</dl>\n'
    return html

def f_footnotes(tree):
    html = '<ul>\n'
    for c in tree.children:
        html += '<li>' + c.value+ '</li>\n'
    html += '</ul>\n'
    return html

def f_section_number(tree):
    ns = tree.section_number(3)
    w = ''
    for n in ns:
        w += str(n) + '.'
    return w

def f_filename(tree):
    fn = '_'.join([str(n) for n in tree.section_number(3)])
    if tree.name:
        fn = tree.name
    return '%s.html' % fn

if __name__ == '__main__':
    usage = os.path.basename(__file__) + " dir filename"
    try:
        to_slides(sys.argv[1], sys.argv[2])
    except IndexError:
        print usage