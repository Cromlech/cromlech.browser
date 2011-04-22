# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulStoneSoup
from optparse import OptionParser
import sys


class XMLSoup(BeautifulStoneSoup):

    def _smartPop(self, name):
        """We don't want to 'clean' the DOM.
        """
        pass


def xmlindent():
    """Indent an XML file.

    Can be used in emacs on your buffer with C-x h C-u M-S | path to
    the script Enter.
    """
    parser = OptionParser()
    (options, files) = parser.parse_args()

    if not files:
        input = ''
        data = sys.stdin.read()
        while data:
            input += data
            data = sys.stdin.read()
        print XMLSoup(input).prettify()
        return

    for filename in files:
        with open(filename, 'r') as input:
            print XMLSoup(input.read()).prettify()


def XMLDiff(xml1, xml2):
    """Assert that two XML content are the same, or fail with a
    comprehensive diff between them.

    You should not use this if you which to compare XML data where
    spaces does matter.
    """
    pretty_xml1 = XMLSoup(xml1.strip()).prettify()
    pretty_xml2 = XMLSoup(xml2.strip()).prettify()
    if pretty_xml1 != pretty_xml2:
        return ['XML differ:\n-expected\n+actual\n',] + \
               list(difflib.unified_diff(
            pretty_xml1.splitlines(True),
            pretty_xml2.splitlines(True), n=2))[2:]
    return None
