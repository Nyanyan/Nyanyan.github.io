import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


GENERATOR = Path(__file__).with_name('generate_html.py')


class GeneratorTestCase(unittest.TestCase):
    def run_generator(self, markdown):
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
            process = subprocess.run(
                [sys.executable, str(GENERATOR), 'ja'], cwd=root,
                capture_output=True, encoding='utf-8',
            )
            output = root / 'generated/ja/index.html'
            return process, output.read_text(encoding='utf-8') if output.exists() else None

    def render(self, markdown):
        process, html = self.run_generator(markdown)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertIsNotNone(html)
        return html


class MarkdownTableTests(GeneratorTestCase):

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


class HtmlTileTests(GeneratorTestCase):
    def test_tiles_preserve_order_titles_paths_and_existing_classes(self):
        html = self.render(
            '# Works\nHTML_TILE_BEGIN\n- First\n  - ./first/\n  - img/first.jpg\n'
            '- Second<br>Details\n  - ./second/\n  - img/second.jpg\nHTML_TILE_END\nAfter\n'
        )
        self.assertEqual(html.count('<div class="eye_catch">'), 2)
        self.assertIn('<div style="text-align:center; line-height:0;">', html)
        self.assertIn('<a href="./first/"><img class="img" src="img/first.jpg"/>', html)
        self.assertIn('<div class="mask"><div class="caption">Second<br>Details</div>', html)
        self.assertLess(html.index('href="./first/"'), html.index('href="./second/"'))
        self.assertIn('</div><p>After</p>', html)
        self.assertNotIn('HTML_TILE_', html)
        self.assertNotIn('<ul>', html)

    def test_multiple_blocks_blank_lines_and_four_space_children(self):
        html = self.render(
            'HTML_TILE_BEGIN\n\n- First\n    - ./first/\n    - first.jpg\n\nHTML_TILE_END\n'
            '## Archive\nHTML_TILE_BEGIN\n- Second\n  - ./second/\n  - second.jpg\nHTML_TILE_END\n'
        )
        self.assertEqual(html.count('<div class="eye_catch">'), 2)
        self.assertEqual(html.count('style="text-align:center; line-height:0;"'), 2)
        self.assertIn('<h2 id="Archive">Archive</h2>', html)

    def test_inline_formatting_and_png_image_conversion(self):
        html = self.render(
            'HTML_TILE_BEGIN\n- **Title**<br>Subtitle\n'
            '  - ./page.png/\n  - img/picture.png\nHTML_TILE_END\n'
        )
        self.assertIn('<div class="caption"><b>Title</b><br>Subtitle</div>', html)
        self.assertIn('<a href="./page.png/">', html)
        self.assertIn('<img class="img" src="img/picture.jpg"/>', html)

    def test_paths_are_escaped_as_html_attributes(self):
        html = self.render(
            'HTML_TILE_BEGIN\n- Title\n  - https://example.com/?a=1&b="two"\n'
            '  - img/picture "one".jpg\nHTML_TILE_END\n'
        )
        self.assertIn('href="https://example.com/?a=1&amp;b=&quot;two&quot;"', html)
        self.assertIn('src="img/picture &quot;one&quot;.jpg"', html)

    def test_lists_and_tables_can_touch_tile_blocks(self):
        for before in ('- Before\n', '| A | B |\n| --- | --- |\n| C | D |\n'):
            with self.subTest(before=before):
                html = self.render(
                    before + 'HTML_TILE_BEGIN\n- Tile\n  - ./tile/\n  - tile.jpg\n'
                    'HTML_TILE_END\n- After\n'
                )
                self.assertEqual(html.count('<div class="eye_catch">'), 1)
                self.assertIn('</div><ul>\n<li>After</li>', html)
                if before.startswith('-'):
                    self.assertIn('</ul><div style="text-align:center;', html)
                else:
                    self.assertIn('</table></div><div style="text-align:center;', html)

    def test_markers_inside_code_fences_or_raw_html_are_ignored(self):
        block = 'HTML_TILE_BEGIN\n- Tile\n  - ./tile/\n  - tile.jpg\nHTML_TILE_END\n'
        for before, after in (('```markdown\n', '```\n'), ('~~~\n', '~~~\n'), ('<script>\n', '</script>\n')):
            with self.subTest(before=before):
                html = self.render(before + block + after)
                self.assertNotIn('class="eye_catch"', html)
                self.assertIn('HTML_TILE_BEGIN', html)
                self.assertIn('HTML_TILE_END', html)

    def test_empty_block(self):
        html = self.render('HTML_TILE_BEGIN\nHTML_TILE_END\n')
        self.assertNotIn('HTML_TILE_', html)
        self.assertNotIn('class="eye_catch"', html)

    def test_invalid_blocks_fail_with_file_and_line(self):
        cases = (
            ('HTML_TILE_BEGIN\n- Title\n  - ./page/\n  - image.jpg\n', 1, 'no matching HTML_TILE_END'),
            ('HTML_TILE_END\n', 1, 'no matching HTML_TILE_BEGIN'),
            ('HTML_TILE_BEGIN\nHTML_TILE_BEGIN\nHTML_TILE_END\n', 2, 'Nested'),
            ('HTML_TILE_BEGIN\n  - ./page/\nHTML_TILE_END\n', 2, 'title first'),
            ('HTML_TILE_BEGIN\n- Title\n  - ./page/\nHTML_TILE_END\n', 2, 'title, href, and image'),
            ('HTML_TILE_BEGIN\n- Title\n  - ./page/\n  - image.jpg\n  - extra\nHTML_TILE_END\n', 5, 'exactly two child'),
            ('HTML_TILE_BEGIN\n- Title\n - ./page/\n  - image.jpg\nHTML_TILE_END\n', 3, 'indent'),
            ('HTML_TILE_BEGIN\nTitle\nHTML_TILE_END\n', 2, 'Expected'),
            ('HTML_TILE_BEGIN\n- Title\n  -   \n  - image.jpg\nHTML_TILE_END\n', 3, 'must not be empty'),
        )
        for markdown, line, message in cases:
            with self.subTest(markdown=markdown):
                process, html = self.run_generator(markdown)
                self.assertNotEqual(process.returncode, 0)
                self.assertIsNone(html)
                self.assertIn('ja/index.md:' + str(line) + ':', process.stderr)
                self.assertIn(message, process.stderr)


if __name__ == '__main__':
    unittest.main()
