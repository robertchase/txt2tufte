# markdown-ish to tufte.css

Change a basic text file with markup to html that uses [tufte.css](https://edwardtufte.github.io/tufte-css/).

## basic markup

### new section

`# optional section title`

### em dash
works with or without a space between the text and the double dash.

`text -- text` -> text&mdash;text

### code

`` `text` `` -> `text`

### bold
`**text**` -> **text**

### italic
`*test*` -> *text*

### link
`[visible text](url)`

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
