import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent import search, run
class AgentTests(unittest.TestCase):
    def test_rank(self): self.assertEqual(search('agent tools', {'b':'agent', 'a':'agent tools'})[0][1], 'a')
    def test_no_match(self): self.assertIn('No matching evidence', run('bananas', {'x':'other'}))
    def test_citation(self): self.assertIn('[source.md]', run('tools', {'source.md':'Tools help.'}))
    def test_stopwords(self): self.assertEqual(search('the and', {'x':'the'}), [])
if __name__ == '__main__': unittest.main()
