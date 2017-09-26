##  Anki extension for adding tags using keys: 4,5,6 are hard, medium, difficult respectively.  7 and 9 are 'impossible'.  Alternate keys: E,W,Q,R.  The keys 4,5,6 let you use one hand to review and tag at the same time using the keypad.  Keys 1,2,3 tell Anki when to show the card again, and Enter shows the answer.

from aqt import mw
from aqt.reviewer import Reviewer
from anki.hooks import wrap
from aqt.utils import tooltip


tags = ['easy', 'medium', 'hard', 'impossible']

def addThisTag(note, thisTag):
    note.addTag(thisTag)
    tooltip('Added tag "%s"' % thisTag)
    for t in tags:
        if t != thisTag: note.delTag(t)
    note.flush()

def keyHandler(self, evt, _old):
    key = unicode(evt.text())
    if key == "E" or key == "6":   #Add tag
        note = mw.reviewer.card.note()
        addThisTag(note, tags[0])
    if key == "W" or key == "5":   #Add tag
        note = mw.reviewer.card.note()
        addThisTag(note, tags[1])
    if key == "Q" or key == "4":   #Add tag
        note = mw.reviewer.card.note()
        addThisTag(note, tags[2])
    if key == "R" or key == "7" or key == "9":   #Add tag
        note = mw.reviewer.card.note()
        addThisTag(note, tags[3])
    else:
        return _old(self, evt)

Reviewer._keyHandler = wrap(Reviewer._keyHandler, keyHandler, "around")
