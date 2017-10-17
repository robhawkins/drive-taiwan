## Description

This is a Python tool for converting the Taiwan driver's test study data from PDF to CSV for import into an Anki deck.

This repo also stores difficulty labels for questions that I've marked up over time. See the Difficulty section below

The code can also produce HTML output for printing and reviewing of questions outside of Anki.

## Motivation and Goal

The motivation for making this was to practice writing some Python, help people study more efficiently for the test, and allow updates by rerunning this code in the event of changes made by the DMV.

The goal is to (1) identify the harder questions and (2) make studying them easier.

Some of the issues with the existing test and resources are,

  * There are now 1,600 questions for the car and scooter tests.  Before July 2015 there were only 600
  * Most questions are easy, but there are enough hard ones that it is easy to fail the test unless you review them
  * It is difficult to identify and focus on studying the hard questions
  * Study material consists of all possible questions rather than a more concise presentation of what you should know

## Requirements

This has been tested under Ubuntu, OS X, Python 3, and poppler 0.34.0.  Beautiful Soup, natsort and Poppler's pdftohtml are required.

## How to use

The basic way to run the program is:

```
./genAll.sh
```

The code will create a set of CSV and HTML files for the supported languages and tests (currently English and Chinese, car and scooter tests)

The file `input/All Decks.txt` is a txt export of all decks from Anki including manually applied difficulty labels as tags ranked easy, medium, hard and impossible.

## Issues

  * On Windows, you may need to set the language, test type, and question type manually since filenames may be stored under a different encoding than expected, and these settings are determined based on the filename.

## Study suggestions

See the Anki shared deck [Taiwan Driver's License - English - Motorcycle - 2015/07][t]

[t]: https://ankiweb.net/shared/info/1274417947

## Data source

  * [PDF files on the Taiwan DMV website][p]
  * [Online quiz][q]

[p]: http://www.thb.gov.tw/sites/ch/modules/download/download_list?node=cc318297-734e-42f0-9524-284801e7064d&c=63e0f1f5-4574-4545-a6fe-987df50ee75f
[q]: https://www.mvdis.gov.tw/m3-simulator-drv/

## Difficulty

* impossible - must be memorized, my intuition gives the wrong or no clear answer, or this is part of a group of questions, one of which is hard
* hard - i might get this wrong without studying
* medium - i could see how someone could get this wrong, or the wording is strange and could throw you off during a timed test
* easy - the answer is intuitive

## Examples

Questions with answers like 1, 2, or 3 years, or 100, 200, 300 meters, are all ranked medium or hard

Aside from those, if the possible answers are similar, and the actual answer is a likely extreme of the question, that question will be marked easy.  For example,

What happens to those who use counterfeit, forged, or illegally obtained license plates:

(1) they will be fined and their license will be revoked
(2) their vehicle registration will be suspended and their license plates will be confiscated
(3) they will be fined, their license will be revoked, their vehicle registration will be suspended, and their license plates will be confiscated.

Answer is (3).  The question is marked easy since the answers are similar and (3) is the most likely extreme.

### Impossible

If an accident takes place on a road with a speed limit over 50 km per hour, how many meters behind the vehicle are the drivers required to place a vehicle breakdown warning sign?

(1) 50-100 meters.
(2) 30-100 meters.
(3) 5-30 meters.

Answer: (2)

If parking is prohibited on a road, what hours are vehicles prohibited from parking?

(1) From 7 a.m. until 8 p.m.
(2) from 7 p.m. until 8 a.m. the following day.
(3) 24 hours a day.

Answer: (1)

Tires deemed safe for driving on a freeway or expressway must have a tread depth of at least

(1) 1.6 mm.
(2) 1.5 mm.
(3) 1.7 mm.

Answer: (1)

The following questions conflict,

\#122: Those who possess a license for driving a bus may also drive a trailer truck.

Answer: X

\#228: Drivers possessing a bus driver's license may drive large trucks, large vehicles for carrying both passengers and goods, trailer trucks, cars, and motorcycles.

Answer: O

These two tricky,

Drivers have to comply with speed limits shown on signs. On roads with no speed limit sign, drivers must not exceed a speed of 40 km per hour. On roads without lines regulating lanes or oncoming traffic separation, drivers must not exceed a speed of 30 km per hour.

Answer: X

Drivers have to comply with speed limits shown on signs. On roads with no speed limit sign, drivers must not exceed a speed of 50km per hour. On roads without lines regulating lanes or oncoming traffic separation, drivers must not exceed a speed of 40km per hour.

Answer: O


### More easy examples

E.G. 1: If a driver receives traffic violation points and a fine for breaking a traffic regulation, in the future they are required to:

(1) drive as usual
(2) drive carefully and not to break any more rules,
(3) never drive again.

E.G. 2: In a tunnel, are drivers allowed to park their vehicle temporarily, pass other vehicles, or drive in reverse?

(1) Yes
(2) No
(3) There is no applicable regulation.

E.G. 3: Which of the following statements is correct?

(1) The driver, the front-seat passengers, and the rear seat passengers of a small vehicle are required to wear safety belts;
(2) The driver must use the turn signal after starting the car;
(3) By law, children must be seated in the front.

