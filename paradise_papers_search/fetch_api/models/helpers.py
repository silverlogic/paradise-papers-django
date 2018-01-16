from neomodel import db
from . import (
    Entity,
    Address,
    Intermediary,
    Officer,
    Other
)

MODEL_ENTITIES = {
    'entity': Entity.Entity,
    'address': Address.Address,
    'intermediary': Intermediary.Intermediary,
    'officer': Officer.Officer,
    'other': Other.Other
}

# Queries Functions
def filter_nodes(node_type, name, country, jurisdiction):
    node_set = node_type.nodes
    if node_type.__name__ == 'Address':
        node_set.filter(address__icontains=name)
    else:
        node_set.filter(name__icontains=name)
    if not node_type.__name__ == 'Other':
        node_set.filter(countries__icontains=country)
    if node_type.__name__ == 'Entity':
        node_set.filter(jurisdiction__icontains=jurisdiction)
    return node_set

def count_nodes(count_info):
    count = {}
    node_type               = count_info['node_type']
    search_word             = count_info['name']
    country                 = count_info['country']
    jurisdiction            = count_info['jurisdiction']
    node_set                = filter_nodes(MODEL_ENTITIES[node_type], search_word, country, jurisdiction)
    count['count']          = len(node_set)

    return count

def fetch_nodes(fetch_info):
    node_type       = fetch_info['node_type']
    search_word     = fetch_info['name']
    country         = fetch_info['country']
    limit           = fetch_info['limit']
    skip            = ((fetch_info['skip'] - 1) * limit)
    jurisdiction    = fetch_info['jurisdiction']
    node_set        = filter_nodes(MODEL_ENTITIES[node_type], search_word, country, jurisdiction)
    node_set.limit  = limit
    node_set.skip   = skip
    fetched_nodes   = node_set.all()

    return [node.serialize for node in fetched_nodes]


def fetch_node_details(node_info):
    node_type       = node_info['node_type']
    node_id         = node_info['node_id']
    node            = MODEL_ENTITIES[node_type].nodes.get(node_id=node_id)
    node_details    = node.serialize
    if (hasattr(node, 'serialize_connections')):
        node_details['conections'] = node.serialize_connections

    return node_details

def serialize_relationship(nodes, relationship):
    serialized_nodes = []
    for node in nodes:
        serialized_node = node.serialize
        serialized_node['relationship'] = relationship
        serialized_nodes.append(serialized_node)

    return serialized_nodes
