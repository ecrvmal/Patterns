from jinja2 import Template
import os
from pathlib import Path


def render(template_name, folder='templates', **kwargs):
    """
    The function renders html template
    :param template_name:
    :param folder:
    :param kwargs:
    :return:
    """
    app_path = Path(os.getcwd()).parent
    file_path = os.path.join(app_path, folder, template_name)
    # print(f'templ_path = {file_path}')
    # -----------Read Template --------------------------
    with open(file_path, mode='r', encoding='utf-8') as f:
        template = Template(f.read())

    # ------------ Render Template -----------------------
    return template.render(**kwargs)
