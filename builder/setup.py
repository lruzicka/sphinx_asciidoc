from setuptools import setup
import sphinx

setup(
    name = 'asciidoc',
    entry_points = {
        'sphinx.builders': [
            'asciidoc = asciidoc:AsciiDocBuilder',
        ],
    }
)
