# -*- coding: utf-8 -*-
from flask import Flask, request
app = Flask(__name__)

from .marcxml_parse import MARCXmlParse
from .symbol_cache import SymbolCache
from bs4 import BeautifulSoup
from collections import defaultdict
from flask import jsonify, render_template, abort
from io import BytesIO
from logging import getLogger
from lxml import etree
from urllib import request as req
from urllib.parse import quote_plus, urljoin
import re
import re
import ssl
import xml.etree.ElementTree as ET

logger = getLogger(__name__)

context = ssl._create_unverified_context()
base_url = 'https://digitallibrary.un.org'
ns = '{http://www.loc.gov/MARC21/slim}'
sc = SymbolCache()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


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
    rec_id = _get_record_id(search_string)
    links = _get_pdf(rec_id)
    marc_dict = _get_marc_metadata(rec_id)

    langs = ['EN', 'ES', 'FR', 'DE', 'RU', 'AR', 'ZH']
    ctx = {}
    ctx['metadata'] = marc_dict
    for link in links:
        for lang in langs:
            if re.search(lang, link):
                ctx[lang] = base_url + link

    return render_template('index.html', context=ctx)


def _get_pdf(record_id):
    resp = req.urlopen(base_url + '/record/{}'.format(record_id), context=context)
    html = resp.read()
    soup = BeautifulSoup(html, 'html.parser')  
    links = defaultdict(int)
    for pdf in soup.find_all(string=re.compile('PDF')):
        a = pdf.find_previous('a')
        link = a.get('href')
        links[link] = 1
    logger.debug(links)

    return links
   
def _get_marc_metadata(record_id):
    url = base_url + '/record/{}'.format(record_id) + '/export/xm'
    parser = MARCXmlParse(url)
    ctx = {
        'title': parser.title(),
        'symbol': parser.symbol(),
        'subjects': parser.subjects(),
        'addedentries': parser.addedentries(),
        'references': parser.cross_reference()
    }
    return ctx

def _get_record_id(search_string):
    document_id = _check_symbol_cache(search_string)
    if document_id:
        return int(document_id)

    path = '/search'
    query = "ln=en&p={}&c=Resource+Type&c=UN+Bodies&fti=0&so=d&rg=10&sc=0&of=xm".format(search_string)
    resp = req.urlopen(
        base_url + path + '?' + query,
        context=context
    )
    if resp.status != 200:
        abort(404)
    xml = resp.read()
    if not xml:
        abort(404)
    root = ET.fromstring(xml)
    elems = root.findall('.//{}controlfield[@tag="001"]'.format(ns))
    if elems == []:
        logger.error("Could not find a record for {}".format(search_string))
        abort(404)
    try:
        rec_id = elems[0].text
    except IndexError as e:
        logger.error("Caught Exception in {}, {}".format(__name__, e))
        abort(404)

    _set_symbol_cache(search_string, rec_id)
    return rec_id

def _check_symbol_cache(search_string):
    document_id = sc.get(search_string)
    if document_id:
        return document_id
    else:
        return None

def _set_symbol_cache(search_string, document_id):
    sc.set(search_string, document_id)

