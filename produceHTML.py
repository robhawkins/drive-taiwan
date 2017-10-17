#encoding: UTF-8

from os.path import basename,dirname,splitext,isfile,join
from os import listdir
from convert import warning, mkdir_p
from shutil import copy
import glob
import os,argparse,errno
import csv
import re
import sys


# This program prints questions in HTML format along with links and difficulty labels


columns_full = ['#', 'ID', 'Question', 'Question2', 'A', 'Rank', 'Rules or Signs', 'True/False or Choice','DMV #', 'Comments']
columns_fuller = ['#', 'ID', 'Question', 'Question2', 'Answer', 'Rank', 'Rules or Signs', 'True/False or Choice','DMV #', 'Comments']

selector = [ {'i': '4', 'label': columns_fuller[4], 'id': 'ans-drop', 'options': ['X','O','1','2','3'], 'opt-names': ['X','O','1','2','3'] },
             {'i': '5', 'label': columns_fuller[5], 'id': 'rank-drop', 'options': ['1','2','3','4', 'n/a'], 'opt-names': ['1 - very hard', '2 - hard', '3 - medium', '4 - easy', 'n/a'] },
             {'i': '6', 'label': columns_fuller[6], 'id': 'rs-drop', 'options': ['rules', 'signs'], 'opt-names': ['rules', 'signs'] },
             {'i': '7', 'label': columns_fuller[7], 'id': 'tf-drop', 'options': ['true/false', 'choice'], 'opt-names': ['true/false', 'choice'] }]


