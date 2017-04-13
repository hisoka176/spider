# -*- coding: utf-8 -*-
import requests

URL = 'http://apis.baidu.com/apistore/idlocr/ocr'
LANG_LIST = ['CHN_ENG', 'ENG', 'JAP', 'KOR']


def ocr(picture, lang='CHN_ENG'):
    """Recognize a picture and return the text on it.

    picture could be a local picture or url of picture on web.

    lang should be one of CHN_ENG, ENG, JAP, KOR
    """
    data = {}
    data['fromdevice'] = "pc"
    data['clientip'] = '10.10.10.0'
    data['detecttype'] = 'Recognize'
    data['imagetype'] = "2"

    if lang not in LANG_LIST:
        raise Exception('invalid language: %s' % lang)
    else:
        data['languagetype'] = lang

    # �˴�Ӧʹ���Լ��� API key
    header = {"apikey": "your api key"}

    image_file = None
    try:
        if picture.startswith('http://') or picture.startswith('https://'):
            image_file = requests.get(picture).content
        else:
            image_file = open(picture, 'rb').read()
    except Exception:
        raise Exception('invalid picture: %s' % picture)

    resp = requests.post(URL, headers=header, data=data, files={"image": ("baidu.jpg", image_file)})

    if resp is not None:
        resp = resp.json()
        if  int(resp.get('errNum')) != 0:
            raise Exception(resp.get('errMsg'))
        else:
            return resp.get('retData')[0].get('word')
    else:
        return None