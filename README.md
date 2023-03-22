# markdown-ish to tufte.css

Change a basic text file with markup to html that uses [tufte.css](https://edwardtufte.github.io/tufte-css/).

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

**Note:** To include an aserisk in the text, escape it with a backslash (\\).

### italic
`*test*` &rarr; *text*

**Note:** To include an aserisk in the text, escape it with a backslash (\\).

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