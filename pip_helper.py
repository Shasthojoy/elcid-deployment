from fabric.api import local, env
from common import lexists


class Pip(object):
    @classmethod
    def get_pip(cls):
        return "{}/bin/pip".format(
            env.virtual_env_path
        )

    @classmethod
    def install_virtualenv(cls):
        if env.http_proxy:
            local("pip install virtualenv --proxy {}".format(env.http_proxy))
        else:
            local("pip install virtualenv")

    @classmethod
    def create_virtual_env(cls):
        cls.install_virtualenv()
        if not lexists(env.virtual_env_path):
            local("/usr/bin/virtualenv {0}".format(env.virtual_env_path))

    @classmethod
    def remove_virtualenv(cls):
        local("rm -rf /usr/bin/virtualenv/{}".format(env.project_name))

    @classmethod
    def set_project_directory(cls):
        local("echo '{0}' > {1}/.project".format(
            env.project_path, env.virtual_env_path
        ))

    @classmethod
    def install(cls, *pkgs):
        pip = cls.get_pip()
        for pkg in pkgs:
            if env.http_proxy:
                local('{0} install --proxy {2} -U {1}'.format(pip, pkg, env.http_proxy))
            else:
                local('{0} install -U {1}'.format(pip, pkg))

    @classmethod
    def install_requirements(cls):
        if env.http_proxy:
            local("{0} install -r requirements.txt --proxy {1}".format(
                cls.get_pip(), env.http_proxy
            ))
        else:
            local("{0} install -r requirements.txt".format(cls.get_pip()))
