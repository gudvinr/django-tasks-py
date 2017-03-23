'''
Some of useful hand-written helpers
'''


def html_esc(text: str) -> str:
    return text.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;')


def exc_parse(exc_info):
    line = None
    fname = None
    name = None
    desc = None

    try:
        name = exc_info[0].__name__
        desc = exc_info[1]
        frame = exc_info[2]

        while frame.tb_next:
            frame = frame.tb_next

        line = frame.tb_lineno
        fname = frame.tb_frame.f_code.co_filename
    except:
        pass

    return name, desc, fname, line
