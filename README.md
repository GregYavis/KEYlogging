# Introduction
Hello this is one of my first serious projects.This is keylogger for Windows.
Project consists of a template (keylogger_template.py) and builder,
 with the help of whitch you can enter your data into the template without diggin into code of template.
Builder also generates an ".exe" file, whitch is enough to run on a computer with Windows OS.
## Using builder.py
To create an .exe file using the data you need, you need to run builder.py from the terminal
 using comand line arguments.
Information about the comand line arguments can be obtained by typing in the terminal:
>python3 builder.py -h 
###Example comand to create ".exe" file:
>python3 builder.py -e example.email@gmail.com -p email_password -d 600 -f result_filename.py
## Gmail Security Settings
For the code to successfully send messages with logs, you need allow @gmail access to third party apps here:
https://myaccount.google.com/lesssecureapps
## Case-sensetive decision
Ther is quite a lot of information on the Internet about how make a keylogger with Python. 
But not all of them are case-sensetive.
I solved this problem by using variables that register the state of the 'SHIFT', 'CTRL' and 'ALT' keys
and then transfer this state to the dictionary, whitch is written to the .txt file.
