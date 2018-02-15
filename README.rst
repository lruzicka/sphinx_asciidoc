#################################################
AsciiDoc Builder and Writer for Sphinx (asciidoc)
#################################################

Introduction
~~~~~~~~~~~~

Sphinx is used to build documentation from reST source files using
Docutils. While there are many Sphinx output writers, such as html,
ePub, and LaTex, there has been no conversion tool available to convert
Sphinx based reST documentation to asciidoc files. Some of the open source 
projects, such as Pandoc, do not understand most of the Sphinx directives 
and are only able to proceed the simple reST format. 

The following is my attempt to write an AsciiDoc extension
for Sphinx and Docutils that would be able to serve as a builder and
writer for Sphinx, as well as a simple reST to AsciiDoc convertor.

It primarily uses Python 3, but should be fine with 2.7.

Standalone usage
~~~~~~~~~~~~~~~~

You can also use the ``./asciidoc/writer.py`` as a simple convertor of
single reST files based on **docutils** reST format. 

To convert a reST file to asciidoc:

    python writer.py file.rst

When the script finishes, it creates a new asciidoc file with the same
name and the ``.adoc`` extension.

Current status
~~~~~~~~~~~~~~

The extension is now a 1.0.0 version. It understands the majority
of the Docutils markup and produces a usable *asciidoc* format, that can be
processed with **Asciidoctor**. However, there are some issues that have not been solved
yet, since **Asciidoctor** does not support similar functionality, or this funcionality
is not possible due to **Asciidoctor**'s architecture. There might be improvements in the future.

.. note::
    The conversion may fail because of ``NotImplemented Error`` that is
    caused when the convertor does not understand how to interpret a
    Sphinx directive. Some of the nodes are only partially implemented. 
    They do not throw out an error, but they do not know how to convert the
    content either. Instead, they pass the content as plain text and wrap it
    with the name of the directive, so that users know where the conversion 
    fails. 

    If you experience such troubles, please report this in the *issues* of this 
    Github project (http://github.com/lruzicka/sphinx-asciidoc) and describe which
    directive is not rendered and how do you think it should be rendered in asciidoc or
    how should the html rendering from **Asciidoctor** look like.

Known issues
~~~~~~~~~~~~

Converted Toctree includes chapters twice
    **Sphinx** uses the ``.. toctree::`` directive to collect single *rst* files and create a complete book to present on the web page. **Asciidoctor** is not capable of something similar, so those links were replaced by ``include`` directives. A problem is, that those includes are sometimes used more than once, first in the master file and then in the submaster files. In order to get proper results, you have to edit the master file and delete includes that include files from submaster files to get rid of duplicities. Alernatively, you can delete all includes from any subfiles and only leave those in the master file.

Referencing to target files instead to IDs
    In **Sphinx**, you can either send a reference to a target (represented by an ID) or to a source file. The result will be similar. On the web, both references will bring you to a given location. The ``:doc:`` refernce will point towards the beginning of the text provided by the source file. **Asciidoc** does not use anything like that and I have not been able to find a complete solution for this issue yet. Now, the convertor creates false reference directives that you have to replace manually or programatically. You can find those references because in their definition, the string ``#fileref`` has been placed.

reST markup conflicts with Asciidoc markup
    Sometimes, especially if you want to show pieces of *reST* code and use a code block, the markup will not be translated, but rather gets transfered directly into the *asciidoc* files where it conflicts with **Asciidoctor**, rendering erroneously. If you experience such problems, you have to use escape characters manually in the resulting *asciidoc* files.


Future improvements
--------------------

In the future:

1. reported issues should be fixed, whenever somebody experiences such an error or a new directive will appear in Sphinx,
2. try to solve the known issues to make the translation work flawlessly
3. implement the not yet implemented Sphinx and Docutils nodes, so that
   the AsciiDoc files use all possible features of the original reST and
   Sphinx format.

Installing the **sphinx_asciidoc** package
------------------------------------------

The package is in **PyPI**. To install it:

    pip3 install sphinx_asciidoc

Now, you should be able to use it.

Using the **asciidoc** builder
------------------------------

When building the documentation from the source files, choose the
**asciidoc** builder with the ``-b`` option:

    sphinx-build -b asciidoc ./source ./build

The built documentation is placed in the ``./build/asciidoc`` directory.

Disclaimer
----------

You can freely use the software, but you should be aware that there might problems arise that would need your manual assistance to make the translation error free. Always check that the files have been properly converted before you publish your content.
