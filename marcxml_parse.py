import xml.etree.ElementTree as ET
from io import BytesIO
from urllib import request
import ssl


MARC_XML_NS = 'http://www.loc.gov/MARC21/slim'


class PageNotFoundException(Exception):
    pass


class MARCXmlParse:
    '''
        # FIXME -- this is NOT effecient
        given a url, e.g.
            https://digitallibrary.un.org/record/696939/export/xm
        get the xml via urllib request
        save the xml to a BytesIO object
        use etree.ElementTree to parse for known tags:
            symbol -> 191 $a
            title -> 239 $a
            title statement -> 245 $a, $b, $c
            Imprint -> 260 $a $b $c
            General Note -> (repeating) 500 $a
            subject added Corporate Name -> (repeating) 610 $a
            subject added uniform title -> (repeating) 630 $a
            subject added topic -> (repeating) 650 $a
            Subject Added Entry - Geographic Name (repeating) -> 651 $a
            
    '''
    def __init__(self, url):
        resp = request.urlopen(url, context=ssl._create_unverified_context())
        if resp.status != 200:
            raise PageNotFoundException("Could not get data from {}".format(url)) 
        self.xml_doc = BytesIO(resp.read())
        self.root = self._get_root(self.xml_doc)

    def _get_root(self, f_obj):
        tree = ET.parse(f_obj)
        return tree.getroot()

    def _find_text(self, tag, code='a'):
        text = []
        df = self.root.findall('.//{{{0}}}datafield[@tag="{1}"]'.format(MARC_XML_NS, tag))
        for elem in df:
            data = elem.find('.//{{{0}}}subfield[@code="{1}"]'.format(MARC_XML_NS, code))
            text.append(data.text)
        return text

    def symbol(self):
        try:
            df = self.root.find('.//{{{0}}}datafield[@tag="191"]'.format(MARC_XML_NS))
            symbol = df.find('.//{{{0}}}subfield[@code="a"]'.format(MARC_XML_NS))
            return symbol.text
        except AttributeError as ex:
            return None

    def title(self):
        try:
            df = self.root.find('.//{{{0}}}datafield[@tag="245"]'.format(MARC_XML_NS))
            title = df.find('.//{{{0}}}subfield[@code="a"]'.format(MARC_XML_NS))
            subtitle = df.find('.//{{{0}}}subfield[@code="b"]'.format(MARC_XML_NS))
            return "{} {}".format(title.text, subtitle.text)
        except AttributeError as ex:
            return None

    def uniformtitle(self):
        uniformtitles = []
        for tag in ['130', '240']:
            uniformtitles = self._find_text(tag)
        return uniformtitles
        
    def subjects(self):
        """
        Note: Fields 690-699 are considered "local" added entry fields but
        occur with some frequency in OCLC and RLIN records.
        """
        subjects = []
        try:
            df = self.root.findall('.//{{{0}}}datafield[@tag="650"]'.format(MARC_XML_NS))
            for sf in df:
                subj = sf.find('.//{{{0}}}subfield[@code="a"]'.format(MARC_XML_NS))
                subjects.append(subj.text)
            return subjects
        except AttributeError as ex:
            return None

    def cross_reference(self):
        references = []
        text = ''
        # import pdb
        # pdb.set_trace()
        try:
            df = self.root.findall('.//{{{0}}}datafield[@tag="991"]'.format(MARC_XML_NS))
            for elem in df:
                for sf in elem.getchildren():
                    if hasattr(sf, 'text'):
                        text += '| {0} '.format(sf.text)
                references.append(text)
                text = ''
            return references
        except AttributeError as ex:
            return None

    def addedentries(self):
        """
        Note: Fields 790-799 are considered "local" added entry fields but
        occur with some frequency in OCLC and RLIN records.
        """
        for tag in ['700', '710', '711', '720', '730', '740',
            '752', '753', '754', '790', '791', '792', '793', '796', '797',
            '798', '799']:
            addedentries = []
            addedentries = self._find_text(tag)
        return addedentries

    # def location(self):
    #     loc = self.get_fields('852')
    #     return loc

    # def notes(self):
    #     """
    #     Return all 5xx fields in an array.
    #     """
    #     notelist = self.get_fields('500', '501', '502', '504', '505',
    #         '506', '507', '508', '510', '511', '513', '514', '515',
    #         '516', '518', '520', '521', '522', '524', '525', '526',
    #         '530', '533', '534', '535', '536', '538', '540', '541',
    #         '544', '545', '546', '547', '550', '552', '555', '556',
    #         '561', '562', '563', '565', '567', '580', '581', '583',
    #         '584', '585', '586', '590', '591', '592', '593', '594',
    #         '595', '596', '597', '598', '599')
    #     return notelist

    # def physicaldescription(self):
    #     """
    #     Return all 300 fields in an array
    #     """
    #     return self.get_fields('300')

    # def publisher(self):
    #     """
    #     Note: 264 field with second indicator '1' indicates publisher.
    #     """
    #     for f in self.get_fields('260', '264'):
    #         if self['260']:
    #             return self['260']['b']
    #         if self['264'] and f.indicator2 == '1':
    #             return self['264']['b']

    #     return None

    # def pubyear(self):
    #     for f in self.get_fields('260', '264'):
    #         if self['260']:
    #             return self['260']['c']
    #         if self['264'] and f.indicator2 == '1':
    #             return self['264']['c']

    #     return None


