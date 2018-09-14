import re
import itertools

def cleanstring(input):
    output=re.sub(r"[,.;@#?!&$]+", ' ', input)  # + means match one or more
    output=re.sub(r"\s+", ' ', output)  # Replaces any number of spaces with one space
    return output

def cleanemoji(input):
    try:
        # Wide UCS-4 build
        myre = re.compile(u'['
        u'\U0001F300-\U0001F64F'
        u'\U0001F680-\U0001F6FF'
        u'\u2600-\u26FF\u2700-\u27BF]+', 
        re.UNICODE)
        return myre.sub(u' ', input)
    except re.error:
        # Narrow UCS-2 build
        myre = re.compile(u'('
        u'\ud83c[\udf00-\udfff]|'
        u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
        u'[\u2600-\u26FF\u2700-\u27BF])+', 
        re.UNICODE)
        return myre.sub(u' ', input)

def cleanreps(input):
    cleaned = ''.join(c[0] for c in itertools.groupby(input))
    return cleaned
