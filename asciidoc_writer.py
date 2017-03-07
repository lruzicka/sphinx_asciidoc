#!/bin/python
# -*- coding: utf-8 -*-

""" 
   sphinx.writers.asciidoc
   ~~~~~~~~~~~~~~~~~~~~~~~

   Custom docutils writer for AsciiDoc format.

   This writer is based on the RTF writer by Benoit Allard (benoit@aeteurope.nl) and has been adapted to the use with AsciiDoc.
      
   Author:    Lukas Ruzicka
   Contact:   lukas.ruzicka@gmail.com
   Copyright: This module has been placed in the public domain.
"""
from docutils import writers, nodes
import sys

from sphinx import addnodes
from sphinx.deprecation import RemovedInSphinx16Warning
from sphinx.locale import admonitionlabels, _

class AsciiDocWriter(writers.Writer):

    supported = ('asciidoc',)
    output = None

    def __init__(self):
        writers.Writer.__init__(self)
        self._translator_class = AsciiDocTranslator

    def translate(self):
        visitor = self._translator_class(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()

def toansi(text):
    """ Encode special characters """
    trans = {'{': r'\{',
             '}': r'\}',
             '\\': r'\\',
             '|': r'\|',
             }
    out = ''
    for char in text:
        if char in trans:
            out += trans[char]
        elif ord(char) < 127:
            out += char
        else:
            out += r"\'%x" % ord(char)
    return out


sectionEquals = { # Stores values for different section levels
    -1: '',
     0: '= ', #title
     1: '== ', # section
     2: '=== ', # subsection
     3: '==== ', # subsubsection
    }


bulletIndent = { # Adds indentation to bullet lists
    1:'* ',   # First level
    2:'** ', # Second level
    3:'*** ', # Third level
    4:'**** ', # Fourth level
    5:'***** ', # Fifth level
    }

enumIndent = { # Adds indentation to ordered lists
    1:'. ',   # First level
    2:'.. ', # Second level
    3:'... ', # Third level
    4:'.... ', # Fourth level
    5:'..... ', # Fifth level
    }

numberIndent = {} # Holds the level of indentation


def indent(fn):
    def wrapper(self, *args, **kwargs):
        self.par_level += 1
        return fn(self, *args, **kwargs)
    return wrapper


def dedent(fn):
    def wrapper(self, *args, **kwargs):
        self.par_level -= 1
        return fn(self, *args, **kwargs)
    return wrapper

class AsciiDocTranslator(nodes.NodeVisitor):
    
    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.body = []
        self.section_level = 0
        self.par_level = -1
        
        self.lists = []  # stack of the currents bullets
        self.listLevel = len(self.lists)
        self.bullet = '*' # next one to add to the next paragraph
        self.figures = 0 # Counts figures for reference targets
        self.inTable = False
        self.turnsInList = 0

    def astext(self):
        docs = ''
        for line in self.body:
            docs = docs+line
        return docs
    
    def visit_document(self, node):
        #self.body.append('Start document')
        pass
    
    def depart_document(self, node):
        pass

    def visit_title(self, node):
        if isinstance(node.parent, nodes.document):
            """ doc title """
            self.body.append('\n\n%s ' % sectionEquals[0])
        elif isinstance(node.parent, nodes.section):
            level = self.section_level
            self.body.append('\n\n%s ' % sectionEquals[level])
        

    def depart_title(self, node):
        self.body.append('\n\n')
            
    def visit_Text(self, node):
##        if self.bullet is not None:
##            self.body.append(self.bullet+'')
##            self.bullet = None
##        self.body.append(toansi(node.astext()))
        self.body.append(node.astext())
        

    def depart_Text(self, node):
        pass

    def visit_strong(self, node): # Does the bold face
        nline = '*'
        self.body.append(nline)

    def depart_strong(self, node):
        nline = '*'
        self.body.append(nline)
    
    def visit_index(self,node):
        self.body.append('((')


    def depart_index(self,node):
        self.body.append('))')
    

    def visit_section(self, node):
        self.section_level += 1
        
    def depart_section(self, node):
        self.section_level -= 1

    @indent
    def visit_paragraph(self, node):
        nline = ''
        self.body.append(nline)

    @dedent    
    def depart_paragraph(self, node):
        if self.listLevel == -1:
            nline = '\n\n'
        else:
            nline = '\n'
        self.body.append(nline)    


    def visit_compact_paragraph(self, node):
        nline = ''
        self.body.append(nline)

    @dedent    
    def depart_compact_paragraph(self, node):
        if self.listLevel == -1:
            nline = '\n\n'
        else:
            nline = '\n'
        self.body.append(nline)    

    def visit_bullet_list(self, node): # Unordered list
        self.lists.append('bulleted')
        if self.inTable == True:
            self.body.append('\n')
        if self.turnsInList == 0:
            self.body.append('\n')
        self.turnsInList = self.turnsInList + 1
        
        
    def depart_bullet_list(self, node):
        if self.listLevel == -1:
            self.body.append('\n\n')
        else:
            self.body.append('\n')
        self.lists.pop(-1)
        self.turnsInList = 0

    def visit_enumerated_list(self, node): # Ordered list
        self.lists.append('numbered')
        enumeration = node['enumtype']
        self.body.append('\n['+enumeration+']\n')
        self.turnsInList = self.turnsInList + 1
        

    def depart_enumerated_list(self,node):
        self.lists.pop(-1)
        self.turnsInList = 0
    
        
    def visit_list_item(self, node):
        level = len(self.lists)
        if 'bulleted' in self.lists:
            sign = bulletIndent[level]
        elif 'numbered' in self.lists:
            sign = enumIndent[level]
        else:
            sign = '\nList indentation error!\n'
        nline = sign
        self.body.append(nline)
        self.turnsInList = self.turnsInList + 1
        
    def depart_list_item(self, node):
        self.body.append('\n')

    def visit_block_quote(self, node):
        pass

    def depart_block_quote(self, node):
        pass

    def visit_reference(self, node):
        tag = str(node)
        
        if 'refuri' in tag:
            self.linkType = 'link'
            link = node['refuri']
            nline = 'link:'+link+'['
            self.body.append(nline)
        elif 'refid' in tag:
            self.linkType = 'refx'
            link = node['refid']
            nline = '<<'+link
            self.body.append(nline)
        else:
            self.body.append('[')

    def depart_reference(self, node):
        if self.linkType == 'link':
            self.body.append(']')
        elif self.linkType == 'refx':
            self.body.append('>>')
        else:
            self.body.append(']')

    def visit_docinfo(self, node):
        nline = 'Document information: '
        self.body.append(nline)

    def depart_docinfo(self, node):
        self.body.append('\n\n')

    def visit_author(self, node):
        nline = 'Author: '
        self.body.append(nline)

    def depart_author(self, node):
        self.body.append('\n\n')

    def visit_version(self, node):
        nline = 'Document version: '
        self.body.append(nline)

    def depart_version(self, node):
        self.body.append('\n\n')

    def visit_copyright(self, node):
        nline = 'Copyright: '
        self.body.append(nline)

    def depart_copyright(self, node):
        self.body.append('\n\n')

    
    def visit_rubric(self, node): # Needs to be implemented.
        pass

    def depart_rubric(self, node):
        pass
    
    def visit_topic(self, node):
        pass
    def depart_topic(self, node):
        pass

    def visit_target(self, node): # Create internal inline links.
        try:
            refid = node['refid']
            self.body.append('[['+str(refid)+']] ')
        except KeyError:
            pass
        
    def depart_target(self, node):
        pass
        
    def visit_compound(self, node): # Needs to be implemented.
        self.body.append('COMPOUND:')

    def depart_compound(self, node):
        self.body.append(':COMPOUND')

    def visit_glossary(self, node):
        self.body.append('GLOSSARY:')

    def depart_glossary(self, node):
        self.body.append('GLOSSARY:')

    def visit_note(self, node):
        if self.listLevel > 0:
            nline = '+\n[NOTE]\n'
        else:
            nline = '[NOTE]\n'
        mline = '====\n'
        self.body.append(nline+mline)

    def depart_note(self, node):
        if self.listLevel > 0:
            nline = '====\n\n'
        else:
            nline = '====\n'
        self.body.append(nline)

    def visit_literal(self, node):
        nline = '`'
        self.body.append(nline)

    def depart_literal(self, node):
        self.body.append('`')
        
    def visit_literal_strong(self, node):
        nline = '`*'
        self.body.append(nline)

    def depart_literal_strong(self, node):
        self.body.append('*`')
    
    def visit_literal_block(self, node):
        level = len(self.lists)
        if level > 0:
            nline = '+\n----\n'
        else:
            nline = '\n----\n'
        self.body.append(nline)

    def depart_literal_block(self, node):
        self.body.append('\n----\n')

    def visit_emphasis(self, node):
        nline = ' _'
        self.body.append(nline)

    def depart_emphasis(self, node):
        self.body.append('_')

    def visit_tip(self, node):
        level = len(self.lists)
        if level > 0:
            nline = '+\n[TIP]\n'
        else:
            nline = '[TIP]\n'
        mline = '====\n'
        self.body.append(nline+mline)
        
    def depart_tip(self, node):
        level = len(self.lists)
        if level > 0:
            nline = '====\n\n'
        else:
            nline = '====\n'
        self.body.append(nline)

    def visit_warning(self, node):
        level = len(self.lists)
        if level > 0:
            nline = '+\n[WARNING]\n'
        else:
            nline = '[WARNING]\n'
        mline = '====\n'
        self.body.append(nline+mline)

    def depart_warning(self, node):
        level = len(self.lists)
        if level > 0:
            nline = '====\n\n'
        else:
            nline = '====\n'
        self.body.append(nline)

    def visit_subtitle(self, node):
        pass

    def depart_subtitle(self, node):
        pass

    def visit_attribution(self, node):
        self.add_text('-- ')

    def depart_attribution(self, node):
        pass
    
    def visit_important(self, node):
        level = len(self.lists)
        if level > 0:
            nline = '+\n[IMPORTANT]\n'
        else:
            nline = '[IMPORTANT]\n'
        mline = '====\n'
        self.body.append(nline+mline)
        
    def depart_important(self, node):
        level = len(self.lists)
        if level > 0:
            nline = '====\n\n'
        else:
            nline = '====\n'
        self.body.append(nline)

    def visit_caution(self, node):
        level = len(self.lists)
        if level > 0:
            nline = '+\n[CAUTION]\n'
        else:
            nline = '[CAUTION]\n'
        mline = '====\n'
        self.body.append(nline+mline)

    def depart_caution(self, node): # Pozor, opravit na level = len(self.lists)
        level = len(self.lists)
        if level > 0:
            nline = '====\n\n'
        else:
            nline = '====\n'
        self.body.append(nline)    

    def visit_definition_list(self, node):
        self.body.append('\n\n')

    def depart_definition_list(self, node):
        self.body.append('\n\n')

    def visit_definition_list_item(self, node):
        self.body.append('')

    def depart_definition_list_item(self, node):
        self.body.append('\n')

    def visit_term(self, node):
        #nline = ''
        #self.body.append(nline)
        pass

    def depart_term(self, node):
        self.body.append(':: ')

    def visit_definition(self, node):
        nline = '\n'
        self.body.append(nline)

    def depart_definition(self,node):
        self.body.append('\n\n')


    def visit_image(self,node):
        try:
            alt = node['alt']
        except KeyError:
            alt = 'Image'
            
        uri = node['uri']
        #tag = str(node)
        #parsed = tag.split(' ')
        #for feature in parsed:
        #    if 'uri' in feature:
        #        ptag = feature.split('"')
        #        path = ptag[1]
        #for feature in parsed:
        #    if 'alt' in feature:
        #        palt = feature.split('"')
        #        alt = palt[1]
        #        break
        #    else:
        #        alt = 'Image'
        nline = 'image::'+uri+'['+alt+']'
        self.body.append(nline)

    def depart_image(self,node):
        self.body.append('\n\n')

    def visit_footnote_reference(self,node):
        ref = str(node['refid'])
        nline = "footnoteref:["+ref+","
        self.body.append(nline)

    def depart_footnote_reference(self,node):
        nline = "] "
        self.body.append(nline)
        
    def visit_footnote(self,node):
        nline = "footnote:["
        self.body.append(nline)

    def depart_footnote(self,node):
        nline = "] "
        self.body.append(nline)

    def visit_label(self,node):
        self.body.append('LABEL:') 

    def depart_label(self,node):
        self.body.append(':LABEL')

    def visit_contents(self,node):
        nline = '== '
        self.body.append(nline)

    def depart_contents(self,node):
        pass
        
    def visit_system_message(self,node):
        self.body.append('System message: ')
    
    def depart_system_message(self,node):
        #self.body.append('')
        pass
    
    def visit_figure(self, node):
        ids = str(node['ids'])
        count = str(self.figures)
        nline = '\n[[ids]]\n'
        mline = '.'+ids+'\n'
        self.body.append(nline+mline)
        

    def depart_figure(self, node):
        self.body.append('\n\n')

    def visit_caption(self,node):
        self.body.append('//.')

    def depart_caption(self,node):
        self.body.append('\n')

    def visit_table(self,node): ## Whole table element
        self.inTable = True
        
    def depart_table(self,node):
        self.inTable = False
        
    def visit_tgroup(self,node): ## Whole inside of the table
        cols = node['cols']
        col = int(round((100 / cols)))
        clist = []
        for i in range(cols):
            clist.append(str(col))
        cline = ','.join(clist)    
        specline = '[cols="'+cline+'",options="header"]\n'
        introline = "|===\nh| "
        self.body.append(specline+introline)

    def depart_tgroup(self,node):
        nline = '|===\n'
        self.body.append(nline)

    def visit_colspec(self,node): ## Column specifics
        pass

    def depart_colspec(self,node):
        pass

    def visit_thead(self,node): ## Table head
        pass

    def depart_thead(self,node):
        pass

    def visit_row(self,node): # Table row
##        nline = ''
##        self.body.append(nline)
        pass

    def depart_row(self,node):
        self.body.append('\n')

    def visit_entry(self,node): # Table cell
        nline = 'a| '
        self.body.append('')
        

    def depart_entry(self,node):
        self.body.append(' a| ')

    def visit_tbody(self,node):
        pass

    def depart_tbody(self,node):
        pass

    def visit_subscript(self,node):
        self.body.append('~')

    def depart_subscript(self,node):
        self.body.append('~')

    def visit_superscript(self,node):
        self.body.append('^')

    def depart_superscript(self,node):
        self.body.append('^')

    def visit_title_reference(self,node):
        self.body.append('TITLE REFERENCE: ') 

    def depart_title_reference(self,node):
        pass

    def visit_line_block(self,node):
        self.body.append('LINE BLOCK: ')

    def depart_line_block(self,node):
        pass

    def visit_line(self,node):
        nlink="\n---"
        self.body.append(nlink)

    def depart_line(self,node):
        self.body.append('\n')

    def visit_comment(self,node):
        self.body.append('\n////')

    def depart_comment(self,node):
        self.body.append('////\n')

    def visit_problematic(self,node):
        self.body.append('PROBLEMATIC: ')

    def depart_problematic(self,node):
        pass

    def visit_raw(self,node):
        self.body.append('RAW: ')

    def depart_raw(self,node):
        pass
    
    def visit_subtitle(self,node):
        self.body.append('SUBTITLE: ')

    def depart_subtitle(self,node):
        pass

    def visit_inline(self,node):
        self.body.append('INLINE: ')

    def depart_inline(self,node):
        pass

    def visit_desc(self, node):
        self.body.append('DESC: ')

    def depart_desc(self, node):
        pass

    def visit_desc_signature(self, node):
        pass

    def depart_desc_signature(self, node):
        pass

    def visit_desc_signature_line(self, node):
        pass

    def depart_desc_signature_line(self, node):
        pass

    def visit_desc_name(self, node):
        pass

    def depart_desc_name(self, node):
        pass

    def visit_desc_addname(self, node):
        pass

    def depart_desc_addname(self, node):
        pass

    def visit_desc_type(self, node):
        pass

    def depart_desc_type(self, node):
        pass

    def visit_desc_returns(self, node):
        pass

    def depart_desc_returns(self, node):
        pass

    def visit_desc_parameterlist(self, node):
        pass

    def depart_desc_parameterlist(self, node):
        pass

    def visit_desc_parameter(self, node):
        pass

    def visit_desc_optional(self, node):
        pass

    def depart_desc_optional(self, node):
        pass

    def visit_desc_annotation(self, node):
        pass

    def depart_desc_annotation(self, node):
        pass

    def visit_desc_content(self, node):
        pass

    def depart_desc_content(self, node):
        pass

    def visit_productionlist(self, node):
    #   self.new_state()
    #   names = []
    #  for production in node:
    #      names.append(production['tokenname'])
    #  maxlen = max(len(name) for name in names)
    #  lastname = None
    #  for production in node:
    #      if production['tokenname']:
    #          self.add_text(production['tokenname'].ljust(maxlen) + ' ::=')
    #          lastname = production['tokenname']
    #      elif lastname is not None:
    #          self.add_text('%s    ' % (' ' * len(lastname)))
    #      self.add_text(production.astext() + self.nl)
    #  self.end_state(wrap=False)
    #  raise nodes.SkipNode
        pass

    def visit_option_list(self, node):
        pass

    def depart_option_list(self, node):
        pass

    def visit_option_list_item(self, node):
        pass

    def depart_option_list_item(self, node):
        pass

    def visit_option_group(self, node):
        pass

    def depart_option_group(self, node):
        pass

    def visit_option(self, node):
        pass

    def depart_option(self, node):
        pass

    def visit_option_string(self, node):
        pass

    def depart_option_string(self, node):
        pass

    def visit_option_argument(self, node):
        pass

    def depart_option_argument(self, node):
        pass
    
    def visit_legend(self, node):
        pass

    def depart_legend(self, node):
        pass

    def visit_description(self, node):
        pass

    def depart_description(self, node):
        pass

    def visit_field_list(self, node):
        pass

    def depart_field_list(self, node):
        pass

    def visit_field(self, node):
        pass

    def depart_field(self, node):
        pass

    def visit_field_name(self, node):
        pass

    def depart_field_name(self, node):
        pass

    def visit_field_body(self, node):
        pass

    def depart_field_body(self, node):
        pass

    def visit_centered(self, node):
        pass

    def depart_centered(self, node):
        pass

    def visit_hlist(self, node):
        pass

    def depart_hlist(self, node):
        pass

    def visit_hlistcol(self, node):
        pass

    def depart_hlistcol(self, node):
        pass

    def visit_versionmodified(self, node):
        pass

    def depart_versionmodified(self, node):
        pass

    def visit_date(self,node):
        self.body.append('Date:')

    def depart_date(self,node):
        self.body.append(':Date')

    def visit_revision(self,node):
        self.body.append('Revision:')

    def depart_revision(self,node):
        self.body.append(':Revision')

    def visit_doctest_block(self,node):
        self.body.append('DocTestBlok:')

    def depart_doctest_block(self,node):
        self.body.append(':DocTestBlok')

    def visit_classifier(self,node):
        self.body.append('Classifier:')

    def depart_classifier(self,node):
        self.body.append(':Classifier')

    def visit_citation(self,node):
        self.body.append('Citation:')

    def depart_citation(self,node):
        self.body.append(':Citation')

    def visit_citation_reference(self,node):
        self.body.append('CitationRFR:')

    def depart_citation_reference(self,node):
        self.body.append(':CitationRFR')
    
    def visit_substitution_definition(self,node):
        self.body.append('SBSdef:')

    def depart_substitution_definition(self,node):
        self.body.append(':SBSdef')







if __name__ == "__main__":
    """ To test the writer """
    from docutils.core import publish_string
    filename = sys.argv[-1]
    print 'Converting: '+ filename
    f_in = open(filename, 'rb')
    rtf = publish_string(f_in.read(), writer=AsciiDocWriter())
    f_in.close()

    filename = filename+'.adoc'
       
    f_out = open(filename, 'wb')
    f_out.write(rtf)
    print 'Converted file: ' + filename
    f_out.close()
