# Modals Display Logic

## Rendering a modal

All modals are created from language files, so they adhere to a simple standard form:

```
[title]
[body]
```

To render a specific modal, the following language codes can be used

```
modals.[modal_id].title
modals.[modal_id].body
```

## Triggering a modal

Links may contain the `class=modal-trigger` attribute.  They must also contain a `data-modal="[modal_id]"`
attribute.

Bind an event such that whenever any link of class `modal-trigger` is triggered then a generic modal
is displayed and populated with the text from the language files for that `modal_id`.