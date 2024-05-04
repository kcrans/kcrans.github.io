from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.blockprocessors import BlockProcessor
from markdown.treeprocessors import Treeprocessor
from markdown.inlinepatterns import InlineProcessor, LinkInlineProcessor, IMAGE_REFERENCE_RE
import xml.etree.ElementTree as etree
import re
from copy import deepcopy

meta_identifer = "vE+8*J(Y,gHM&U0Q?v-h4x%/9id4*.utSvt%,DQh4S#)tf#0)L"

class SectionProcessor(BlockProcessor):
    # Parses blocks of text which start with a title/header
    # and puts the text into "section" elements.

    RE = re.compile(r'(?:^|\n)(#{2})(?P<header>(?:\\.|[^\\])*?)#*(?:\n|$)')
    def test(self, parent: etree.Element, block: str) -> bool:
        test = re.compile(IMAGE_REFERENCE_RE)
#        if test.search(block):
#            print(block)
        return bool(self.RE.search(block))

    def run(self, parent: etree.Element, blocks: list[str]) -> None:
#        print(blocks[0])
        header_block = blocks.pop(0)
        match = self.RE.search(header_block)
        if match:
            section = etree.SubElement(parent, 'section')
            h2 = etree.SubElement(section, 'h2')
            h2.text = match.group('header').strip()
            
            before = header_block[:match.start()]  # All lines before header
            after = header_block[match.end():]     # All lines after header
            if before:
                # As the header was not the first line of the block and the
                # lines before the header must be parsed first,
                # recursively parse this lines as a block.
                self.parser.parseBlocks(parent, [before])
            
            # *** Experimental ***
            for block_num, block in enumerate(blocks):
                if re.search(self.RE, block):
                    self.parser.parseBlocks(section, blocks[:block_num])
                    for i in range(block_num):
                        blocks.pop(0)
                    break
            # We didn't find another header, so from this header to EOF we will be one section
            else:
                self.parser.parseBlocks(section, blocks)
                blocks = []

            if after:
                # Insert remaining lines as first block for future parsing.
                if self.parser.state.isstate('looselist'):
                    # parsing, the line(s) after need to be detabbed. See #1443.
                    after = self.looseDetab(after)
                blocks.insert(0, after)
        else:  # pragma: no cover
            # This should never happen, but just in case...
            logger.warn("We've got a problem header: %r" % header_block)

class ImageBlockProcessor(BlockProcessor):
    """ 
    Does two things:
        1. finds images within blocks and breaks them out
        2. wraps all images in <figure> tags
    
    Also, as long as this processor has a higher priority than
    the built-in 'ParagraphProcessor', images will not be
    inclosed in <p> tags which is what tufte-css expects.
    """
    RE = re.compile(r'!\[[^]]*\]\([^)]+\)')

    def test(self, parent: etree.Element, block: str) -> bool:
        return bool(self.RE.search(block))

    def run(self, parent: etree.Element, blocks: list[str]) -> None:
        image_block = blocks.pop(0)
        match = self.RE.search(image_block)

        before = image_block[:match.start()]  # All lines before header
        after = image_block[match.end():]     # All lines after header
        
        if before:
                # As the header was not the first line of the block and the
                # lines before the header must be parsed first,
                # recursively parse this lines as a block.
                self.parser.parseBlocks(parent, [before])
        figure = etree.SubElement(parent, "figure")
        figure.text = match.group(0).strip()

        if after:
            # Insert remaining lines as first block for future parsing.
                if self.parser.state.isstate('looselist'):
                    # parsing, the line(s) after need to be detabbed. See #1443.
                    after = self.looseDetab(after)
                blocks.insert(0, after)

class FirstSectionProcessor(Treeprocessor):
    """ Build and append footnote div to end of document. """

    def run(self, root: etree.Element) -> None:
        tree_list = list(root)
        end_of_intro = len(tree_list)
#        print('----')
#        for element in root.iter():
#            print(element.tag)
#        print('____')
       # print(tree_list)
        if tree_list[0].text == meta_identifier:
            root.remove(tree_list[0])
            return
        for index, top_lvl_element in enumerate(tree_list):
            #print(top_lvl_element.tag)
            if top_lvl_element.tag == 'section':
                #print(index, '---------------------------------')
                end_of_intro = index + 1
                break
        first_section = etree.Element('section')
        root.insert(0, first_section)
        
        for index in range(0, end_of_intro):
            current_el = tree_list[index]
            first_section.append(deepcopy(current_el))
            root.remove(current_el)

        #print(list(root))
