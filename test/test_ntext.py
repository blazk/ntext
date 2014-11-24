import unittest
from ntext import Templates


class TestTemplates(unittest.TestCase):

    def setUp(self):
        self.templ = Templates()

    def test_parse_command(self):
        command = '<keyword, arg1=val1, arg2=val2>'
        it = iter(command)
        it.next()
        ret = self.templ._parse_command(it)
        self.assertEqual(ret, ('keyword', [('arg1', 'val1'), ('arg2', 'val2')]))

    def test_escaping_brackets_in_command(self):
        command = '<keyword, arg=cat\<file>'
        it = iter(command)
        it.next()
        ret = self.templ._parse_command(it)
        self.assertEqual(ret, ('keyword', [('arg', 'cat<file')]))

    def test_missing_nested_closing_bracket(self):
        command = '<keyword, arg=cat<file>'
        it = iter(command)
        it.next()
        self.assertRaises(Templates.SyntaxError, self.templ._parse_command, it)

    def test_command_with_command_argument_1(self):
        command = '<keyword, arg=<keyword2>>'
        it = iter(command)
        it.next()
        ret = self.templ._parse_command(it)
        self.assertEqual(ret, ('keyword', [('arg', '<keyword2>')]))

    @unittest.skip("doesn't work yet")
    def test_command_with_command_argument_2(self):
        command = '<keyword, arg=<keyword2, arg=val>>'
        it = iter(command)
        it.next()
        ret = self.templ._parse_command(it)
        self.assertEqual(ret, ('keyword', [('arg', '<keyword2, arg=val>')]))

    def test_expanding_command_keyword(self):
        command = '<run_<what>, what=test, run_test=ok>'
        ret = self.templ.expand(command)
        self.assertEqual(ret, 'ok')

    def test_empty_keyword(self):
        command = '<, ''=x>'
        ret = self.templ.expand(command)
        self.assertEqual(ret, 'x')
