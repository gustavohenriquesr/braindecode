#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Braindecode documentation build configuration file, created by
# sphinx-quickstart on Sat Jul  1 01:51:38 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
import inspect
import os.path as op

import matplotlib
matplotlib.use('agg')
from datetime import datetime, timezone
import faulthandler

import sphinx_gallery  # noqa
from sphinx_gallery.sorting import FileNameSortKey, ExplicitOrder

from numpydoc import numpydoc, docscrape  # noqa

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '2.0'

curdir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(curdir, '..', 'braindecode')))
sys.path.append(os.path.abspath(os.path.join(curdir, 'sphinxext')))

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'sphinx_gallery.gen_gallery',
    "sphinx.ext.linkcode",
    "sphinx_design",
    'numpydoc',
    'gh_substitutions',
]


def linkcode_resolve(domain, info):
    """Determine the URL corresponding to a Python object.

    Parameters
    ----------
    domain : str
        Only useful when "py".
    info : dict
        With keys "module" and "fullname".

    Returns
    -------
    url : str
        The code URL.

    Notes
    -----
    This has been adapted to deal with our "verbose" decorator.
    Adapted from SciPy (doc/source/conf.py).
    """
    repo = "https://github.com/braindecode/braindecode/"
    if domain != "py":
        return None
    if not info["module"]:
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

    try:
        fn = inspect.getsourcefile(obj)
    except Exception:
        fn = None
    if not fn:
        try:
            fn = inspect.getsourcefile(sys.modules[obj.__module__])
        except Exception:
            fn = None
    if not fn:
        return None
    fn = op.relpath(fn, start=op.dirname(braindecode.__file__))
    fn = "/".join(op.normpath(fn).split(os.sep))  # in case on Windows

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""

    return f"{repo}/blob/master/braindecode/{fn}{linespec}"

# -- Options for sphinx gallery --------------------------------------------
faulthandler.enable()
os.environ['_BRAINDECODE_BROWSER_NO_BLOCK'] = 'true'
os.environ['BRAINDECODE_BROWSER_OVERVIEW_MODE'] = 'hidden'
os.environ['BRAINDECODE_BROWSER_THEME'] = 'light'

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
curdir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(curdir, '..', 'mne')))
sys.path.append(os.path.abspath(os.path.join(curdir, 'sphinxext')))

autosummary_generate = True
autodoc_default_options = {'inherited-members': False}

numpydoc_show_class_members = False

exclude_patterns = ['_build', '_templates']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.


# -- Project information -----------------------------------------------------

project = "Braindecode"
td = datetime.now(tz=timezone.utc)

# We need to triage which date type we use so that incremental builds work
# (Sphinx looks at variable changes and rewrites all files if some change)
copyright = (
    f'2012–{td.year}, Braindecode Developers. Last updated <time datetime="{td.isoformat()}" class="localized">{td.strftime("%Y-%m-%d %H:%M %Z")}</time>\n'  # noqa: E501
    '<script type="text/javascript">$(function () { $("time.localized").each(function () { var el = $(this); el.text(new Date(el.attr("datetime")).toLocaleString([], {dateStyle: "medium", timeStyle: "long"})); }); } )</script>'
)  # noqa: E501
if os.getenv("BRAINDECODE_FULL_DATE", "false").lower() != "true":
    copyright = f"2018–{td.year}, Braindecode Developers. Last updated locally"

author = 'Braindecode developers'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
import braindecode
release = braindecode.__version__
# The full version, including alpha/beta/rc tags.
version = '.'.join(release.split('.')[:2])

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
# language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# Sphinx-gallery configuration

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/{.major}'.format(sys.version_info), None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference', None),
    'matplotlib': ('https://matplotlib.org/', None),
    'sklearn': ('http://scikit-learn.org/stable', None),
    'mne': ('http://mne.tools/stable', None),
    'skorch': ('https://skorch.readthedocs.io/en/stable/', None),
    'torch': ('https://pytorch.org/docs/stable/', None),
    'braindecode': ('https://braindecode.org/', None),
}

sphinx_gallery_conf = {
    'examples_dirs': ['../examples'],
    'gallery_dirs': ['auto_examples'],
    'doc_module': ('braindecode', 'mne'),
    'backreferences_dir': 'generated',
    'show_memory': True,
    'reference_url': dict(braindecode=None),
    'subsection_order': ExplicitOrder(
        [
            '../examples/datasets_io',
            '../examples/model_building',
            '../examples/advanced_training',
            '../examples/applied_examples'
        ]
    ),
    "within_subsection_order": FileNameSortKey
}

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
import sphinx_rtd_theme  # noqa
html_theme = "pydata_sphinx_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
switcher_version_match = 'dev' if release.endswith('dev0') else version
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

