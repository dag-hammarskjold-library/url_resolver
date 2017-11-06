import xml.etree.ElementTree as ET
from io import BytesIO
from urllib import request
import ssl
from pymarc import marcxml
import re
from urllib import parse

# FIXME want to import this from common module
base_url = 'https://digitallibrary.un.org'
path = '/search'

subject_re = re.compile(r'^\d{7} unbis[nt] (.+)$')


class PageNotFoundException(Exception):
    pass


class MARCXmlParse:
    '''
        # FIXME -- this is NOT effecient
        given a url, e.g.
            https://digitallibrary.un.org/record/696939/export/xm
        get the xml via urllib request
        save the xml to a BytesIO object
        use pymarc to pull out fields:  
            author
            leader
            location
            notes
            physicaldescription
            pos
            publisher
            pubyear
            series
            subjects
            title
            uniformtitle
            for sub in rec.subjects():
                m = marc_re.match(str(sub))
                if m:
                    print(m.group(1))
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

    # def uniformtitle(self):
    #     return [elem.value() for elem in self.record.uniformtitle()]
        
    def subjects(self):
        subjs = {}
        for sub in self.record.subjects():
            print("Subject: {}".format(sub.value()))
            m = subject_re.match(sub.value())
            if m:
                search_string = parse.quote_plus(m.group(1))
                query = "f1=subject&as=1&sf=title&so=a&rm=&m1=p&p1={}&ln=en".format(search_string)
                subjs[m.group(1)] = base_url + path + '?' + query
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
            docs[rel_doc.value()] = '/symbol/{}'.format(rel_doc.value())
        return docs


    # def _generate_link(self, data)