#        for element in root.iter():
            #print(element.tag)

# Depreciated Processor:
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

class SidenoteProcessor(InlineProcessor):
    sidenote_index = 0

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | None, int | None, int | None]:
        side_text = m.group(1)
        note_id = str(SidenoteProcessor.sidenote_index)
        SidenoteProcessor.sidenote_index += 1

        container = etree.Element('span')
        
        label = etree.SubElement(container, 'label')
        label.set('for', note_id)
        label.set('class', 'margin-toggle sidenote-number')
        
        input_el = etree.SubElement(container, 'input')
        input_el.set('type', 'checkbox')
        input_el.set('id', note_id)
        input_el.set('class', 'margin-toggle')
        
        sidenote = etree.SubElement(container, 'span')
        sidenote.set('class', 'sidenote')
        sidenote.text = side_text

        return container, m.start(0), m.end(0)

class MarginNoteProcessor(InlineProcessor):
    margin_note_index = 0

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | None, int | None, int | None]:
        margin_text = m.group(1)
        note_id = str(MarginNoteProcessor.margin_note_index)
        MarginNoteProcessor.margin_note_index += 1

        container = etree.Element('span')
        
        label = etree.SubElement(container, 'label')
        label.set('for', note_id)
        label.set('class', 'margin-toggle')
        
        input_el = etree.SubElement(container, 'input')
        input_el.set('type', 'checkbox')
        input_el.set('id', note_id)
        input_el.set('class', 'margin-toggle')
        
        margin_note = etree.SubElement(container, 'span')
        margin_note.set('class', 'marginnote')
        margin_note.text = margin_text

        return container, m.start(0), m.end(0)

# Matches a line of metadata, EX:
#   Some_Meta-data:     woah this is cool metadata
META_RE = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)')
# Matches metadata start signifiers, EX:
# ---          
BEGIN_RE = re.compile(r'^-{3}(\s.*)?')


class MetadataTestPreprocessor(Preprocessor):
    """
    Checks to see if there is any metadata in the given Markdowm document.
    If there is, then it's an article and the process proceeds normally.
    If not, then this must be a Markdown process run on a formatted piece of metadata
    already taken from an article (like "summary" for instance).
    """
    def run(self, lines: list[str]) -> list[str]:
        if lines:
            if BEGIN_RE.match(lines[0]) or META_RE.match(lines[0]):
                # Change nothing, continue processing document
                return lines
            else:
                blank_line = ""
                lines.insert(0, blank_line)
                line = meta_identifier
                lines.insert(0, line)
        return lines

class TufteExtension(Extension):
    def extendMarkdown(self, md):
        # IMAGE_REFERENCE_RE = r'\!\['
        RE_SIDENOTE = r'\[\^s\s(.*?)\]' # Example: [^s This is a sidenote!]
        RE_MARGIN_NOTE = r'\[\^m\s(.*?)\]' # Example: [^m This is a margin note!]

        metadata_test_processor = MetadataTestPreprocessor(md)

        section_processor = SectionProcessor(md.parser)
        img_block_processor = ImageBlockProcessor(md.parser)
        first_section_processor = FirstSectionProcessor(md)
        sidenote_processor = SidenoteProcessor(RE_SIDENOTE, md)
        margin_note_processor = MarginNoteProcessor(RE_MARGIN_NOTE, md)
#        img_processor = ImageInsideFigureProcessor(IMAGE_REFERENCE_RE, md)
        md.preprocessors.register(metadata_test_processor, 'test', 28)

        md.parser.blockprocessors.register(section_processor, "wrap_subheaders_in_sections", 175)
        md.parser.blockprocessors.register(img_block_processor, "prevent_paragraphs_containing_imgs", 11)
        md.treeprocessors.register(first_section_processor, "creates_first_section_under_h1", 50)
        md.inlinePatterns.register(sidenote_processor, 'sidenotes', 40)
        md.inlinePatterns.register(margin_note_processor, 'margin_notes', 40)
#        md.inlinePatterns.register(img_processor, 'img_inside_figure', 155)

# Tests
if __name__ == "__main__":
    def makeHtml(text):
        from markdown import markdown
        return markdown(text, extensions=[TufteExtension()])
    # Example usage
    with open("mm.md", "r") as file:
        md_text = file.read()
    html = makeHtml(md_text)
    print(html)
