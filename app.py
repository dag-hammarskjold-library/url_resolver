from flask import Flask
from flask import render_template, abort, redirect
from urllib import request as req
from urllib.parse import quote_plus
from io import BytesIO
import re
import ssl
import xml.etree.ElementTree as ET
from pymarc import marcxml
from urllib import parse

base_url = 'https://digitallibrary.un.org'
ns = '{http://www.loc.gov/MARC21/slim}'
path = '/search'

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
        resp = req.urlopen(url, context=ssl._create_unverified_context())
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
            app.logger.debug("Subject: {}".format(sub.value()))
            m = subject_re.match(sub.value())
            if m:
                search_string = parse.quote_plus(m.group(1))
                query = "f1=subject&as=1&sf=title&so=a&rm=&m1=p&p1={}&ln=en".format(search_string)
                subjs[m.group(1)] = base_url + path + '?' + query
        app.logger.debug(subjs)
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
            app.logger.debug("Related Doc: {}".format(rel_doc.value()))
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


app = Flask(__name__)
context = ssl._create_unverified_context()

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(e)
    return render_template('404.html'), 404

@app.route('/')
def redirect_to_symbol():
    # pick a General Assembly resolution -- like A/RES/52/115
    return redirect('/symbol/A/RES/52/115')

@app.route('/symbol', defaults={'path': ''})
@app.route('/symbol/<path:search_string>')
def index(search_string):
    """
    @ags: search string : of the format S/RES/198, or ST/IC/2010/12
    raises: 404
    returns: dict

    pass a search string on the URL
    try to get an XML document back from base_url based on that search string
    if this xml exists, get the record id
    using the record id call _get_pdf -- gets location of PDF files assoc to search_string
    record id's are internal to envivio.
    document symbols (search strings) are known and used by users of UNDL
    """
    search_string = quote_plus(search_string)
    app.logger.info(search_string)
    rec_id = _get_record_id(search_string)
    urls = _get_pdf_urls(rec_id)
    marc_dict = _get_marc_metadata(rec_id)

    langs = ['EN', 'ES', 'FR', 'DE', 'RU', 'AR', 'ZH']
    ctx = {}
    ctx['metadata'] = marc_dict
    for url in urls:
        for lang in langs:
            if re.search('-{}\.pdf'.format(lang), url):
                ctx[lang] = url

    return render_template('index.html', context=ctx)


def _get_marc_metadata(record_id):
    '''
    use the xml format of the page
    to nab metadata
    '''
    url = base_url + '/record/{}'.format(record_id) + '/export/xm'
    parser = MARCXmlParse(url)
    ctx = {
        'title': parser.title(),
        'author': parser.author(),
        'subjects': parser.subjects(),
        'notes': parser.notes(),
        'publisher': parser.publisher(),
        'pubyear': parser.pubyear(),
        'document_symbol': parser.document_symbol(),
        'related_documents': parser.related_documents(),
        'summary': parser.summary(),
        'agenda': parser.agenda()
    }
    return ctx

def _get_record_id(search_string):
    '''
    @args: search string
    @returns: undl internal record id
    @raises 404
    '''
    # https://github.com/dag-hammarskjold-library/pymarc/tree/dev

    path = '/search'
    query = "ln=en&p=191__a:\"{}\"&c=Resource+Type&c=UN+Bodies&fti=0&so=d&rg=10&sc=0&of=xm".format(search_string)
    app.logger.info("!! {}".format(search_string))
    app.logger.info("$$ {}".format(query))

    url_pattern = path + '?' + query
    root = _fetch_xml_root(url_pattern, search_string)
    elems = root.findall('.//{}controlfield[@tag="001"]'.format(ns))
    if elems == []:
        app.logger.debug("Could not find a record for {}".format(search_string))
        abort(404)
    try:
        rec_id = elems[0].text
    except IndexError as e:
        app.logger.debug("Caught Exception in {}, {}".format(__name__, e))
        abort(404)

    return rec_id


def _get_pdf_urls(record_id):
    urls = []
    root = _fetch_xml_root('/record/{}/?ln=en&of=xm', record_id)
    elems = root.findall('.//{0}datafield[@tag="856"]/{0}subfield[@code="u"]'.format(ns))
    urls = []
    if elems == []:
        app.logger.debug("Could not find a record for {}".format(record_id))
        abort(404)
    for elem in elems:
        try:
            urls.append(elem.text)
        except Exception as e:
            app.logger.error("Caught exception getting pdf urls: {}".format(e))
            abort(404)
    return urls

def _fetch_xml_root(url_pattern, param):
    url = base_url + url_pattern.format(param)
    resp = req.urlopen(url, context=ssl._create_unverified_context())
    if resp.status != 200:
        app.logger.debug("query {}, gave status: {}".format(url_pattern, resp.status))
        abort(404)
    xml = resp.read()
    if not xml:
        app.logger.debug("No XML for query: {}".format(url_pattern))
        abort(404)
    root = ET.fromstring(xml)
    return root

if __name__ == '__main__':
    app.run(debug=True)
