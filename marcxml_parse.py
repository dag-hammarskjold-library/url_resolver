import xml.etree.ElementTree as ET
from io import BytesIO
from urllib import request
import ssl
from pymarc import marcxml


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
        return [sub.value() for sub in self.record.subjects()]

    def notes(self):
        return [note.value() for note in self.record.notes()]

    def publisher(self):
        return self.record.publisher()

    def pubyear(self):
        return self.record.pubyear()

    def document_symbol(self):
        return self.record.document_symbol()

    def related_documents(self):
        return self.record.related_documents()
