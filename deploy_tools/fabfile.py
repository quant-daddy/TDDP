from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random


#  Deployment
# 1. Create directory structure in ~/sites
# 2. Pull down source code into folder named source
# 3. Start virtualenv in ../virtualenv
# 4. pip install -r requirements.txt
# 5. manage.py migrate for database
# 6. collectstatic for static files
# 7. Set DEBUG = False and ALLOWED_HOSTS in settings.py
# 8. Restart Gunicorn job
# 9. Run FTs to check everything works

REPO_URL = 'https://github.com/skk2142/TDDP.git'

def deploy():
	site_folder = '/home/%s/sites/%s' % (env.user, env.host)
	source_folder = site_folder + '/source'
	_install_packages()
	_create_directory_structure_if_necessary(site_folder)
	_get_latest_source(source_folder)
	_update_settings(source_folder, env.host)
	_update_virtualenv(source_folder)
	_update_static_files(source_folder)
	_update_database(source_folder)
	_update_nginx_conf_and_upstart_script(source_folder)
	_update_etc_hosts_for_live_functional_test()
	_start_server_and_gunicorn()


def _install_packages():
	run('sudo apt-get update')
	run('sudo apt-get install -y nginx git python3 python3-pip')
	run('sudo pip3 install virtualenv')


def _create_directory_structure_if_necessary(site_folder):
	for subfolder in ('database', 'static', 'virtualenv', 'source'):
		run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
	if exists(source_folder+'/.git'):
		run('cd %s && git fetch' % (source_folder,))
	else:
		run('git clone %s %s' % (REPO_URL, source_folder))
		current_commit = local('git log -n 1 --format=%H', capture=True)
		run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
	settings_path = source_folder + '/superlists/settings.py'
	sed(settings_path, "DEBUG = True", "DEBUG = False")
	sed(settings_path, "TEMPLATE_DEBUG =.+$", "TEMPLATE_DEBUG = DEBUG")
	sed(settings_path, 'ALLOWED_HOSTS =.+$', 'ALLOWED_HOSTS = ["*"]')
	secret_key_file = source_folder + '/superlists/secret_key.py'
	if not exists(secret_key_file):
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
		append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
		append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
	virtualenv_folder = source_folder + '/../virtualenv'
	if not exists(virtualenv_folder + '/bin/pip'):
		run('virtualenv --python=python3 %s' % (virtualenv_folder,))
	run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder))

def _update_static_files(source_folder):
	run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (source_folder,))

def _update_database(source_folder):
	run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (source_folder,))

def _update_nginx_conf_and_upstart_script(source_folder):
	run('cd %s && sed "s/SITENAME/%s/g;s/USERID/%s/g" deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/%s' % (source_folder, env.host, env.user, env.host))
	run('cd %s && sudo ln -s ../sites-available/%s /etc/nginx/sites-enabled/%s' % (source_folder, env.host, env.host,))
	gunicorn_upstart_script_name = 'gunicorn-'+env.host+'.conf'
	run('cd %s && sed "s/SITENAME/%s/g;s/USERID/%s/g" deploy_tools/gunicorn-upstart.template.conf | sudo tee /etc/init/%s' % (source_folder, env.host, env.user, gunicorn_upstart_script_name,))

def _update_etc_hosts_for_live_functional_test():
	pass

def _start_server_and_gunicorn():
	run('sudo service nginx reload')
	run('sudo start gunicorn-%s' % (env.host,))
