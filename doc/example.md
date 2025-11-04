# Markdown Formatting Examples

This document demonstrates various markdown formatting options.

## Headers

# H1 Header

## H2 Header

### H3 Header

#### H4 Header

##### H5 Header

###### H6 Header

---

## Text Formatting

**Bold text** or **bold text**

*Italic text* or *italic text*

***Bold and italic*** or ***bold and italic***

~~Strikethrough text~~

`Inline code`

> Blockquote
>
> Multiple lines in blockquote

---

## Lists

### Unordered Lists

- Item 1
- Item 2
  - Nested item 2.1
  - Nested item 2.2
    - Deeply nested item
- Item 3

- Alternative bullet
- Another item

### Ordered Lists

1. First item
2. Second item
   1. Nested numbered item
   2. Another nested item
3. Third item

### Task Lists

- [x] Completed task
- [ ] Incomplete task
- [ ] Another incomplete task

---

## Links and Images

[Link text](https://www.example.com)

[Link with title](https://www.example.com "Hover text")

[Reference-style link][reference]

[reference]: https://www.example.com "Reference link"

![Alt text for image](https://via.placeholder.com/150)

![Image with title](https://via.placeholder.com/150 "Image title")

---

## Code Blocks

### Inline Code

Use `var x = 10;` for inline code.

### Fenced Code Blocks

```javascript
function greet(name) {
  console.log(`Hello, ${name}!`);
}

greet("World");
```

```python
def greet(name):
    print(f"Hello, {name}!")

greet("World")
```

```bash
# Shell commands
git status
git commit -m "Initial commit"
git push origin main
```

---

## Tables

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Row 1, Col 1 | Row 1, Col 2 | Row 1, Col 3 |
| Row 2, Col 1 | Row 2, Col 2 | Row 2, Col 3 |
| Row 3, Col 1 | Row 3, Col 2 | Row 3, Col 3 |

### Aligned Tables

| Left-aligned | Center-aligned | Right-aligned |
|:-------------|:--------------:|--------------:|
| Left | Center | Right |
| Text | Text | Text |

---

## Horizontal Rules

Three or more hyphens, asterisks, or underscores:

---

***

___

---

## Nested Elements

1. First ordered item
   - Unordered sub-item
   - Another sub-item

     ```python
     # Code in nested list
     print("Hello")
     ```

2. Second ordered item
   > Blockquote in list
   >
   > Second line

---

## Escaping Characters

Use backslash to escape special characters:

\* Not a bullet
\# Not a header
\[Not a link\]

---

## HTML in Markdown

You can also use HTML:

<details>
<summary>Click to expand</summary>

Hidden content here!

- Item 1
- Item 2

</details>

<br>

<div align="center">
  <strong>Centered text using HTML</strong>
</div>

---

## Footnotes

Here's a sentence with a footnote.[^1]

Another reference to footnote.[^2]

[^1]: This is the first footnote.
[^2]: This is the second footnote with more details.

---

## Emoji

:smile: :rocket: :tada: :+1:

Or use Unicode directly: 😀 🚀 🎉 👍

---

## Mathematical Expressions (if supported)

Inline math: $E = mc^2$

Block math:

$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

---

## Definition Lists (extended markdown)

Term 1
: Definition 1

Term 2
: Definition 2a
: Definition 2b

---

## Abbreviations (if supported)

The HTML specification is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium

---

## Highlights (if supported)

==Highlighted text== (not supported in all markdown flavors)

---

## Subscript and Superscript (if supported)

H~2~O (subscript)

X^2^ (superscript)

---

## Best Practices

1. **Use headers hierarchically** - Don't skip levels
2. **Add blank lines** - Between different elements for readability
3. **Be consistent** - Choose one style for bullets, emphasis, etc.
4. **Preview your markdown** - Different renderers may have slight variations
5. **Use code blocks for code** - With appropriate language syntax highlighting

---

## Common Use Cases

### Documentation

- README files
- API documentation
- Project wikis
- User guides

### Academic Writing

- Research notes
- Literature reviews
- Lab reports (with proper extensions)

### Web Content

- Blog posts
- Static site generators (Jekyll, Hugo, etc.)
- GitHub Pages

---

**Last Updated:** November 4, 2025
