'''
Created on 20 Oct. 2018

@author: Michael
'''
import os, uuid
CONFIG = {
          'host':'127.0.0.1',
          'user':'mikebauer',
          'passwd':'firefly!',
          'db':'clublite'
          }

DEBUG = True

#Time Zone settings
TIME_ZONE = 'Australia/Sydney'

URL = "https://sunred.zira.com.au/"
DIR = "/home/zira/alexa-python-web-to-device"

AMAZON_AUTH_ENDPOINT = "https://api.amazon.com/auth/O2/create/codepair"
AMAZON_TOKEN_ENDPOINT = "https://api.amazon.com/auth/O2/token"
CLIENT_ID = os.environ.get('ALEXA_CLIENT_ID',"")
CLIENT_SECRET = os.environ.get('ALEXA_CLIENT_SECRET',"")
PRODUCT_ID = os.environ.get('ALEXA_PRODUCT_ID','')
REFRESH_TOKEN = os.environ.get('ALEXA_REFRESH_TOKEN',"")
WEB_PORT = int(os.environ.get('ALEXA_PORT',3000))

SCOPE_DATA = {
        "alexa:all": {
            "productID": PRODUCT_ID,
            "productInstanceAttributes": {
               # "deviceSerialNumber": uuid.getnode()
               "deviceSerialNumber": "1234"
            }
        }
    }

LOGIN_PAYLOAD = {
        "client_id": CLIENT_ID,
        "scope": "alexa:all",
        "scope_data": SCOPE_DATA,
        "response_type": "code",
        "redirect_uri": URL
    }

#WYSIWYG Settings
def sanitize_iframe(attr,value):
    if attr in ['frameborder','src','width','height','sandbox',
                'name','align','scrolling','marginheight','marginwidth']:
        if attr=='src':
            ALLOWED_URLS = ['https://www.youtube.com/embed',
                            '//www.youtube.com/embed'
                            ]
            for url in ALLOWED_URLS:
                if value.startswith(url):
                    return True
            return False
        else:
            return True    
    return False

ALLOWED_TAGS = [
    'a', 'b', 'blockquote',
    'br', 'caption', 'cite',
    'code', 'col', 'hr',
    'h2', 'h3', 'h4',
    'h5', 'h6', 'h7',
    'h8', 'del', 'ins',
    'colgroup', 'dd', 'div',
    'dl', 'dt', 'em',
    'i', 'img', 'li',
    'ol', 'p', 'pre',
    'q', 'small', 'span',
    'strike', 'strong', 'sub',
    'sup', 'table', 'tbody',
    'td', 'tfoot', 'th',
    'thead', 'tr', 'u',
    'ul', 'param', 'video',
    'track', 'audio', 'source',
    'caption', 'abbr', 'acronym',
    's','del', 'caption',
    'map','area','font',
    'iframe','wbr'
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title','target'],
    'abbr': ['title'],
    'acronym': ['title'],
    'area':['shape','coords','href','alt','target'],
    'blockquote':['cite'],
    'col':['span','width'],
    'colgroup':['span','width'],
    'font':['face','size','color'],
    'img':['src','align','alt','height','width','usemap','title','data-filename'],
    'ol':['start','type'],
    'q':['cite'],
    'table':['summary','width','border','cellpadding','cellspacing','center','frame','rules'],
    'tr':['align','valign','dir'],
    'td':['abbr', 'axis', 'colspan', 'rowspan', 'width', 'align', 'valign', 'dir'],
    'th':['abbr', 'axis', 'colspan', 'rowspan', 'width', 'align', 'valign', 'dir', 'scope'],
    'ul':['type'],
    'param':['name','value'],
    'video':['width','height','controls','muted','loop','autoplay','poster','src','muted'],
    'source':['src','type'],
    'audio':['src','muted','type','loop','controls','autoplay'],
    'iframe':sanitize_iframe
}

for tag in ALLOWED_TAGS:
    if not tag=='iframe':
        if tag in ALLOWED_ATTRIBUTES:
            ALLOWED_ATTRIBUTES[tag].extend(['style','name','id','class'])
        else:
            ALLOWED_ATTRIBUTES[tag] = ['style','name','id','class']

ALLOWED_STYLES = [
    'background', 'border', 'clear', 
    'color', 'cursor', 'direction', 
    'display', 'float', 'font', 
    'font-family', 'font-weight',
    'height', 'left line-height','list-style', 
    'margin', 'max-height', 'max-width', 
    'min-height', 'min-width', 'overflow overflow-x', 
    'overflow-y','padding', 'position', 
    'right', 'text-align', 'table-layout', 
    'text-decoration', 'text-indent', 'top', 
    'vertical-align','visibility', 'white-space', 
    'width','z-index', 'zoom', 'background-color',
]

DEREFERENCE_HTML = (
                    #&amp; is unnecessary as this is
                    #looped over no matter while until none exist
                    #in order to prevent '&amp;amp;amp;amp' etc...
                    ('&lt;','<'),
                    ('&gt;','>'),
                    #('&quot;','"'), #Causes some CSS issues, shouldn't be a security issue
                    ('&#39;',"'"),
                    ('&#x2F;','/'),
                    ('&#x60;','`'),
                    ('&#x3D;','='),
                    )