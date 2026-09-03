# logic_engine.py

class KnowledgeBase:
    def __init__(self):
        # Facts stored as a set (no duplicates)
        self.facts = set()
        # Rules stored as list of tuples: (premises_list, conclusion)
        self.rules = []
    
    def tell_fact(self, fact_string):
        """Add a fact to the knowledge base"""
        self.facts.add(fact_string)
    
    def tell_rule(self, premise_list, conclusion_string):
        """Add a rule to the knowledge base"""
        self.rules.append((premise_list, conclusion_string))
    
    def clear_facts(self):
        """Clear all facts from the knowledge base"""
        self.facts.clear()
    
    def forward_chain(self):
        """
        Forward chaining inference engine.
        Continues to apply rules until no new facts can be deduced.
        """
        new_facts_added = True
        
        while new_facts_added:
            new_facts_added = False
            
            # Check each rule
            for premises, conclusion in self.rules:
                # Only check if conclusion not already known
                if conclusion not in self.facts:
                    # Check if all premises are in facts (Modus Ponens)
                    if all(premise in self.facts for premise in premises):
                        # Add the conclusion as a new fact
                        self.facts.add(conclusion)
                        new_facts_added = True
                        # Break to restart the loop with new facts
                        break