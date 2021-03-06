from ... environment import cfg
from ... run_cli import Arguments

from .. lsh import lsh

from . elasticfactor import ElasticFactor
from elasticsearch import Elasticsearch

import time


def create_index(es, name):
    """
    :param es: <Elasticsearch>
        Elasticsearch Instance
    :param name: str
        Name of newly created index

    :return: Acknowledged
    :rtype:  dict
    """
    if not es.indices.exists(name):
        return es.indices.create(index=name)
    else:
        return {'acknowledged': False}


def run(node):
    es = Elasticsearch()

    create_index(es, 'factor_state2016')

    ad_id, factors = node.get('id', '63166071'), node.get('factors', ['phone', 'email', 'text', 'title'])
    constructor = ElasticFactor(cfg["cdr_elastic_search"]["hosts"] + cfg["cdr_elastic_search"]["index"])
    initialized    = constructor.initialize(ad_id, *factors)

    # If Text Factor is Selected, run LSH to get near duplicates
    if 'text' in factors and initialized[ad_id]['text']:
        initialized[ad_id]['lsh'] = {}
        for text in initialized[ad_id]['text']:
            initialized[ad_id]['lsh'][text] = list(lsh(Arguments(text, 1000)))
    index_id = ad_id + "_1"
    initialized["_id"] = index_id
    res = es.index(index="factor_state2016", id=index_id, doc_type="factor_network", body=initialized)
    return initialized
