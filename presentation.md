# Arcade Toolkit Presentation

Agenda

- Frame my decision-making
- Showcase tooling leveraged
- Present implementation
- Demo
- Toolkit development feedback

---

``

## README

The README.md has most of the important details I want to touch on. Let's go there.

---

## Implementation

`get_audio_list`

Tool

- intent-based implementation
- use of context for secret management
- graceful error handling with RetryableToolError

Evals

- fairly extensive scenarios of how one would interface with the tool

Tests

- unit tests to cover sanity checks

---

## Demo

I will show off the agent app in a moment, but first, here is just the toolkit in action:
https://api.arcade.dev/dashboard/playground/chat

---

## Toolkit development feedback

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

You can add a code block with three tildes (`~`) and write a command to run _before_ displaying
the slides, the text inside the code block will be passed as `stdin` to the command
and the code block will be replaced with the `stdout` of the command.

```
~~~graph-easy --as=boxart
[ A ] - to -> [ B ]
~~~
```

The above will be pre-processed to look like:

┌───┐ to ┌───┐
│ A │ ────> │ B │
└───┘ └───┘

For security reasons, you must pass a file that has execution permissions
for the slides to be pre-processed. You can use `chmod` to add these permissions.

```bash
chmod +x file.md
```
