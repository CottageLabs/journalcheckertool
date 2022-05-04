---
title: "Widget example"
date: 2021-02-14T04:44:50Z
description: "Page demonstrating how to embed the Journal Checker Tool: Plan S Compliance Validator widget."
type: "blank"
---

This is a page which shows an example of the Journal Checker Widget

It is installed and configured using the settings shown below.

```code
<script>
    window.jct_query_options = {
        journal: "1477-9129",
        funder: "wellcome",
        not_he: true
    }
    jct.setup_plugin();
</script>
```

For full documentation on the widget please see the [widget](/widget) page
