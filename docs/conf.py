import os

import alagitpull

# Get the project root dir, which is the parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(cwd)

# package data
about = {}
with open("../vcspull/__about__.py") as fp:
    exec(fp.read(), about)

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "sphinx.ext.todo",
    "sphinx.ext.napoleon",
    "sphinx.ext.linkcode",
    "alagitpull",
    "sphinx_issues",
    "sphinx_click.ext",  # sphinx-click
    "myst_parser",
]

# app setup hook
def setup(app):
    pass


myst_enable_extensions = ["substitution", "replacements"]


issues_github_path = about["__github__"].replace("https://github.com/", "")

templates_path = ["_templates"]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

master_doc = "index"

project = about["__title__"]
copyright = about["__copyright__"]

version = "%s" % (".".join(about["__version__"].split("."))[:2])
release = "%s" % (about["__version__"])

exclude_patterns = ["_build"]

pygments_style = "sphinx"

html_theme_path = [alagitpull.get_path()]
html_theme = "alagitpull"
html_theme_options = {
    "logo": "img/vcspull.svg",
    "github_user": "vcs-python",
    "github_repo": "vcspull",
    "github_type": "star",
    "github_banner": True,
    "projects": alagitpull.projects,
    "project_name": about["__title__"],
    "project_title": about["__title__"],
    "project_description": about["__description__"],
    "project_url": about["__docs__"],
    "show_meta_manifest_tag": True,
    "show_meta_og_tags": True,
    "show_meta_app_icon_tags": True,
}
html_sidebars = {
    "**": [
        "about.html",
        "navigation.html",
        "relations.html",
        "more.html",
        "searchbox.html",
    ]
}

html_static_path = ["_static"]
html_extra_path = ["manifest.json"]

alagitpull_internal_hosts = ["vcspull.git-pull.com", "0.0.0.0"]
alagitpull_external_hosts_new_window = True


htmlhelp_basename = "%sdoc" % about["__title__"]

latex_documents = [
    (
        "index",
        "{0}.tex".format(about["__package_name__"]),
        "{0} Documentation".format(about["__title__"]),
        about["__author__"],
        "manual",
    )
]

man_pages = [
    (
        "index",
        about["__package_name__"],
        "{0} Documentation".format(about["__title__"]),
        about["__author__"],
        1,
    )
]

texinfo_documents = [
    (
        "index",
        "{0}".format(about["__package_name__"]),
        "{0} Documentation".format(about["__title__"]),
        about["__author__"],
        about["__package_name__"],
        about["__description__"],
        "Miscellaneous",
    )
]

intersphinx_mapping = {
    "py": ("https://docs.python.org/", None),
    "libvcs": ("http://libvcs.git-pull.com/", None),
}


def linkcode_resolve(domain, info):  # NOQA: C901
    import inspect
    import sys
    from os.path import dirname, relpath

    import vcspull

    """
    Determine the URL corresponding to Python object

    Notes
    -----
    From https://github.com/numpy/numpy/blob/v1.15.1/doc/source/conf.py, 7c49cfa
    on Jul 31. License BSD-3. https://github.com/numpy/numpy/blob/v1.15.1/LICENSE.txt
    """
    if domain != "py":
        return None

    modname = info["module"]
    fullname = info["fullname"]

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except Exception:
            return None

    # strip decorators, which would resolve to the source of the decorator
    # possibly an upstream bug in getsourcefile, bpo-1764286
    try:
        unwrap = inspect.unwrap
    except AttributeError:
        pass
    else:
        obj = unwrap(obj)

    try:
        fn = inspect.getsourcefile(obj)
    except Exception:
        fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""

    fn = relpath(fn, start=dirname(vcspull.__file__))

    if "dev" in about["__version__"]:
        return "%s/blob/master/%s/%s%s" % (
            about["__github__"],
            about["__package_name__"],
            fn,
            linespec,
        )
    else:
        return "%s/blob/v%s/%s/%s%s" % (
            about["__github__"],
            about["__version__"],
            about["__package_name__"],
            fn,
            linespec,
        )
