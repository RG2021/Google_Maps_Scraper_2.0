from cx_Freeze import setup,Executable

includefiles = [ 'templates', 'chromedriver.exe', 'static', 'test.py']
includes = [ 'jinja2' , 'jinja2.ext']  # add jinja2.ext here
excludes = ['Tkinter']

setup(
	name='Sample Flask App',
	version = '0.1',
	description = 'Sample Flask App',
	options = {'build_exe':   {'excludes':excludes,'include_files':includefiles, 'includes':includes}},
	executables = [Executable('main.py')]
)