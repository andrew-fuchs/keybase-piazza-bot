import urllib

def piazza_post_url(network_id: str, post_nr: int):
    network_id_str = urllib.parse.quote_plus(network_id)
    post_nr = str(post_nr)
    post_nr_str = urllib.parse.quote_plus(post_nr)
    return 'https://piazza.com/class/{}?cid={}'.format(network_id_str, post_nr_str)
