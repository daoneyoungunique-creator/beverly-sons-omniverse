"""147 Codex deterministic developmental node registry (draft indexing)."""
from dataclasses import dataclass

CHAKRAS=("Root","Sacral","Solar","Heart","Throat","Third Eye","Crown")
PRINCIPLES=("Truth","Balance","Reciprocity","Responsibility","Justice","Harmony","Legacy")
DANTIAN=("Lower","Middle","Upper")

@dataclass(frozen=True)
class CodexNode:
    chakra: int
    principle: int
    dantian: int

    def __post_init__(self):
        if not 0 <= self.chakra < 7 or not 0 <= self.principle < 7 or not 0 <= self.dantian < 3:
            raise ValueError("Expected zero-based chakra 0..6, principle 0..6, dantian 0..2")

    @property
    def node_id(self) -> int:
        return self.chakra * 21 + self.principle * 3 + self.dantian + 1

    def as_dict(self) -> dict:
        return {"node_id":self.node_id,"chakra":CHAKRAS[self.chakra],
                "principle":PRINCIPLES[self.principle],"dantian":DANTIAN[self.dantian]}

def all_nodes():
    return [CodexNode(c,p,d) for c in range(7) for p in range(7) for d in range(3)]

if __name__=="__main__":
    assert len({n.node_id for n in all_nodes()})==147
    print(f"147 developmental nodes; Heart + Justice + Middle is node {CodexNode(3,4,1).node_id}")
