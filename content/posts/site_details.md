Title: How I Built This Site
Date: 2024-07-07 19:20
Tags: projects, meta
Slug: site-details
Author: Kaleb Crans
Summary: Github Pages + Pelican Static Site Generator + Custom HTML/CSS/Javascript = this site
Subtitle: A tepid dive into webdev

My intention with this website is to have an online place where I can post my portfolio, resume, blog, etc… I also want to experiment with web development, so I went with a simple setup hosted on Github Pages where I can mess around with css and javascript to my heart’s content. The client should be able to handle everything for my purposes, so a static site will work fine (and cost me nothing!). You can find the source for the site in [this](https://github.com/kcrans/kcrans.github.io) repo. Here are some notes on how exactly I’ve set everything up.

## Static Site Generator
I messed around with Jekyll, the standard static site generator for Github Pages, but I didn’t find it compelling. Site theming was unintuitive and I didn’t like the hassle of dealing with Ruby package management when I’m not using Ruby for anything else. Instead, I searched around and found [Pelican](https://getpelican.com), which is a static site generator written in Python. I already know Python, so I found the configuration syntax intuitive and package management is a breeze[!s I mean the Python packaging ecosystem is a mess, but it's a mess I’m used to dealing with ].

## Styling and CSS
I'm a fan of Edward Tufte's work on design. His books are typeset beautifully and are a great example of the combination of textual exposition plus quantitative richness I want for this blog. Of course, you don’t want to go down the cargo cult route of blindly copying the style in his books wholesale. So my solution was to use [tufte-css](https://edwardtufte.github.io/tufte-css/), which is a fairly straightforward port of histstyle to html documents, and then modify it as I see fit. What I’ve done so far is add extra styling for website features such as navigation bars and article directories, remove the dark mode [!s It clashed with my homepage styling and I didn’t like the default look anyways. I’ll probably implement my own dark mode at some future date. ], and add more color to give my website a consistent theme.

## Markdown
Making posts using Markdown as a markup language is a very convenient and intuitive workflow. The problem is tufte-css uses css classes and html tags that do not mesh well with the default markdown interpreter. The good thing is python markdown is very extensible, so I was able to create an extension that parses markdown documents in a more fitting way and adds support for things like sidenotes and endnotes.
```
def square(num: int) -> int:
    return num * num
```

## Deployment
Deployment on Github Pages with Pelican is just as easy as setting up a Github action like this [one](https://docs.getpelican.com/en/latest/tips.html#publishing-to-github-pages-using-a-custom-github-actions-workflow).

