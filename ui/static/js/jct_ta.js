let jct_ta = {
    api: JCT_API_endpoint,
    latest_full_response: false,
    chosen: {},
    clinputs: {},
    inputsCycle: {
        "journal" : "institution"
    },
};

jct_ta.d = document;
jct_ta.d.gebi = document.getElementById;
jct_ta.d.gebc = document.getElementsByClassName;

jct_ta.inputs_plugin_html = () => {
    return `
    <h2 class="sr-only">Make a query</h2>
    <div class="col col--1of2 expression">
        <div class="expression__input" id="jct_journal-container">
        </div>
<!--        <div class="expression__operator">-->
<!--            <svg width="36" height="36" viewbox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">-->
<!--                <path d="M18.3 3L18.3 33M3 17.7H33" stroke="white" stroke-width="5" stroke-linecap="round"></path>-->
<!--            </svg>-->
<!--        </div>-->
    </div>

    <div class="col col--1of2 expression">
        <div class="expression__input">
            <div id="jct_institution-container">
            </div>
        </div>
<!--        <div class="expression__operator">-->
<!--            <div>-->
<!--                <svg width="70" height="70" viewbox="0 0 70 70" fill="none" xmlns="http://www.w3.org/2000/svg">-->
<!--                    <path fill-rule="evenodd" clip-rule="evenodd" d="M22.5 22C21.1193 22 20 23.1193 20 24.5C20 25.8807 21.1193 27 22.5 27H47.5C48.8807 27 50 25.8807 50 24.5C50 23.1193 48.8807 22 47.5 22H22.5ZM22.5 42C21.1193 42 20 43.1193 20 44.5C20 45.8807 21.1193 47 22.5 47H47.5C48.8807 47 50 45.8807 50 44.5C50 43.1193 48.8807 42 47.5 42H22.5Z" fill="white"></path>-->
<!--                </svg>-->
<!--            </div>-->
<!--        </div>-->
    </div>

    <div class="col col--1of2 suggest" id="jct_suggestjournal">
    </div>
    <div class="col col--1of2 suggest" id="jct_suggestinstitution">
    </div>
    <div class="loading" id="jct_loading" style="display:none">
        <div class="loading__dots">
            <div></div>
            <div></div>
            <div></div>
            <span class="sr-only">Loading TAs…</span>
        </div>
    </div>
`;};

jct_ta.results_plugin_html = ``;

jct_ta.suggest_prepare = (txt, stop_words) => {
    txt = txt.toLowerCase().trim();
    for (let sw of stop_words) {
        let fullThing = new RegExp("^" + sw + "$");
        let atEnd = new RegExp(" " + sw + "$");
        let atStart = new RegExp("^" + sw + " ");
        let inMiddle = new RegExp(" " + sw + " ");

        txt = txt.replace(fullThing, "").replace(atEnd, "").replace(atStart, "").replace(inMiddle, " ");
    }
    while (true) {
        if (!(txt.includes("  "))) {
            break;
        }
        txt.replace("  ", " ");
    }
    return txt;
};

// ----------------------------------------
// function to do api calls
// ----------------------------------------
jct_ta.jx = (route, q, after, api) => {
    let base_url = api ? api : jct_ta.api;
    let url;
    if (route) {
        url = new URL(route, base_url);
    } else {
        url = new URL(base_url);
    }
    if (!q === false) {
        let searchParams = new URLSearchParams(q);
        for (const [key, value] of searchParams.entries()) {url.searchParams.append(key, value);}
    }

    // request the tas
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url.href);
    xhr.send();
    xhr.onload = () => { xhr.status !== 200 ? jct_ta.error(xhr) : (typeof after === 'function' ? after(xhr) : jct_ta.result_loaded(xhr)); };
    xhr.onerror = () => { jct_ta.error(); };
};

jct_ta.error = (xhr) => {
    jct_ta.latest_response = xhr;
};

jct_ta.result_loaded = (xhr) => {
    let js = JSON.parse(xhr.response);
    jct_ta.latest_full_response = js;
    jct_ta.drawResults();
};

