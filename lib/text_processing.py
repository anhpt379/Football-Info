#! coding: utf-8
import string
import re
from xml.dom.minidom import parseString


def xml_format(s):
    try:
        s = str(s)
    except:
        pass
    s = s.strip()
    s = s.replace("&", "&amp;") # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace("'", '&#39;')
    s = s.replace('"', '&quot;')
    return s

def xml_decode(s):
    s = s.strip()
    s = s.replace("&amp;", "&") # Must be done first!
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace('&#39;', "'")
    s = s.replace('&quot;', '"')
    return s

def normalize(s):
    """ 
    Chuẩn hoá chuỗi:
    - Các ký tự đầu viết hoa
    - Ký tự thứ 2 trở đi viết thường
    - Các từ cách nhau bởi một khoảng trống
    - Chuẩn hoá cách viết các dấu câu
    """
    s = s.split()
    s = ' '.join(x for x in s)
    s = s.replace('(', '( ')
    s = string.capwords(s)
    s = s.replace('( ', '(').replace(' )', ')').replace(' !', '!').replace(' ?', '?')
    return s

def remove_special_chars(s):
    specialChars = '''~`!#$%^()_+={}[]|:;"<>?/\\'''
    s = ''.join(x for x in s if x not in specialChars)
    return ' '.join(x for x in s.split())

def get_text(begin_str, end_str, document):
    """ Trả về các ký tự nằm giữa 2 chuỗi """
    s = begin_str + '(.*?)' + end_str
    return re.compile(s, re.DOTALL | re.IGNORECASE).findall(document)

def unsign(utf8_encoded):
    IN = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđẠẢÃÀÁÂẬẦẤẨẪĂẮẰẶẲẴÓÒỌÕỎÔỘỔỖỒỐƠỜỚỢỞỠÉÈẺẸẼÊẾỀỆỂỄÚÙỤỦŨƯỰỮỬỪỨÍÌỊỈĨÝỲỶỴỸĐëËäÄöÖüÜñÑïÏ"
    IN = [ch.encode('utf8') for ch in unicode(IN, 'utf8')]
    OUT = "a" * 17 + "o" * 17 + "e" * 11 + "u" * 11 + "i" * 5 + "y" * 5 + "d" + "A" * 17 + "O" * 17 + "E" * 11 + "U" * 11 + "I" * 5 + "Y" * 5 + "D" + "e" + "E" + "a" + "A" + "o" + "O" + "u" + "U" + "n" + "N" + "i" + "I"
    r = re.compile("|".join(IN))
    replaces_dict = dict(zip(IN, OUT))
    utf8_encoded = utf8_encoded.encode('utf-8')
    return r.sub(lambda m: replaces_dict[m.group(0)], utf8_encoded)

def unique(a):
    """ return the list with duplicate elements removed """
    return list(set(a))

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

def pretty_xml(xml_string):
    return '\n'.join([line for line in parseString(xml_string).toprettyxml(indent=' ' * 4, encoding='utf-8').split('\n') if line.strip()])

def raw_unicode_string(s):
    return repr(unicode(s))

if __name__ == '__main__':
  title = u"Phạm Tuấn Anh"
  import unicodedata
  _unsign = lambda s: unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
  print _unsign(title)
