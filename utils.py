import difflib

def truncate(text, max_len=30):
    return text[:max_len] + "..." if len(text) > max_len else text


def diff_texts(text1, text2):
    d = difflib.HtmlDiff()
    return d.make_file(text1.splitlines(), text2.splitlines(), fromdesc='Branch A', todesc='Branch B')