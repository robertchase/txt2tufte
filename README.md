# markdown-ish to tufte.css

[tufte.css](https://edwardtufte.github.io/tufte-css/) lets you mark up your `HTML` so that it has
the feel of one of [Edward Tufte's](https://en.wikipedia.org/wiki/Edward_Tufte)
books. I wanted to use this styling to create articles for publication
on a website and I *didn't* want to manage a bunch of hand-edited `HTML`.
I stole a page from [markdown](https://www.markdownguide.org/) and created
my own markdown-like text file that compiles to tufte-capable `HTML`.

Since this is for a website, I needed a way to generate an `index.html`
that was stylistically compatible&mdash;so i made a compiler for that too.

## Article File

An `Article` is a text file of this format:

```
   Title of Article
   Description (short description used in the index.html)
   Author (turned into a link back to index.html)
   Date

   # First Section Title

   ...section contents

   # Next Section Title ...
```

An `article` file can be converted into `HTML` by running this script:

`python3 -m txt2tufte.tufte < my-article.txt > my-article.html`

## Index File

An `Index` file is a text file of this format:

```
Index Title (for example "Deep Thoughts")
Subtitle

first-article.txt
second-article.txt
...
```

An `index` file can be converted into `HTML` by running this script:

`python3 -m txt2tufte.index < index.txt > index.html`

### how building the index file works

**Note:** The `index.txt` file only generates links to articles that
are *explicitly called out*. In other words: The compiled index
file will not automatically point to *all* the articles&mdash;just the
ones you specify, and in just the order you specify.

The lines containing (for example) `first-article.txt`
tell `index.py` to look for a text file
named `src/{first-article.txt}` (the value of `src` can be changed by
setting the `INDEX_SRC` environment variable).
The text file is opened and the `title` (first line) and
`description` (second line)
of the article
are extracted.

The expected layout is something like this:

```
├── site
│   ├── about.html
│   ├── colophon.html
│   ├── css
│   │   ├── tufte.css
│   │   ├── tufte-nav.css
│   │   ├── tufte-index.css
│   ├── an-article.html
│   ├── another-article.html
│   ├── et-book
│   │   ├──  ...
│   ├── index.html
│   ├── media
│   │   ├── pic-1.png
│   │   ├── pic-2.png
│   │   ├── ...
└── src
    ├── about.txt
    ├── colophon.txt
    ├── an-article.txt
    ├── another-article.txt
    └── index.txt
```

Note that all of the `.html` files are ephemeral.

### Building all the things with `make`

I use a `Makefile` with this code to automatically derive `html` targets:

```
SRCDIR := src
TGTDIR := site

# derive targets ({site}/*.html) from source ({src}/*.txt)
SRC := $(wildcard $(SRCDIR)/*.txt)
TGT := $(notdir $(SRC))
TGT := $(basename $(TGT))
TGT := $(addprefix $(TGTDIR)/,$(TGT))
TGT := $(addsuffix .html,$(TGT))
```

and build things with something like this (assumes `PYTHONPATH` is set):

```
all: $(TGT)

$(TGTDIR)/%.html : $(SRCDIR)/%.txt
	python3 -m txt2tufte.tufte < $< > $@

$(TGTDIR)/index.html : $(SRCDIR)/index.txt
	INDEX_SRC=$(SRCDIR) python3 -m txt2tufte.index < $< > $@
```

I have other `make` targets that help with pushing things
to an `S3` bucket and invalidating `cloudfront` assets&mdash;but
you can do whatever makes sense for your deployment.

## basic markup

### new section

`# optional section title`

### em dash
works with or without a space between the text and the double dash.

`text -- text` &rarr; text&mdash;text

### code

`` `text` `` &rarr; `text`

### bold
`**text**` &rarr; **text**

**Note:** To include an asterisk in the text, escape it with a backslash (\\).

### italic
`*test*` &rarr; *text*

**Note:** To include an asterisk in the text, escape it with a backslash (\\).

### link
`[visible text](url)`

**Note:** To include a parenthesis in the `url`, escape it with a backslash (\\).
To include a square bracket in the `visible text`, escape it with a backslash (\\).

### horizontal rule
On a line by itself:

`---`

### copyright
On a line by itself:

`@ 1923 Roaring Twenties` &rarr; Copyright &copy; 1923 Roaring Twenties


### uppercase start to paragraph (so-called newthought)
```

+ It was the best
of times...
```

becomes:

`IT WAS THE BEST of times...`

### return arrow
Add a return arrow that navigates to the index.

`<=`

## multi-line markup

### numbered margin footnote (sidenote)

```
^ text to which footnote is added
footnote
more footnote
^
```

### margin note
```
>
note
more note
>
```

### image with margin note
```
{ image-url
margin note
more margin note
{
```

### margin image with added note
```
} image-url
note
more note
}
```

### blockquote
Creates an indented quote in the main column.

```
% quote attribution
quote
more quote
%
```
