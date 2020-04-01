import unittest
import wanttoread.wanttoread

class TestSum(unittest.TestCase):

  def test_get_title_fails_due_to_bad_xml(self):
    dummy_data = "dummy_data"
    with self.assertRaises(AttributeError):
      wanttoread.wanttoread.get_title(dummy_data)

if __name__ == '__main__':
    unittest.main()
