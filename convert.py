#encoding: UTF-8
from __future__ import division
from __future__ import print_function
from functools import wraps
import inspect
from copy import deepcopy
from bs4 import BeautifulSoup
from os.path import basename,dirname,splitext
from shutil import copy2
from subprocess import call
import os,argparse,errno
import sys
import re
import glob
import pdb
from natsort import natsorted

## This program converts Taiwan driver's test PDF files into csv for import as Anki flashcards. It can optionally copy images to Anki media folder

##TODO : make use of optional arguments to override setting of options based on filename: scooter/car, language, signs/rules

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--file', required=True)
  #parser.add_argument('-t', '--type', required=False) ## scooter or car
  #parser.add_argument('-l', '--lang', required=False) ## [eng|chn|...]
  #parser.add_argument('-q', '--qualifier', required=True) ## [signs|rules]-[choice|true]
  parser.add_argument('-a', '--anki', required=False) ## path to anki media folder.  if set, copy images here
  parser.add_argument('-w', '--working', required=False, default='./') ## working directory, where output files will be stored.  Defaults to ./
  args = parser.parse_args()

  filename = splitext(basename(args.file))
  base = filename[0]
  ext = filename[1]
  xmlfile = args.file

  qfile = theqfile(filebase=base)

  workingDir = args.working + '/' + qfile.type.getFileID()
  mkdir_p(workingDir)

  if ext == '.pdf':
    xmlfile = workingDir + '/' + base + '.xml'
    opts = ['pdftohtml', '-xml']
    if not args.anki:
      opts.append('-i')
    opts.extend([args.file, xmlfile])
    FNULL = open(os.devnull, 'w')
    call(opts,stdout=FNULL)
  elif ext != '.xml':
    warning("File [-f file] is not .xml or .pdf")
    sys.exit()

  filehandler = open(xmlfile)

  soup = BeautifulSoup(filehandler,'lxml')

  current_q = qfile.newQuestion()

  state = ''
  qnum = 0

  ignorable_lines = [ '^題號$',
                      '^答案$',
                      '^題目圖示$',
                      '^題\s*目$',
                      '^第\d+頁/共\d+頁$',
                      '^機車標誌、標線、號誌是非題$',
                      '^機車標誌、標線、號誌選擇題$',
                      '^機車法規選擇題$',
                      '^分類$',
                      '^編號$',
                      '^機車法規是非題$',
                      '^汽車法規選擇題$',
                      '^【英文】$',
                    ]


  for page in soup.findAll('page'):
    pageheight = int(page['height'])
    pagewidth = int(page['width'])
    for text in page.findAll('text'):
      top_pos = float(text['top']) / pageheight
      left_pos = float(text['left']) / pagewidth
      txt = text.get_text()
      txt_strip = txt.strip()
      txt_nospace = re.sub('\s+','',txt.encode('utf-8'))
      if not txt:
        continue
      skip = False
      for ignore in ignorable_lines:
        if re.match(ignore, txt_nospace):
          skip = True
          continue
      if skip:
        if current_q:
          current_q.question = re.sub('\n','',current_q.question)
          current_q = qfile.newQuestion()
        continue
      if re.match('^[0-9]{3}$',txt_strip):
        state = 'found_qnum'
        qnum += 1
        qnum_i = qnum-1
        if current_q:
          current_q.question = re.sub('\n','',current_q.question)
          current_q = qfile.newQuestion()
        current_q.number = qnum
        continue
      elif state == 'found_qnum':
        if re.match('^[0-9OX]$',txt_strip) or txt_strip == u'Ｘ' or txt_strip == u'Ｏ':
          state = 'found_ans'
          if current_q.answer != '':
            warning("%d: Answer being overwritten" % (qnum))
          if txt_strip == u'Ｏ': txt_strip = 'O'
          elif txt_strip == u'Ｘ': txt_strip = 'X'
          current_q.answer = txt_strip
        else:
          warning("%d: Answer not found after question number" % (qnum))
      elif state == 'found_ans' and not re.match('^[0-9]+$',txt_strip):
        current_q.question += txt
      elif re.match('^[0-9]{1,2}$',txt_strip) and left_pos > 0.75:
        current_q.category = txt_strip
  filehandler.close()

  qfile.writeCSV(args.working)
  if args.anki:
    qfile.copyImages(workingDir, args.anki)





def initializer(func):
  names, varargs, keywords, defaults = inspect.getargspec(func)

  @wraps(func)
  def wrapper(self, *args, **kargs):
    for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
      setattr(self, name, arg)

    for name, default in zip(reversed(names), reversed(defaults)):
      if not hasattr(self, name):
        setattr(self, name, default)

    func(self, *args, **kargs)

  return wrapper

class qfiletype(object):
  @initializer
  def __init__(self, vehicle='', signsrules='', truechoice='',language=''):
    pass
  def getFileID(self):
    return self.language+'-'+self.vehicle+'-'+self.signsrules+'-'+self.truechoice
  def getAttributes(self):
    return (self.language, self.vehicle, self.signsrules, self.truechoice)

