# Development

## Preparation

* install python 3+
* set up venv for this folder ```py -m venv env```
* use the env ```.\env\Scripts\activate```
* update pip ```.\env\Scripts\python.exe -m pip install --upgrade pip```
* get dependencies ```pip install -r requirements.txt```
  * ignore warning about mq install
* get pyinstaller ```pip install pyinstaller```

## Package

```pyinstaller --onefile -w .\pbivcs.py```

this will bundle up ```pbivcs.exe``` to \dist
Note - this kicks off some antivirus programs - you may need to unquarantine it.

## tasks

### TODO

* Refactor into strategy/visitor pattern for json rewriting
* BLOCKED: Not compatible with PowerBI - Sort Layout Visual Containers array by id

### DOING

### DONE

* Rebase on upstream master
* Change option to "--diffable", and use it
* Expression - string with \n into __multi_line with array of lines
* Split large data model schema "tables" into independent files
* Split large report model schema "bookmarks" into independent files
* Split large report model schema "sections" into independent files
* Remove last modified noise
  * only needed on data model schema, so hard-coded
* Diagram layout - apply formatted json converter
