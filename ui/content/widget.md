---
title: "Widget"
date: 2021-02-13T23:43:29Z
description: "Documentation of the public widget for the Journal Checker Tool: Plan S Compliance Validator."
---

# Journal Checker Widget

The Journal Checker Widget allows you to embed the Journal Checker Tool's full functionality on your site. It also 
allows you to pre-select any of the values for the user: the ISSN for a journal, the funder, or the ROR for the institution.

To embed the widget on your web page, copy and paste the code below into the web page where you want the widget to be displayed,
and then customise it according to the documentation below.

```code
<head>
    <script type="text/javascript" src="https://journalcheckertool.org/js/jct_plugin.js"></script>
    <link href="https://journalcheckertool.org/css/plugin.css" rel='stylesheet' type='text/css'>
</head>
<body>
    <div id="jct_plugin"></div>
    <script>
        window.jct_query_options = {
            journal: "[issn_of_the_journal]",
            funder: "[funder_id]",
            institution: "[ror_of_the_institution]",
            not_he: false, // true or false
        }
        jct.setup_plugin();
    </script>
</body>
```

You can see a live demonstration of the widget [here](/widget-example).

## Considerations for embedding

The Journal Checker Widget provides a similar experience for the user as the main Journal Checker Tool.  It is presented
as a "sidebar", suitable for embed in a narrow enclosure (300px by default) on your site. This is similar in presentation
to the mobile view of the main Journal Checker Tool.  It will take up a reasonable amount of vertical space, and that
space will vary depending on exactly what results the user gets from their query.

The widget will give the user the 3 standard input boxes (with autosuggests for values), and then the usual summary
of compliance options followed by a link to the main JCT page for full details on their results.

See the [live demonstration of the widget](/widget-example) to see a reference example.

## Configuring the widget

The widget can be configured to pre-fill the user input boxes with values dictated by the embedder.  Any number of the
input boxes can be pre-filled.

The parameter `window.jct_query_options` takes a set of default values for the plugin to offer to the user. 
All of the parameters are optional, and you do not need to include them if you do not want any default values.

***journal***    
This parameter should be a valid journal ISSN.
Setting it will pre-fill the "Journal" input box on the widget.
A user will also be able select other journals from the "Journal" box.

For example, providing the following configuration will pre-fill "Nature": 

```code
window.jct_query_options.journal = "1476-4687"
```

***funder***    
This parameter expects the JCT Funder ID.
Setting it will pre-fill the "My Funder" input box on the widget.
A user will also be able to select other funders from the "My Funder" box.

See the [list of Funder IDs](/funder-ids) for a full list of your available options.

For example, if you wish to pre-fill the "My Funder" input box with the "Academy of Finland (AKA)"
then you should provide: 

```code
window.jct_query_options.funder = "academyoffinlandaka"
```

***institution***    
This parameter expects the [ROR](https://ror.org) of the institution.
Setting it will pre-fill the "My Institution" input box.
A user will also be able to select other institutions from the "My Institution" box or select _No affiliation_.

If you do not know the ROR of the organisation that you wish to pre-fill, you can find it by searching in
the [ROR Registry](https://ror.org/) and taking the alphanumerical ID of the organisation (like `041kmwe10`).
For example, this will pre-fill "Imperial College London": 

```code
window.jct_query_options.institution = "041kmwe10"  
```
Do **not** include the `https://ror.org/` part of the ROR ID.

***not_he***    
This parameter can be set to either `true` or `false` and is used if you want to run the compliance check with no 
institution pre-filled. Instead the "Not affiliated" checkbox will be selected.
If set to `true`, it will override any institution value you have set.
A user will also be able to uncheck this box and select other institutions from the "My Institution" box.

```code
window.jct_query_options.no_he = true
```

## Customising the styles

The styles for the widget are provided by the [plugin.css](https://journalcheckertool.org/css/plugin.css) file,
and you may customise or override the styles here as you need.

The main styles you may wish to override are the width and font-size of the widget, which can be done with the following
properties:

```
#jct_plugin {
    width: 300px;
    font-size: 12px;
}
```
