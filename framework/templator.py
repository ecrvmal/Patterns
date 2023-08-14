from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment

import os
import sys
# sys.path.append('../')

def render(template_name, folder='templates', **kwargs):
    """
    The function renders html template
    :param template_name:
    :param folder:
    :param kwargs:
    :return:
    """
    # ----------------  Old Templator ------------------------
    # # proj_path = Path(os.getcwd()).parent
    # proj_path = Path(os.getcwd())
    # # print(f'app_path = {proj_path}')
    # file_path = os.path.join(proj_path, folder, template_name)
    # # print(f'templ_path = {file_path}')
    # #                -Read Template -
    # with open(file_path, mode='r', encoding='utf-8') as f:
    #     template = Template(f.read())
    #
    # #              - Render Template -
    # return template.render(**kwargs)

    # ------------------ New Templator -----------------------------
    env = Environment()

    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    print(template)
    return template.render(**kwargs)

if __name__ == "__main__":
    output_test = render('index.html', )
    print(output_test)

