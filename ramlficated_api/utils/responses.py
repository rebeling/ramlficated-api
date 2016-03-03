# -*- coding: utf-8 -*-


def example(responses, code=None, key='description'):
    # print resource_responses
    example = None
    # print responses
    for res in responses:
        # print res
        if code:
            if code == res.code:
                # print ">>", res.raw
                example = res.raw[code][key]
    # print example
    return example


def message(responses, code, doc, request_url):
    doc = example(responses, code=code)
    return {'status': code, 'message': '{} {}'.format(doc, request_url)}


def response_info(success, doc, responses, code=None, request_url=None):

    if code == 500:
        doc = {'status': 500,
               'message': '{} {}'.format(doc, request_url)}
    else:
        first = '2' if success else '4'
        x = [x for x in responses if repr(x.code).startswith(first)][0]
        code = x.code
        if doc is None or first == '4':
            doc = message(responses, code, doc, request_url)

    return doc, code
