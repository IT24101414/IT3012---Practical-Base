# agent.py

from logic_engine import KnowledgeBase

class Agent:
    def __init__(self):
        self.kb = KnowledgeBase()
        
        # Define safety rules
        self.kb.tell_rule(['TargetVisible', 'HasDust'], 'SafeToEngage')
        self.kb.tell_rule(['SafeToEngage', 'BloodseekerMissing'], 'Retreat')
    
    def is_tile_feasible(self, percepts):
        """
        Check if a tile is feasible based on logical reasoning.
        
        Args:
            percepts: list of fact strings at this tile
        
        Returns:
            bool: True if tile is safe, False if retreat is required
        """
        # Clear previous facts
        self.kb.clear_facts()
        
        # Add current percepts as facts
        for fact in percepts:
            self.kb.tell_fact(fact)
        
        # Run inference
        self.kb.forward_chain()
        
        # Check if Retreat was deduced
        return 'Retreat' not in self.kb.facts
    
    def test_feasibility(self):
        """Test the feasibility checking"""
        # Test 1: Safe tile
        percepts = ['TargetVisible', 'HasDust']
        result = self.is_tile_feasible(percepts)
        print(f"Test 1 (Safe): {'Passed' if result else 'Failed'}")
        
        # Test 2: Unsafe tile (Retreat required)
        percepts = ['TargetVisible', 'HasDust', 'BloodseekerMissing']
        result = self.is_tile_feasible(percepts)
        print(f"Test 2 (Retreat): {'Passed' if not result else 'Failed'}")

if __name__ == "__main__":
    agent = Agent()
    agent.test_feasibility()