class theqfile(object):
  global filemap
  filemap = {
              '機車法規是非題-中文' : qfiletype('motorcycle', 'rules', 'true','chinese'),
              '機車法規選擇題-中文' : qfiletype('motorcycle', 'rules', 'choice', 'chinese'),
              '機車標誌是非題-中文' : qfiletype('motorcycle', 'signs', 'true','chinese'),
              '機車標誌選擇題-中文' : qfiletype('motorcycle', 'signs', 'choice','chinese'),
              'Rules-True or False／English〈機車法規是非題-英文〉' : qfiletype('motorcycle', 'rules', 'true', 'english'),
              'Rules-Choice／English〈機車法規選擇題-英文〉' : qfiletype('motorcycle', 'rules', 'choice', 'english'),
              'Signs-True or False／English〈機車標誌是非題-英文〉' : qfiletype('motorcycle', 'signs', 'true', 'english'),
              'Signs-Choice／English〈機車標誌選擇題-英文〉' : qfiletype('motorcycle', 'signs', 'choice', 'english'),
              'Rules-Choice／English(汽車法規選擇題-英文)' : qfiletype('car', 'rules', 'choice', 'english'),
              'Rules-True or False／English(汽車法規是非題-英文)' : qfiletype('car', 'rules', 'true', 'english'),
              'Signs-Choice／English(汽車標誌選擇題-英文)' : qfiletype('car', 'signs', 'choice', 'english'),
              'Signs-True or False／English(汽車標誌是非題-英文)' : qfiletype('car', 'signs', 'true', 'english'),
            }

  @initializer
  def __init__(self,type='',language='',filebase='',questions=[],images=[]):
    if not language and not filebase:
      warning('qfile(): language and filebase not specified')
    if not language and filebase:
      self.language = filemap[filebase].language
    if not type and filebase:
      self.type = filemap[filebase]
    if not self.language:
      warning('qfile(): language not set')
    if not self.type:
      warning('qfile(): type not set')
      sys.exit()
  def newQuestion(self):
    q = question(qfile=self)
    self.questions.append(q)
    return q
  def getQuestion(self,i):
    return self.questions[i]
  def prettyAll(self):
    self.finished()
    return '\n'.join(q.pretty() for q in self.questions)
  def writeCSV(self, dir):
    file = dir + '/' + self.type.getFileID() + '.csv'
    f = open(file, 'w')
    f.write(self.prettyAll())
    f.close()
    print("Wrote file: "+file)
  def finished(self):
    lastq = self.questions[-1]
    if not lastq:
      del self.questions[-1]
    if self.type.signsrules == 'signs':
      self.populateImageNames()
      for i,q in enumerate(self.questions):
        q.question = '<img src="'+self.images[i]+'"><br>'+q.question
    self.finished_called = 1
  def copyImages(self, work, anki):
    if not self.finished_called:
      self.finished()
    images = glob.glob(work + '/' + self.filebase + '*png')
    for i,f in enumerate(natsorted(images)):
      copy2(f, anki + '/' + self.images[i])
  def populateImageNames(self):
    self.images = []
    newbase = self.type.getFileID()
    for i,q in enumerate(self.questions):
      qnum = i+1
      imagefile = newbase+'-'+str(qnum)+'.png'
      self.images.append(imagefile)

class question(object):
  @initializer
  def __init__(self,number='',question='',answer='',category='', qfile=''):
    pass
  def __eq__(self, other):
    copy_self = deepcopy(self)
    copy_other = deepcopy(other)
    copy_self.qfile = ''
    copy_other.qfile = ''
    return (isinstance(copy_other, copy_self.__class__) and copy_self.__dict__ == copy_other.__dict__)
  def __ne__(self, other):
    return not self.__eq__(other)
  def __bool__(self):
    empty = question()
    mycopy = deepcopy(self)
    mycopy.qfile = ''
    return self != empty
  __nonzero__ = __bool__
  def add_question_text(self):
    pass
  def pretty(self):
    if not self.number or not self.question or not self.answer:
      warning("pretty(): Number, question or answer not set before printing")
    pretty_question = self.question
    if self.qfile.type.truechoice == 'choice':
      pretty_question = re.sub(r'\( *([123]) *\)',r'<br>(\1) ',self.question)
    row = [self.qfile.type.getFileID()+'-'+str(self.number).zfill(3),pretty_question,self.answer,self.category]
    row.extend(self.qfile.type.getAttributes())
    return '\t'.join(row).encode('utf-8')

def warning(*objs):
  print("WARNING: ", *objs, file=sys.stderr)

def mkdir_p(path):
  try:
    os.makedirs(path)
  except OSError as exc: # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
      pass
    else: raise


if __name__ == '__main__':
  main()
