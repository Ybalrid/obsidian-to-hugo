import unittest
from obsidian_to_hugo import wiki_links_processor


class WikiLinksProcessorTestCase(unittest.TestCase):
    def test_get_wiki_links(self):
        text = "[[foo]] [[bar|baz]]"
        links = wiki_links_processor.get_wiki_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(
            links[0],
            {
                "wiki_link": "[[foo]]",
                "link": "foo",
                "text": "foo",
            },
        )
        self.assertEqual(
            links[1],
            {
                "wiki_link": "[[bar|baz]]",
                "link": "bar",
                "text": "baz",
            },
        )

    def test_convert_wiki_link(self):
        wiki_link = wiki_links_processor.get_wiki_links("[[foo]]")[0]
        hugo_link = wiki_links_processor.wiki_link_to_hugo_link(wiki_link)
        self.assertEqual(hugo_link, '[foo]({{< ref "foo" >}})')

    def test_convert_wiki_link_with_text(self):
        wiki_link = wiki_links_processor.get_wiki_links("[[bar|baz]]")[0]
        hugo_link = wiki_links_processor.wiki_link_to_hugo_link(wiki_link)
        self.assertEqual(hugo_link, '[baz]({{< ref "bar" >}})')

    def test_convert_wiki_link_with_text_and_backslash(self):
        wiki_link = wiki_links_processor.get_wiki_links("[[bar\\|baz]]")[0]
        hugo_link = wiki_links_processor.wiki_link_to_hugo_link(wiki_link)
        self.assertEqual(hugo_link, '[baz]({{< ref "bar" >}})')

    def test_convert_wiki_link_with_index(self):
        wiki_link = wiki_links_processor.get_wiki_links("[[bar/_index|baz]]")[0]
        hugo_link = wiki_links_processor.wiki_link_to_hugo_link(wiki_link)
        self.assertEqual(hugo_link, '[baz]({{< ref "bar/" >}})')

    def test_convert_wiki_link_with_heading(self):
        wiki_link = wiki_links_processor.get_wiki_links("[[bar#Foo Bar|baz]]")[0]
        hugo_link = wiki_links_processor.wiki_link_to_hugo_link(wiki_link)
        self.assertEqual(hugo_link, '[baz]({{< ref "bar#foo-bar" >}})')

    def test_replace_wiki_links(self):
        real_in = """
        [[foo]]
        [[bar|baz]]
        [[bar\\|baz]]
        [[bar/_index|baz]]
        [[bar#Foo Bar|baz]]
        """
        expected_out = """
        [foo]({{< ref "foo" >}})
        [baz]({{< ref "bar" >}})
        [baz]({{< ref "bar" >}})
        [baz]({{< ref "bar/" >}})
        [baz]({{< ref "bar#foo-bar" >}})
        """
        real_out = wiki_links_processor.replace_wiki_links(real_in)
        self.assertEqual(real_out, expected_out)

    def test_convert_image_wiki_link_uses_parent_relative_path_for_root_images(self):
        wiki_link = wiki_links_processor.get_wiki_links("![[ektachrome original.jpg]]")[0]
        hugo_link = wiki_links_processor.wiki_link_to_hugo_link(wiki_link)
        self.assertEqual(hugo_link, '{{< figure src="../ektachrome original.jpg"  >}}')

    def test_convert_image_wiki_link_keeps_nested_paths(self):
        wiki_link = wiki_links_processor.get_wiki_links("![[images/ektachrome original.jpg]]")[0]
        hugo_link = wiki_links_processor.wiki_link_to_hugo_link(wiki_link)
        self.assertEqual(hugo_link, '{{< figure src="images/ektachrome original.jpg"  >}}')

    def test_convert_image_wiki_link_with_caption(self):
        wiki_link = wiki_links_processor.get_wiki_links("![[ektachrome original.jpg|Original]]")[0]
        hugo_link = wiki_links_processor.wiki_link_to_hugo_link(wiki_link)
        self.assertEqual(
            hugo_link,
            '{{< figure src="../ektachrome original.jpg" caption="Original" >}}',
        )


if __name__ == "__main__":
    unittest.main()
