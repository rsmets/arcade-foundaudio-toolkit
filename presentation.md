# Arcade Toolkit Presentation

## <<<<<<< Updated upstream

- [Design](README.md#design-principles)
- [Tools]
- ***

## Everything is markdown

=======
Goal:

- [Design](README.md#design-principles)
- [Tools]
- ***

## Everything is markdown

> > > > > > > Stashed changes
> > > > > > > In fact, this entire presentation is a markdown file.

---

## Everything happens in your terminal

<<<<<<< Updated upstream

=======

> > > > > > > Stashed changes
> > > > > > > Create slides and present them without ever leaving your terminal.

---

## Code execution

<<<<<<< Updated upstream

=======

> > > > > > > Stashed changes

```go
package main

import "fmt"

func main() {
  fmt.Println("Execute code directly inside the slides")
}
```

You can execute code inside your slides by pressing `<C-e>`,
the output of your command will be displayed at the end of the current slide.

---

## Pre-process slides

<<<<<<< Updated upstream
You can add a code block with three tildes (`~`) and write a command to run _before_ displaying
=======
You can add a code block with three tildes (`~`) and write a command to run _before_ displaying

> > > > > > > Stashed changes
> > > > > > > the slides, the text inside the code block will be passed as `stdin` to the command
> > > > > > > and the code block will be replaced with the `stdout` of the command.

```
~~~graph-easy --as=boxart
[ A ] - to -> [ B ]
~~~
```

The above will be pre-processed to look like:

<<<<<<< Updated upstream
┌───┐ to ┌───┐
│ A │ ────> │ B │
└───┘ └───┘
=======
┌───┐ to ┌───┐
│ A │ ────> │ B │
└───┘ └───┘

> > > > > > > Stashed changes

For security reasons, you must pass a file that has execution permissions
for the slides to be pre-processed. You can use `chmod` to add these permissions.

```bash
chmod +x file.md
```
