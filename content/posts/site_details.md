Title: How I Built This Site
Date: 2024-07-07 19:20
Tags: projects, meta
Slug: site-details
Author: Kaleb Crans
Summary: Github Pages + Pelican + Custom HTML/CSS/Javascript = this site
Subtitle: A tepid dive into webdev

My intention with this website is to have an online place where I can post my portfolio, resume, blog, etc… I also want to experiment with web development, so I went with a simple setup hosted on Github Pages where I can mess around with css and javascript to my heart’s content. At the moment I don't need to do anything that interacts with databases or has complex backend logic, so a static site will work fine (and cost me nothing!). You can find the source for the site in [this](https://github.com/kcrans/kcrans.github.io) repo. Here are some notes on how exactly I’ve set everything up.

## Static Site Generator

I messed around with Jekyll, the standard static site generator for Github Pages, but I didn’t find it compelling. Site theming was unintuitive and I didn’t like the hassle of dealing with Ruby package management when I’m not using Ruby for anything else. Instead, I searched around and found [Pelican](https://getpelican.com), which is a static site generator written in Python. I already know Python, so I found the configuration syntax intuitive and package management is a breeze[^s I mean the Python packaging ecosystem is a mess, but it's a mess I’m used to dealing with ]. You can write arbitrary python within the `pelicanconf.py ` configuration file, which means I could do things like walk through a directory in order to create a python dictionary of all my custom homepage files so that I can control the final file structure of the resulting site.

## Styling and CSS

I'm a fan of Edward Tufte's work on design. His books are typeset beautifully and are a great example of the combination of textual exposition plus quantitative richness I want for this blog. Of course, you don’t want to go down the cargo cult route of blindly copying the style in his books wholesale. So my solution was to use [tufte-css](https://edwardtufte.github.io/tufte-css/), which is a fairly straightforward port of his style to html documents, and then modify it as I see fit. What I’ve done so far is add extra styling for website features such as navigation bars and article directories, remove the dark mode [^s It clashed with my homepage styling and I didn’t like the default look anyways. I’ll probably implement my own dark mode at some future date. ], and add more color to give my website a consistent, unique theme. Speaking of themes, the Pelican theme I’m using is basically just two html templates (one for the blog directory and one for blog posts) and then my custom css files (including one for code highlighting). My homepage is distinct enough that I just created its files directly and have Pelican treat them as static files and move them to the output directory when the rest of the site is generated.

## Markdown

Making posts using Markdown as a markup language is a very convenient and intuitive workflow. The problem is tufte-css uses css classes and html tags that do not mesh well with the default markdown interpreter. I could rewrite the css completely, but that’s tedious and lots of the structure is actually well-designed. The good thing is python markdown is very extensible, so I was able to create an extension that parses markdown documents in a more fitting way and adds support for things like sidenotes and endnotes.

For instance, here is the code[^s The complete code for my markdown extension is in the [tufte_markdown](https://github.com/kcrans/kcrans.github.io/blob/main/tufte_markdown/tufte_markdown.py) directory.] that handles sidenotes:

```
:::python
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
```

During the inline processing phase of interpretation, character sequences that match the regex `\[\^s\s(.*?)\]`[^s i.e. `[^s This is a sidenote ]` ] will be converted into the appropriate html for sidenotes as specified by tufte-css.

## Deployment

Deployment on Github Pages with Pelican is just as easy as setting up a Github action like this [one](https://docs.getpelican.com/en/latest/tips.html#publishing-to-github-pages-using-a-custom-github-actions-workflow). It takes about 45 seconds to deploy with the current configuration I have. Make sure to include markdown as a dependency if you are using it for writing posts like I am. Using this setup, you can deploy to Github Pages with just a simple push to main.


