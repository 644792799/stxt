# coding=utf8
import sys
class DocTreeNode(object):
  def __init__(self, type, value='', title=''):
    self.type, self.value, self.title = type, value, title
    self.parent, self.children = None, []
    self.number = None     # It's section number
    self.occurence = None  # It's table number
  def __str__(self):
    m = "%s:\n[\n%s\n]" % (self.type, self.value)
    for c in self.children:
      m+=str(c)
    return m
  def __repr__(self):
    return str(self)
  def append(self, *nodes):
    for n in nodes: 
      n.parent = self
      self.children.append(n)
    return self
  def isRoot(self):
    return self.parent is None
  def height(self):
    if self.isRoot(): return 0
    c, h = self, 0
    while c.parent:
      c = c.parent
      h += 1
    return h

  def _dfs(self, unvisited):
    for c in self.children:
      c._dfs(unvisited)
    unvisited.append(self)

  def dfs(self):
    '''depth-first search
         It calls _dfs() to construct a list of nodes in dfs order, then
         it enumerates the list to implement the generator.
       TODO: 
         Modify it not constructing node first, just find the next
         node on demand.
    '''
    unvisited = []
    self._dfs(unvisited)
    for n in unvisited:
      yield n

  def number_children(self):
    cs = self.children
    if self.type in ('book'):
      for i, c in enumerate([c for c in cs if c.type == 'sect1']):
        c.number = i + 1
        c.number_children()
    elif self.type in ('sect1'):
      for i, c in enumerate([c for c in cs if c.type == 'sect2']):
        c.number = i + 1
        c.number_children()
    elif self.type in ('sect2'):
      for i, c in enumerate([c for c in cs if c.type == 'sect3']):
        c.number = i + 1

  def section_number(self, level=0):
    '''Return a list of section numbers by level.
    '''
    if self.number is None: return '' 
    else: 
      if self.parent.number is None: return [self.number]
      elif level == 0: return [self.number]
      else: 
        ns = self.parent.section_number(level-1)
        ns.append(self.number)
        return ns

  def _count_occurence(self, type, o=0):
    for c in self.children:
      if c.type in [type]:
        o = o+1
        c.occurence = o
      o = c._count_occurence(type, o)
    return o

  def count_occurence(self):
    for type in ['code', 'table']:
      if self.type in [type]:
        o = o+1
        self.occurence = o
      self._count_occurence(type)

  def print_type_tree(self, level_limit=10):
    if self.height() < level_limit:
      print '*' * self.height() + self.type
    for c in self.children: c.print_type_tree(level_limit)

  def print_postfix_tree(self):
    for c in self.children: c.print_postfix_tree()
    print '*' * self.height() + self.type

  def print_tree(self):
    out = '+' * self.height() + self.type + '[' + self.name + ']' \
           +'#'+str(self.occurence)+'#' + self.section_number() + self.title + '\n'
    for c in self.children: out += c.print_tree()
    return out