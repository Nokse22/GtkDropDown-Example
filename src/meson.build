pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'gtkdropdown_example')
gnome = import('gnome')

gnome.compile_resources('gtkdropdown-example',
  'gtkdropdown-example.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'gtkdropdown-example.in',
  output: 'gtkdropdown-example',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

gtkdropdown_example_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

install_data(gtkdropdown_example_sources, install_dir: moduledir)
