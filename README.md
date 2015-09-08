## Description

This is a Python tool for converting the Taiwan driver's test study data from PDF to CSV for import into an Anki deck.

## Motivation and Goal

The motivation for making this was to practice writing some Python, help people study more efficiently for the test, and allow updates by rerunning this code in the event of changes made by the DMV.

The goal is to (1) identify the harder questions and (2) make studying them easier.

Some of the issues with the existing test and resources are,

  * There are now 1,600 questions for the scooter test.  Before July 2015 there were only 600
  * Most questions are easy, but there are enough hard ones that it is easy to fail the test unless you review them
  * It is difficult to identify and focus on studying the hard questions
  * Study material consists of all possible questions rather than a more concise presentation of what you should know

## Requirements

This has been tested under OS X, Python 2, and poppler 0.34.0.  Beautiful Soup and Poppler's pdftohtml are required.

## How to use

The basic way to run the program is

```
python convert.py -f <path-to-pdf> -c -a <path-to-anki-media-folder> [-w working-directory]
```

The code will create a .csv file in the working directory, or the current one if not specified.  With the -c argument given, if the PDF contains images, they will be copied to the anki media folder, and inserted into the front of the question cards.

Then, import this CSV into an Anki deck

## To do

  * Identify medium and hard questions.  Store that information in git and write code to re-apply it when converting from PDF to CSV
  * Make some test cases

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

