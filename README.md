# PC-GUI
A GUI application for the PC that sends the ARM32 executable .ELF file to the server

## Dependencies
```bash
sudo pip3 install PySide2
```

## Steps and guides
1) pyrebase4 

https://github.com/thisbejim/Pyrebase/issues/299
https://github.com/nhorvath/Pyrebase4

********** important steps *****************

* install  python 3.7.1
* pip install pyrebase4 

************** may be needed ****************


```bash
pip3 install --upgrade setuptools
```


```bash
pip3 install --upgrade gcloud
```


```bash
pip install wheel
```

// solves win32com module not found when compiling GUI

```bash
pip3 install pypiwin32
```

----------------------------------------------------------------------------

2) pyinstaller


```bash
pip install pyinstaller
```

setup for python 3.7 :
----------------------
// pyi-rth-pkgres issue
https://stackoverflow.com/questions/37815371/pyinstaller-failed-to-execute-script-pyi-rth-pkgres-and-missing-packages


solve google-cloud issue :
-------------------------- 
https://github.com/googleapis/google-cloud-python/issues/4780
or
https://github.com/googleapis/google-cloud-python/issues/4780#issuecomment-626121078


solve other issues:
--------------------------
// after installing pyinstaller

```bash
pip uninstall shiboken2
```

```bash
pip uninstall PySide2
```

```bash
pip3 install shiboken2
```

```bash
pip3 install PySide2
```

// then copy these folders from python install dir to dist dir
`gcloud-0.18.3-py3.8.egg-info`
`google`


to generate .exe file :
-----------------------
```bash
pyinstaller PC-GUI.py -w --name FOTA
```

then add the icon to dist folder
----------------------------------------------------------------------------