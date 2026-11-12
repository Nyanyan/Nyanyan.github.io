import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


GENERATOR = Path(__file__).with_name('generate_html.py')


class MarkdownTableTests(unittest.TestCase):
    def render(self, markdown):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'generated').mkdir()
            (root / 'ja').mkdir()
            files = {
                'lang.txt': 'Japanese ja\n',
                'main_page_url.txt': 'https://example.com/',
                'ja/head.html': '',
                'ja/head2.html': '',
                'ja/menu_elements.txt': '',
                'ja/tweet.html': '',
                'ja/foot.html': '',
                'ja/description.txt': '',
                'ja/style.css': '.table_wrapper { overflow-x: scroll; }',
                'ja/title.txt': 'Test',
                'ja/index.md': markdown,
            }
            for name, contents in files.items():
                (root / name).write_text(contents, encoding='utf-8')
            subprocess.run(
                [sys.executable, str(GENERATOR), 'ja'], cwd=root,
                check=True, capture_output=True, encoding='utf-8',
            )
            return (root / 'generated/ja/index.html').read_text(encoding='utf-8')

    def test_table_and_surrounding_paragraphs(self):
        html = self.render(
            'Before\n\n| Year | Achievement |\n| --- | --- |\n'
            '| 2026 | Award |\n\nAfter\n'
        )
        self.assertIn('<p>Before</p><div class="table_wrapper"><table>', html)
        self.assertIn('<thead><tr><th>Year</th><th>Achievement</th></tr></thead>', html)
        self.assertIn('<tbody><tr><td>2026</td><td>Award</td></tr></tbody>', html)
        self.assertIn('</table></div><p>After</p>', html)
        self.assertNotIn('---', html)

    def test_optional_outer_pipes_and_alignment(self):
        html = self.render(
            'Left | Center | Right\n:--- | :---: | ---:\nA | B | 123\n'
        )
        for tag in ('th', 'td'):
            for alignment in ('left', 'center', 'right'):
                self.assertIn('<' + tag + ' style="text-align: ' + alignment + '">', html)

    def test_escaped_pipes_and_even_backslashes(self):
        html = self.render(
            '| Heading \\| text | Other |\n| --- | --- |\n'
            '| A \\| B | C |\n'
            r'| path\\| second |' + '\n'
        )
        self.assertIn('<th>Heading | text</th><th>Other</th>', html)
        self.assertIn('<td>A | B</td><td>C</td>', html)
        self.assertIn('<td>path' + '\\' * 2 + '</td><td>second</td>', html)

    def test_existing_inline_formatting_inside_cells(self):
        html = self.render(
            '| **Name** | Link |\n| --- | --- |\n'
            '| **Award** | [Details](https://example.com/award) |\n'
            '| ```A \\| B``` | [Local](./local) |\n'
        )
        self.assertIn('<th><b>Name</b></th>', html)
        self.assertIn('<td><b>Award</b></td>', html)
        self.assertIn('href="https://example.com/award"', html)
        self.assertIn('>Details</a></td>', html)
        self.assertIn('<td><code>A | B</code></td>', html)
        self.assertIn('<td><a href="./local">Local</a></td>', html)

    def test_missing_and_extra_cells(self):
        html = self.render(
            '| A | B |\n| --- | --- |\n| One |\nOnly one cell\n| One | Two | Extra |\n'
        )
        self.assertIn('<tr><td>One</td><td></td></tr>', html)
        self.assertIn('<tr><td>Only one cell</td><td></td></tr>', html)
        self.assertIn('<tr><td>One</td><td>Two</td></tr>', html)
        self.assertNotIn('Extra', html)

    def test_header_only_table(self):
        html = self.render('| Header |\n| --- |\n\nFollowing paragraph\n')
        self.assertIn('<th>Header</th>', html)
        self.assertIn('<tbody></tbody></table></div><p>Following paragraph</p>', html)

    def test_single_column_with_optional_pipes(self):
        html = self.render('Header |\n---\nOne\nTwo\n\nAfter\n')
        self.assertIn('<th>Header</th>', html)
        self.assertIn('<tr><td>One</td></tr><tr><td>Two</td></tr>', html)
        self.assertIn('</table></div><p>After</p>', html)

    def test_inline_html_without_outer_pipes(self):
        html = self.render('Name | Value\n--- | ---\n<span>A</span> | B\n')
        self.assertIn('<td><span>A</span></td><td>B</td>', html)

    def test_invalid_separators_remain_text(self):
        for markdown in (
            '| A | B |\n| --- |\n',
            '| A | B |\n| --- | words |\n',
            'A \\| B\n--- \\| ---\n',
            'Ordinary | prose\nAnother paragraph\n',
        ):
            with self.subTest(markdown=markdown):
                html = self.render(markdown)
                self.assertNotIn('<table>', html)
                self.assertNotIn('<th>', html)

    def test_existing_html_and_raw_blocks(self):
        html = self.render(
            '<div class="table_wrapper">\n<table>\n<tbody>\n'
            '<tr><th>Existing</th></tr>\n<tr><td>Value</td></tr>\n'
            '</tbody>\n</table>\n</div>\n\n'
            '<script>\nconst text = `\n| A | B |\n| --- | --- |\n`\n</script>\n'
        )
        self.assertEqual(html.count('<table>'), 1)
        self.assertIn('<tr><th>Existing</th></tr>', html)
        self.assertIn('<tr><td>Value</td></tr>', html)
        self.assertNotIn('<thead>', html)

    def test_fenced_and_indented_text_is_not_a_table(self):
        for markdown in (
            '```text\n| A | B |\n| --- | --- |\n| C | D |\n```\n',
            '~~~\n| A | B |\n| --- | --- |\n~~~\n',
            '    | A | B |\n    | --- | --- |\n',
        ):
            with self.subTest(markdown=markdown):
                self.assertNotIn('<table>', self.render(markdown))

    def test_table_ends_before_a_heading_or_list(self):
        for following in ('## Heading | text', '- Item | text', '---', '<div>Block</div>'):
            with self.subTest(following=following):
                html = self.render('| A | B |\n| --- | --- |\n| C | D |\n' + following)
                self.assertIn('<tbody><tr><td>C</td><td>D</td></tr></tbody>', html)
                if following.startswith('#'):
                    self.assertIn('</table></div><h2 id="Heading | text">', html)
                elif following.startswith('- '):
                    self.assertIn('</table></div><ul>\n<li>Item | text</li>', html)
                else:
                    self.assertIn('</table></div>' + ('<p>---</p>' if following == '---' else following), html)

    def test_list_before_table_is_closed(self):
        html = self.render('- Item\n| A | B |\n| --- | --- |\n| C | D |\n')
        self.assertIn('<li>Item</li>\n</ul><div class="table_wrapper"><table>', html)

    def test_multiple_tables(self):
        html = self.render(
            '| First |\n| --- |\n| One |\n\n'
            '| Second | Other |\n| --- | --- |\n| Two | Three |\n'
        )
        self.assertEqual(html.count('<div class="table_wrapper">'), 2)
        self.assertEqual(html.count('</table>'), 2)
        self.assertIn('<th>First</th>', html)
        self.assertIn('<th>Second</th><th>Other</th>', html)


if __name__ == '__main__':
    unittest.main()