html_theme_options = {
    'icon_links': [
        {
            "name": "GitHub",
            "url": "https://github.com/braindecode/braindecode",
            "icon": "fa-brands fa-github",
        },
    ],
    "github_url": "https://github.com/braindecode/braindecode",
    'icon_links_label': 'External Links',  # for screen reader
    'use_edit_page_button': False,
    'navigation_with_keys': False,
    "collapse_navigation": False,
    "header_links_before_dropdown": 4,
    "navigation_depth": 4,
    'show_toc_level': 1,
    'navbar_end': ['theme-switcher', 'version-switcher'],
    'switcher': {
      'json_url': 'https://braindecode.org/stable/_static/versions.json',
      'version_match': switcher_version_match,
    },
    "logo": {
        "image_light": "_static/braindecode_symbol.png",
        "image_dark": "_static/braindecode_symbol.png",
        "alt_text": "Braindecode Logo",
    },
    'footer_start': ['copyright'],
    'pygment_light_style': 'default',
    'analytics': dict(google_analytics_id='G-7Q43R82K6D'),
}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/braindecode_symbol.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
    'style.css',
]

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False
html_copy_source = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'Braindecode-doc'

# accommodate different logo shapes (width values in rem)
xs = '2'
sm = '2.5'
md = '3'
lg = '4.5'
xl = '5'
xxl = '6'

html_context = {
    'build_dev_html': bool(int(os.environ.get('BUILD_DEV_HTML', False))),
    'default_mode': 'light',
    'pygment_light_style': 'tango',
    'pygment_dark_style': 'native',
    'icon_links_label': 'Quick Links',  # for screen reader
    'show_toc_level': 1,
    'institutions': [
        dict(name='University of Freiburg',
             img='unifreiburg.png',
             url='https://www.ieeg.uni-freiburg.de/',
             size=lg),
        dict(name='Institut national de recherche en informatique et en automatique',  # noqa E501
             img='inria.png',
             url='https://www.inria.fr/',
             size=xl),
    ],
    "navbar_align": "content",
    "github_user": "braindecode",
    "github_repo": "braindecode",
    "github_version": "main",
    "doc_path": "docs",

}


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_logo = "_static/braindecode_symbol.png"
latex_toplevel_sectioning = 'part'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Braindecode.tex', 'Braindecode',
     'Robin Tibor Schirrmeister', 'manual'),
]



# -- Fontawesome support -----------------------------------------------------

# here the "fab" and "fas" refer to "brand" and "solid" (determines which font
# file to look in). "fw" indicates fixed width.
brand_icons = ('apple', 'linux', 'windows', 'discourse', 'python')
fixed_icons = (
    # homepage:
    'book', 'code-branch', 'newspaper', 'question-circle', 'quote-left',
    # contrib guide:
    'bug', 'comment', 'hand-sparkles', 'magic', 'pencil-alt', 'remove-format',
    'universal-access', 'discourse', 'python',
)
other_icons = (
    'hand-paper', 'question', 'rocket', 'server', 'code', 'desktop',
    'terminal', 'cloud-download-alt', 'wrench', 'hourglass'
)
icons = dict()
for icon in brand_icons + fixed_icons + other_icons:
    font = ('fab' if icon in brand_icons else 'fas',)  # brand or solid font
    fw = ('fa-fw',) if icon in fixed_icons else ()     # fixed-width
    icons[icon] = font + fw

prolog = ''
for icon, classes in icons.items():
    prolog += f'''
.. |{icon}| raw:: html

    <i class="{' '.join(classes)} fa-{icon}"></i>
'''

prolog += '''
.. |fix-bug| raw:: html

    <span class="fa-stack small-stack">
        <i class="fas fa-bug fa-stack-1x"></i>
        <i class="fas fa-ban fa-stack-2x"></i>
    </span>
'''

prolog += '''
.. |ensp| unicode:: U+2002 .. EN SPACE
'''


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'braindecode', 'Braindecode',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Braindecode', 'Braindecode',
     author, 'Braindecode', 'One line description of project.',
     'Miscellaneous'),
]
