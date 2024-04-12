from markdown.extensions import Extension
from markdown.inlinepatterns import LinkInlineProcessor, IMAGE_REFERENCE_RE
import xml.etree.ElementTree as etree
import re

class ImageInsideFigureProcessor(LinkInlineProcessor):
    """
    Given an image definition in Markdown, return an 'img' html element
    nested within a 'figure' element.
    """

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | None, int | None, int | None]:
        """
        Takes in a regex match for the begining of an image link (i.e. ![).
        Returns a tuple of Nones if anything does not work. Otherwise
        returns an img element contained in a figure with the begining of
        the regex match and the index of the link.
        """
        alt_text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        src, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        figure = etree.Element('figure')
        img = etree.SubElement(figure, 'img')
        
        img.set('src', src)
        img.set('alt', self.unescape(alt_text))

        if title is not None:
            img.set('title', title)
            figcaption = etree.SubElement(figure, 'figcaption')
            figcaption.text = title

        return figure, m.start(0), index

class TufteExtension(Extension):
    def extendMarkdown(self, md):
        # IMAGE_REFERENCE_RE = r'\!\['
        img_processor = ImageInsideFigureProcessor(IMAGE_REFERENCE_RE, md)
        md.inlinePatterns.register(img_processor, 'img_inside_figure', 155)

# Tests

def makeHtml(text):
    from markdown import markdown
    return markdown(text, extensions=[TufteExtension()])

# Example usage
md_text = '![An image](http://example.com/image.png "Image Title")'
html = makeHtml(md_text)
#print(html)

with open("test.md", "r") as f:
    other_text = f.read()
    html = makeHtml(other_text)
    print(html)
