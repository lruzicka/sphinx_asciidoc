# AsciiDoc Builder and Writer for Sphinx (rst2adoc)

## Introduction

Sphinx is used to build documentation from reST source files using Docutils. While there are many Sphinx output writers, such as html, ePub, and LaTex. Unfortunately, there is no conversion tool to AsciiDoc and some of the open source projects, such as Pandoc, do not understand most of the Sphinx directives and are only able to proceed the simple reST format. The following is my attempt to write an AsciiDoc extension for Sphinx and Docutils that would be able to serve as a builder and writer for Sphinx, as well as a simple reST to AsciiDoc convertor.

It uses Python 2.7.

## Files

Currently, there are two files in the repository:

* **asciidoc_builder.py** is a Sphinx builder that you can place in the *builders* directory of the Sphinx installation.
* **asciidoc_writer.py** is Sphinx writer that you can place in the *writers* directory of the Sphinx installation.

Note, that in order to work, both files must be renamed to *asciidoc.py* in the respective directory and you must register the new builder in the Sphinx application (*application.py*). I am currently studying how to write an installation script. If you know how, let me know.

## Standalone usage

You can also use the *asciidoc_writer.py* as a simple convertor of single reST files. Use the following way to do it:

> python asciidoc_writer.py file.rst

After the program is over, you will find a new file in the target directory with an .adoc extension which is the converted format.


## Current status

The convertor is able to serve as a Sphinx builder and writer, as well as a standalone reST to AsciiDoc convertor. It understands the most important Docutils nodes and produces a usable AsciiDoc format, but there still are improvements necessary.

Note that when the convertor parses files included with ``include::``, it outputs their contents directly into the referencing file, i.e. the convertor does not preserve individual files for included content.

The conversion may fail because of ``NotImplemented Error`` which is caused when the convertor does not understand how it shall interpret the particular node. Some of the nodes are partially implemented, i.e. the conversion does not fail on them, but they are only converted as plain text, so the formatting features are dropped.

## Further improvements

 Among the most needed things are:

1. implement formatting features of the nodes that only produce plain text.
2. implement the not yet implemented Sphinx and Docutils nodes, so that the AsciiDoc files use all possible features of the original reST and Sphinx format.
3. improve the visitors (conversion functions) so that the AsciiDoc output is always flawless and possibly error free.

## Disclaimer

You can already use the software, but you shall take it as not fully developed, so there still may be problems and some features may not work properly or at all.
