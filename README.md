# rst2adoc

## AsciiDoc Builder and Writer for Sphinx

## Introduction

Sphinx is used to build documentation from reST source files using Docutils. While there are many Sphinx output writers, such as html, ePub, and LaTex. Unfortunately, there is no conversion tool to AsciiDoc and some of the open source projects, such as Pandoc, do not understand most of the Sphinx directives and are only able to proceed the simple reST format. The following is my attempt to write an AsciiDoc extension for Sphinx and Docutils that would be able to serve as a builder and writer for Sphinx, as well as a simple rst to asciidoc convertor.

## Files

Currently, there are two files in the repository:

* **asciidoc_builder.py** is a Sphinx builder that you can place in the *builders* directory of the Sphinx installation.
* **asciidoc_writer.py** is Sphinx writer that you can place in the *writers* directory of the Sphinx installation.

Note, that in order to work, you must register the new builder in the Sphinx application (*application.py*)

- 
