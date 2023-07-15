from jinja2 import Template
import os
import sys
from pathlib import Path


def render(template_name, folder='templates', **kwargs):
    """
    The function renders html template
    :param template_name:
    :param folder:
    :param kwargs:
    :return:
    """
    # proj_path = Path(os.getcwd()).parent
    proj_path = Path(os.getcwd())
    print(f'app_path = {proj_path}')
    file_path = os.path.join(proj_path, folder, template_name)
    # print(f'templ_path = {file_path}')
    # -----------Read Template --------------------------
    with open(file_path, mode='r', encoding='utf-8') as f:
        template = Template(f.read())

    # ------------ Render Template -----------------------
    return template.render(**kwargs)