def main():
  scriptDir=os.path.dirname(os.path.realpath(__file__))
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--questionsdir', help='CSV question files directory (input).', default=scriptDir+'/output/')
  parser.add_argument('-l', '--language', required=True, choices=['english','chinese','vietnamese','khmer','japanese','indonesian','thai','burmese'])
  parser.add_argument('-v', '--vehicle', required=True, choices=['car','moto','mech'])
  parser.add_argument('-e', '--export', type=argparse.FileType('r'), default=scriptDir+'/input/All Decks.txt', help='Export of all decks.  Contains a comments field.')
  parser.add_argument('-a', '--ankimedia', help='Path to anki media folder.  Copy images from there', default=os.environ['HOME']+'/Documents/Anki/Taiwan Driver/collection.media/')
  parser.add_argument('-o', '--outputhtml', help='Output html folder.', default=scriptDir+'/output-html')
  args = parser.parse_args()

  questionFiles = getQuestionFiles(args.questionsdir, args.language, args.vehicle)

  if (len(questionFiles) == 0):
    warning("Found 0 files for the selected language and vehicle.  Exiting.")
    sys.exit()
  elif (len(questionFiles) != 4):
    warning("Found "+str(len(questionFiles))+" question files.  Expected 4.  Continuing anyway.")

  reader = csv.reader(args.export, delimiter='\t')

  comments = {}

  for row in reader:
    qid = row[0]
    rest = row[1:]
    comments[qid] = rest[-2]

  tf = {'choice':'choice', 'true':'true/false'}
  diff = {'easy':'4', 'medium':'3', 'hard':'2', 'impossible':'1', '':'n/a'}

  oppLang = 'english'
  if args.language == 'english':
    oppLang = 'chinese'

  questionFilesOpp = getQuestionFiles(args.questionsdir, oppLang, args.vehicle)
  questionsOpp = {}


  for csvFilename in questionFilesOpp:
    with open(csvFilename,'r') as f:
      reader = csv.reader(f, delimiter='\t')
      for (qid,question,answer,category,language,vehicle,signsrules,truechoice,tags) in reader:
        split = qid.split('-')
        number = split[-1]
        refid = '-'.join(split[2:])
        question = question.replace('<img src="', '<img src="media/')
        questionsOpp[refid] = question


  columns_full[3] = 'Question ('+oppLang.capitalize()+')'
  columns_fuller[3] = columns_full[3]


  link_info = {'english': {'txt': '中文', 'file':args.outputhtml+'/chinese-'+args.vehicle+'-more.html'},
               'chinese': {'txt': 'eng', 'file':args.outputhtml+'/english-'+args.vehicle+'-more.html'},
              }

  out_simple = open(args.outputhtml+'/'+args.language+'-'+args.vehicle+'.html', 'w')
  out =        open(args.outputhtml+'/'+args.language+'-'+args.vehicle+'-more.html', 'w')

  media = args.outputhtml+'/media'
  mkdir_p(media)

  for file in glob.glob(args.ankimedia+'/'+args.language+'-'+args.vehicle+'*'):
    copy(file, media)


  title=args.vehicle.capitalize()+'/'+args.language.capitalize()+" Taiwan Driver's Test"
  out_write('<html><head><title>'+title+'</title>', [out, out_simple])
  out_write("""<style>
    table {width: 100%}
    th, tr, td {page-break-inside: avoid;}
    th, td {border: 1px solid black;}
    th {padding: 15px;}
    td {padding: 5px 8px;}
    h2 {text-align:center;}
    img {max-height: 187px;}
    #selectors select { position: relative!important; }
    .btn-group { display: inline!important; float:none!important; }
    body {margin: 5px !important; }
  </style>""", [out, out_simple])

  out_write('<link rel="stylesheet" type="text/css" href="js-css/datatables.css">', [out, out_simple])
  out_write('<link rel="stylesheet" type="text/css" href="js-css/bootstrap.css">', [out, out_simple])
  out_write('<link rel="stylesheet" type="text/css" href="js-css/bootstrap-multiselect.css">', [out, out_simple])
  out_write('<script type="text/javascript" charset="utf8" src="js-css/datatables.js"></script>', [out, out_simple])
  out_write('<script type="text/javascript" charset="utf8" src="js-css/bootstrap.js"></script>', [out, out_simple])
  out_write('<script type="text/javascript" charset="utf8" src="js-css/bootstrap-multiselect.js"></script>', [out, out_simple])

  out_write("""<script type='text/javascript' charset='utf8'>
    $(document).ready( function () {
        $('table#questions').DataTable({
           sDom: 'Bif',
           paging: false,
           dom: 'Bfrtip',\n""", [out, out_simple])
  out_write("""
           order: [[ 1, 'asc' ]],
           """, [out])
  out_write("""
           order: [[ 5, 'asc' ]],
           """, [out_simple])
  out_write("""
           buttons: [ { extend: 'colvis', text: 'Hide/Show Columns' },
                      { extend: 'print',  exportOptions: { stripHtml: false, columns: ':visible' } }],
          columns: [
           """,[out, out_simple])
  out_write("""
                { "visible": false },
                { "visible": false },
                { "visible": true },
                { "visible": false },
                { "visible": true },{ "visible": true },{ "visible": false },{ "visible": false },{ "visible": false },{ "visible": false }
  """, [out_simple])
  out_write("""
                { "visible": false },
                { "visible": true },
                { "visible": true },
                { "visible": true },
                { "visible": true },{ "visible": true },{ "visible": false },{ "visible": false },{ "visible": false },{ "visible": true }
  """, [out])

  out_write("""
                     ],

        });
        function multiselect(selector, col, label) {
          $(selector).multiselect({
              nonSelectedText: label,
              allSelectedText: label,
              buttonText: function(options, select) {
                return label;
              },
              onChange: function(element, checked) {

                var opts = $(selector+' option:selected');

                var selected = [];
                $(opts).each(function(index, opt) {
                  selected.push([$(this).val()]);
                });

                var regex = selected.join("|");

                $('table').DataTable().column(col).search(
                  regex, true, true
                ).draw();
              }
          });
        }\n""", [out, out_simple])
  for c in selector:
      out_write("multiselect('#"+c['id']+"',"+str(c['i'])+",'"+c['label']+"')\n", [out, out_simple])

  out_write("""
    });
  </script>""", [out, out_simple])

  out_write('</head>', [out, out_simple])
  out_write('<body><h2>'+title+'</h2>', [out, out_simple])
  out_write('<p> Ranks - 1 = very hard, 2 = hard, 3 = medium, 4 = easy', [out, out_simple])

  string='<div id="selectors" style="padding: 10px 0; margin-bottom: 50px">'

  for c in selector:
    string += '<span style="float: left; margin-left: 10px;">'
    string += '<select id='+c['id']+' multiple="multiple">\n'
    string += '<optgroup label=''>\n'
    for i, opt in enumerate(c['options']):
      string += '<option value="'+opt+'">'+c['opt-names'][i]+'</option>\n'
    string += '</optgroup></select><br>\n'
    string += '</span>'
  string += '</div>'
  out_write(string, [out, out_simple])


  out_write('<table id="questions" class="display" width="100%"><thead> <tr>', [out, out_simple])

  out_write(columns(columns_full, True), [out, out_simple])


  out_write('</tr></thead><tbody>', [out, out_simple])
  i = 0;
  for csvFilename in questionFiles:
    with open(csvFilename,'r') as f:
      reader = csv.reader(f, delimiter='\t')
      for (qid,question,answer,category,language,vehicle,signsrules,truechoice,tags) in reader:
        i += 1
        split = qid.split('-')
        number = split[-1]
        refid = '-'.join(split[2:])
        out_write('<tr id="'+refid+'">', [out, out_simple])
        question = question.replace('<img src="', '<img src="media/')
        #link = '<a href="'+link_info[args.language]['file']+'#'+refid+'">'+link_info[args.language]['txt']+'</a>'
        lookup = refid
        ref_base = '-'.join(split[2:-1])
        int_num = int(number)
        if re.match('rules-true', refid):
          if int_num == 165:
            if args.language == 'english':
              lookup = 'jibberish'
            elif args.language == 'chinese':
              lookup = ref_base+'-'+str(int_num+1)
          elif int_num > 165:
            if args.language == 'english':
              lookup = ref_base+'-'+str(int_num-1)
            elif args.language == 'chinese':
              lookup = ref_base+'-'+str(int_num+1)


        out_write(columns([str(i), args.language+'-'+refid, question,questionsOpp.get(lookup, ''),
                           answer,diff[tags],signsrules,tf[truechoice],number,comments[qid]]),
                  [out, out_simple])

        out_write('</tr>', [out, out_simple])
  out_write('</tbody></table></body></html>', [out, out_simple])
  out.close()
  out_simple.close()
  print("Finished writing HTML files into "+args.outputhtml)

def getQuestionFiles(qdir, language, vehicle):
  return sorted([join(qdir, f) for f in listdir(qdir) if isfile(join(qdir, f)) and re.match('^'+language+'-'+vehicle+'-', f)])

def columns(cols, th=False):
  string = ''
  for c in cols:
    if (th):
      string += '<th>'+c+'</th>'
    else:
      string += '<td>'+c+'</td>'
  return string

def out_write(string, dest):
  for d in dest:
    d.write(string+'\n')


class question(object):
  def __init__(self,number='',question='',answer='',category='', qfile=''):
    pass


if __name__ == '__main__':
  main()
