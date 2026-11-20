from codex_147 import CodexNode, all_nodes
import pytest

def test_147_unique_nodes():
    assert sorted(n.node_id for n in all_nodes())==list(range(1,148))

def test_author_example_needs_reconciliation():
    assert CodexNode(3,4,1).node_id==77

def test_invalid_dimensions():
    with pytest.raises(ValueError):
        CodexNode(7,0,0)
