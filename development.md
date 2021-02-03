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
