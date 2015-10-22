# from django.test import TestCase
from unittest import TestCase
import unittest
import re
from html import unescape, escape

text = """
<code-block>
    <head>
      <meta charset="utf-8">
      <title>OMG</title>
    </head>
</code-block>
<code-block><h1>OMG THIS WORKS</h1></code-block>
"""

expected_result = """
<code-block>
    &lt;head&gt;
      &lt;meta charset=&quot;utf-8&quot;&gt;
      &lt;title&gt;OMG&lt;/title&gt;
    &lt;/head&gt;
</code-block>
<code-block>&lt;h1&gt;OMG THIS WORKS&lt;/h1&gt;</code-block>
"""

def encode_text(match):
    match = match.group(0)
    return escape(match)


class RegExTestCase(TestCase):

    pattern = re.compile(r"(?<=\<code-block\>)(.*?)(?=\<\/code-block\>)", re.DOTALL)

    def test_reg_ex(self):
        matches = self.pattern.group(text).group()
        self.assertIsNotNone(matches)
        self.assertEqual(len(matches), 1)

    def test_replace(self):
        result = re.sub(self.pattern, encode_text, text)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
