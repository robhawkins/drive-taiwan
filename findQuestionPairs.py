#encoding: UTF-8

from os.path import basename,dirname,splitext,isfile,join
from os import listdir
from convert import *
import os,argparse,errno
import csv


# This program finds questions that appear in both the car and moto driving test

# To do, if ever find dups: load Anki export file "All Decks.txt", copy labels from dups, apply them to the export, and import that to Anki

def main():
  scriptDir=os.path.dirname(os.path.realpath(__file__))
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--questionsdir', help='CSV question files directory (input).', default=scriptDir+'/expected-output/')
  parser.add_argument('-p', '--pairsfile', help='Duplicate questions file (output).', default=scriptDir+'/duplicate-questions.txt')
#  parser.add_argument('-i', '--inputlabels', help='Input labels file (Anki export).', default=scriptDir+'/input/All Decks.txt')
#  TO DO: Update code to work with this
  args = parser.parse_args()

  questionFiles = [join(args.questionsdir, f) for f in listdir(args.questionsdir) if isfile(join(args.questionsdir, f))]

  questions = {}
  duplicates = {}
  for csvFilename in questionFiles:
    with open(csvFilename,'r') as f:
      reader = csv.reader(f, delimiter='\t')
      for (qid,question,answer,blank,language,vehicle,signsrules,truechoice,tags) in reader:
        #print(qid)
        if question not in list(questions):
          questions[question] = [qid]
        else:
          questions[question].append(qid)
          duplicates[question] = questions[question]



#    qfile = QuestionFile(filebase=splitext(basename(csvFilename))[0])
  for q in duplicates.keys():
    print(q)
    print('\t',end='')
    print(duplicates[q])
    print()




if __name__ == '__main__':
  main()
