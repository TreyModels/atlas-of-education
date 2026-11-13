import pickle, unittest
from countries import cambodia
from eduengine import planning_audit
class BridgeTests(unittest.TestCase):
 def test_audit_preserves_state(self):
  E=cambodia.make(N=80,T=20,seed=7);E.run()
  before=pickle.dumps((E.R,E.kids,E.rng.bit_generator.state,E.p))
  r=planning_audit(E)
  self.assertEqual(before,pickle.dumps((E.R,E.kids,E.rng.bit_generator.state,E.p)))
  self.assertEqual(len(r['rows']),20)
  self.assertLess(r['maximumSalaryIdentityResidual'],1e-9)
if __name__=='__main__':unittest.main()
