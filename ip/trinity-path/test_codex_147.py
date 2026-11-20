from codex_147 import CodexNode, all_nodes, from_node_id
import pytest

def test_147_unique_nodes():
    assert sorted(n.node_id for n in all_nodes())==list(range(1,148))

def test_approved_node_77():
    assert CodexNode(3,4,1).node_id==77

def test_reverse_mapping():
    assert all(from_node_id(n.node_id) == n for n in all_nodes())
    assert from_node_id(84).as_dict() == {"node_id":84,"chakra":"Heart","principle":"Legacy","dantian":"Upper"}

def test_invalid_dimensions():
    with pytest.raises(ValueError):
        CodexNode(7,0,0)
    with pytest.raises(ValueError):
        from_node_id(148)
