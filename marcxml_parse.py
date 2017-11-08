from .config import base_url, path
from io import BytesIO
from logging import getLogger
from pymarc import marcxml
from urllib import parse
from urllib import request
import re
import ssl
import xml.etree.ElementTree as ET

logger = getLogger(__name__)


subject_re = re.compile(r'^\d{6,7}\s(?:unbis[nt])*\s*(.+)$')
reldoc_re = re.compile(r'^([a-zA-Z0-9\/]+)(\(\d{4}\))$')


class PageNotFoundException(Exception):
    pass


class MARCXmlParse:
    '''
        given a url, e.g.
            https://digitallibrary.un.org/record/696939/export/xm
        parse the xml via pymarc.parse_xml_to_array
        use pymarc to pull out fields:  
            author
            notes
            publisher
            pubyear
            subjects
            title
            document symbol
            related documents
    '''
    def __init__(self, url):
        resp = request.urlopen(url, context=ssl._create_unverified_context())
        if resp.status != 200:
            raise PageNotFoundException("Could not get data from {}".format(url)) 
        self.xml_doc = BytesIO(resp.read())
        r = marcxml.parse_xml_to_array(self.xml_doc, False, 'NFC')
        self.record = r[0]

    def author(self):
        return self.record.author()

    def title(self):
        return self.record.title()

    def subjects(self):
        subjs = {}
        for sub in self.record.subjects():
            logger.debug("Subject: {}".format(sub.value()))
            m = subject_re.match(sub.value())
            if m:
                search_string = parse.quote_plus(m.group(1))
                query = "f1=subject&as=1&sf=title&so=a&rm=&m1=p&p1={}&ln=en".format(search_string)
                subjs[m.group(1)] = base_url + path + '?' + query
        logger.debug(subjs)
        return subjs

    def notes(self):
        return [note.value() for note in self.record.notes()]

    def publisher(self):
        return self.record.publisher()

    def pubyear(self):
        return self.record.pubyear()

    def document_symbol(self):
        return self.record.document_symbol()

    def related_documents(self):
        docs = {}
        for rel_doc in self.record.related_documents():
            logger.debug("Related Doc: {}".format(rel_doc.value()))
            m = reldoc_re.match(rel_doc.value())
            if m:
                rel_string = m.group(1) + '%20' + m.group(2)
                docs[rel_doc.value()] = '/symbol/{}'.format(rel_string)
            else:
                docs[rel_doc.value()] = '/symbol/{}'.format(rel_doc.value())
        return docs

    def summary(self):
        return self.record.summary()

    def agenda(self):
        return self.record.agenda()