jct_ta.drawResults = () => {
    let results = jct_ta.latest_full_response;
    let frag = `
    <style>
        #jct_ta_results_list td {
            padding: 3px 5px 0 5px;
        }
        #jct_ta_results_list td a {
            text-decoration: none;
        }
    </style>
    <a href="#" id="jct_ta_results_clear">Clear search and start again</a>
    <table style="width: 100%">
        <thead style="color: #fff;
                    font-weight: bold;">
            <tr style="border-bottom: #fff 2px solid;">
                <td>ESAC ID</td>
                <td title="Some TAs specify more than one list of Journals and Institutions.  Where present, the different relationships between those lists are identified here">Journal to Institution Relationship</td>
                <td>Expires</td>
            </tr>
            </thead>
            <tbody style="color: #ffffff">`;

    if (results.length > 0) {
        let last_result = false;
        for (let result of results) {
            frag += jct_ta.result_html(result, last_result);
            last_result = result;
        }
    } else {
        let journal = "";
        let institution = "";
        let and = "";
        if (jct_ta.chosen.journal) {
            journal = " Journal ";
        }
        if (jct_ta.chosen.institution) {
            institution = " Institution ";
        }
        if (journal !== "" && institution !== "") {
            and = " and ";
        }
        frag += `<tr><td colspan="3">No Transformative Agreements found which contain your selected ${journal} ${and} ${institution}</td></tr>`;
    }
    frag += `</tbody></table>`;
    jct_ta.d.gebi('jct_ta_results_list').innerHTML = frag;
    jct_ta.d.gebi('jct_ta_results').style.display = 'block';

    jct_ta.d.gebi('jct_ta_results_clear').addEventListener('click', (e) => {
        e.preventDefault();
        jct_ta.clinputs.journal.reset({silent: true});
        jct_ta.clinputs.institution.reset({silent: true});
        jct_ta.chosen = {};
        jct_ta.d.gebi('jct_ta_results_list').innerHTML = "";
        jct_ta.d.gebi('jct_ta_results').style.display = 'none';

    });
};

jct_ta.result_html = (result, last_result) => {
    let rel = result.jct_id.substring(result.esac_id.length + 1);
    if (rel.length === 0) {
        rel = "No additional relationships specified";
    }

    let esac_link = `<a href="https://esac-initiative.org/about/transformative-agreements/agreement-registry/${result.esac_id}" target="_blank">${result.esac_id}</a>`;
    if (last_result && last_result.esac_id === result.esac_id) {
        esac_link = "&nbsp;";
    }

    return `
    <tr>
    <td>${esac_link}</td> 
    <td><a href="${result.data_url}">${rel}</a></td>
    <td>${result.end_date}</td>
    </tr>
    `;
};

jct_ta.choose = (e, el, which) => {
    jct_ta.chosen[which] = el;
    // let next = jct.inputsCycle[which];
    // if (next) {
    //     let inp = jct.clinputs[next];
    //     if (!inp.hasChoice()) {
    //         inp.activate();
    //     }
    // }
    jct_ta.cycle();
};

jct_ta.clear = (which) => {
    jct_ta.chosen[which] = null;
    jct_ta.cycle();
};

jct_ta.cycle = () => {
    if (jct_ta.chosen.journal || jct_ta.chosen.institution) {
        let qr = {};
        if (jct_ta.chosen.journal) {
            qr.issn = jct_ta.chosen.journal.id;
        }
        if (jct_ta.chosen.institution) {
            qr.ror = jct_ta.chosen.institution.id;
        }
        jct_ta.jx('ta_search', qr);
        // jct_ta.d.gebi("jct_loading").style.display = "block";
    }
};

jct_ta.selectionToText = function(clInputInstance) {
    let lsv = clInputInstance.currentSearch().toLowerCase();
    let selection = clInputInstance.currentSelection();

    if (!selection) {
        return clInputInstance.currentSearch();
    }

    if (typeof(selection) === "string") {
        return selection;
    }

    if (selection.title) {
        return selection.title;
    }

    let keys = Object.keys(selection);
    for (let i = 0; i < keys.length; i++) {
        let key = keys[i];
        let v = selection[key];
        if (Array.isArray(v)) {
            for (var j = 0; j < v.length; j++) {
                if (v[j].toLowerCase().includes(lsv)) {
                    return v[j];
                }
            }
        } else if (typeof(v) === "string") {
            if (v.toLowerCase().includes(lsv)) {
                return v;
            }
        }
    }

    if (keys.length > 0) {
        let v = selection[keys[0]]
        if (Array.isArray(v)) {
            if (v.length > 0) {
                return v[0];
            }
        } else {
            return v;
        }
    }

    return "";
};

jct_ta.setup = () => {
    jct_ta.d.gebi("jct_ta_inputs").innerHTML = jct_ta.inputs_plugin_html();
    // jct_ta.d.gebi("jct_ta_results").innerHTML = jct_ta.results_plugin_html;

    jct_ta.clinputs.journal = clinput.init({
        element: jct_ta.d.gebi("jct_journal-container"),
        id: "jct_journal",
        label: "Limit by Journal",
        logState: false,
        // initialSelection: params.value,
        // inputAttributes: params.inputAttributes,
        options: (text, callback) => {
            let effectiveTextLength = text.length;
            let pattern = /[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9xX]/;
            if (!pattern.test(text)) {
                let effective_text = jct_ta.suggest_prepare(text, ["of", "the", "and", "journa", "journal"]);
                effectiveTextLength = effective_text.length;
            }
            if (effectiveTextLength >= 3) {
                let ourcb = (xhr) => {
                    let js = JSON.parse(xhr.response);
                    callback(js.data);
                };
                jct_ta.jx('suggest/journal/'+text, false, ourcb);
            } else {
                // FIXME: this should be handled inside clinput
                callback([]);
            }
        },
        optionsTemplate: (obj) => {
            let t = obj.title;
            let issns = obj.issns.join(", ");
            let publisher = obj.publisher;
            let frag = "<a class='optionsTemplate'>";

            if (t) {
                frag += '<span class="jct__option_journal_title">' + t + '</span>';
            }
            if (publisher) {
                frag += ' <span class="jct__option_journal_publisher">(' + publisher.trim() + ')</span> ';
            }
            let issnPrefix = "";
            if (!t && !publisher) {
                issnPrefix = "ISSN: ";
            }
            frag += ' <span class="jct__option_journal_issn">' + issnPrefix + issns + '</span></a> ';
            return frag;
        },
        selectedTemplate: (obj) => {
            let t = obj.title;
            let issns = obj.issns;
            let publisher = obj.publisher;

            let frag = "";
            if (t) {
                frag += t;
            }
            if (publisher) {
                frag += " (" + publisher.trim() + ")";
            }
            if (issns) {
                if (t || publisher) {
                    frag += ", ";
                }
                frag += "ISSN: " + issns.join(", ");
            }
            return frag;
        },
        selectionToSearchText: jct_ta.selectionToText,
        newValue: false,
        onChoose: function(e, obj) {
            jct_ta.choose(e, obj, "journal");
        },
        onClear: function(e, idx) {
            jct_ta.clear("journal");
        }
    });

    jct_ta.clinputs.institution = clinput.init({
        element: jct_ta.d.gebi("jct_institution-container"),
        id: "jct_institution",
        label: "Limit by Institution",
        // initialSelection: params.value,
        // inputAttributes: params.inputAttributes,
        logState: false,
        options: (text, callback) => {
            let effective_text = jct_ta.suggest_prepare(text, ["of", "the", "and", "universi", "universit", "university"])
            let effectiveTextLength = effective_text.length;
            if (effectiveTextLength >= 3) {
                let ourcb = (xhr) => {
                    let js = JSON.parse(xhr.response);
                    callback(js.data);
                };
                jct_ta.jx('suggest/institution/'+text, false, ourcb);
            } else {
                // FIXME: this should be handled inside clinput
                callback([]);
            }
        },
        optionsTemplate: (obj) => {
            let frag = '<a class="optionsTemplate"><span class="jct__option_institution_title">' + obj.title + '</span>';
            if (obj.alternate && !(/^[a-zA-Z0-9 ]+$/.test(obj.alternate))) {
                // has alternate non-english title. Use it
                frag += '<span class="jct__option_institution_alt_title"> (' +  obj.alternate + ')</span>';
            }
            if (obj.country) {
                frag += '<span class="jct__option_institution_country">, ' + obj.country + '</span>';
            }
            if (obj.id) {
                frag += ' <span class="jct__option_institution_id"> (ROR:' + obj.id + ')</span>';
            }
            frag += '</a>';
            return frag;
        },
        selectedTemplate: (obj) => {
            let frag = obj.title;
            if (obj.alternate && !(/^[a-zA-Z0-9 ]+$/.test(obj.alternate))) {
                // has alternate non-english title. Use it
                frag += ' (' + obj.alternate + ')';
            }
            if (obj.country) {
                frag += ', ' + obj.country;
            }
            if (obj.id) {
                frag += ' (ROR:' + obj.id + ')';
            }
            return frag;
        },
        selectionToSearchText: jct_ta.selectionToText,
        newValue: false,
        onChoose: function(e, obj) {
            jct_ta.choose(e, obj, "institution");
        },
        onClear: function(e, idx) {
            jct_ta.clear("institution");
        }
    });
};