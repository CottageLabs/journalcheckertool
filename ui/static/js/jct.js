// ----------------------------------------
// Initial definitions
// ----------------------------------------
let jct = {
    api: JCT_API_endpoint,
    host: JCT_UI_BASE_URL,
    delay: 500,
    cache: {},
    chosen: {},
    latest_response: null,
    latest_full_response: null,
    lang: null,
    funder_langs: {},
    load : {
        funder: false,
        response: false
    },
    site_modals : {},
    modal_setup : {},
    clinputs: {},
    inputsCycle: {
        "journal" : "funder",
        "funder" : "institution"
    }
};

jct.d = document;
jct.d.gebi = document.getElementById;
jct.d.gebc = document.getElementsByClassName;

////////////////////////////////////////////////////////
// HTML Fragments for Application structure

// ----------------------------------------
// html for input form
// ----------------------------------------
jct.inputs_plugin_html =`
    <h2 class="sr-only">Make a query</h2>
    <div class="col col--1of3 expression">
        <div class="expression__input" id="jct_journal-container">
        </div>
        <div class="expression__operator">
            <svg width="36" height="36" viewbox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18.3 3L18.3 33M3 17.7H33" stroke="white" stroke-width="5" stroke-linecap="round"></path>
            </svg>
        </div>
    </div>

    <div class="col col--1of3 expression">
        <div class="expression__input"  id="jct_funder-container">
        </div>
        <div class="expression__operator">
            <svg width="36" height="36" viewbox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18.3 3L18.3 33M3 17.7H33" stroke="white" stroke-width="5" stroke-linecap="round"></path>
            </svg>
        </div>
    </div>

    <div class="col col--1of3 expression">
        <div class="expression__input">
            <div id="jct_institution-container">
            </div>
            <br>
            <div class="expression__checkbox">
                <input type="checkbox" id="jct_notHE" name="notHE">
                <label for="notHE">No affiliation</label>
            </div>
        </div>
        <div class="expression__operator">
            <div>
                <svg width="70" height="70" viewbox="0 0 70 70" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M22.5 22C21.1193 22 20 23.1193 20 24.5C20 25.8807 21.1193 27 22.5 27H47.5C48.8807 27 50 25.8807 50 24.5C50 23.1193 48.8807 22 47.5 22H22.5ZM22.5 42C21.1193 42 20 43.1193 20 44.5C20 45.8807 21.1193 47 22.5 47H47.5C48.8807 47 50 45.8807 50 44.5C50 43.1193 48.8807 42 47.5 42H22.5Z" fill="white"></path>
                </svg>
            </div>
        </div>
    </div>

    <div class="col col--1of3 suggest" id="jct_suggestjournal">
    </div>
    <div class="col col--1of3 suggest" id="jct_suggestfunder">
    </div>
    <div class="col col--1of3 suggest" id="jct_suggestinstitution">
    </div>
    <div class="loading" id="jct_loading" style="display:none">
        <div class="loading__dots">
            <div></div>
            <div></div>
            <div></div>
            <span class="sr-only">Loading choices…</span>
        </div>
    </div>
`;

// ----------------------------------------
// html for results_plugin
// ----------------------------------------
jct.results_plugin_html = `
    <header class="jct_compliance">
        <h2 id="jct_compliant" style="display:none"></h2>
        <h2 id="jct_notcompliant" style="display:none"></h2>
    </header>
`;

// ----------------------------------------
// html for tiles_plugin
// ----------------------------------------
jct.tiles_plugin_html = `
    <section class="row" id="jct_paths_results">
        <h3 class="sr-only">Results</h3>
    </section>
`;

// ----------------------------------------
// Function to display the selected list of tiles
// ----------------------------------------
jct.displayCards = (cardsToDisplay, result) => {
    // let chosen_data = jct.chosen;
    for (let i = 0; i < cardsToDisplay.length; i++) {
        let cardConfig = cardsToDisplay[i];
        let card = jct.buildCard(cardConfig, jct.lang, result, jct.chosen);
        jct.d.gebi("jct_paths_results").append(jct.htmlToElement(card));
    }
}

// ----------------------------------------
// Function to display specific card
// ----------------------------------------
jct.buildCard = function(cardConfig, uiText, results, choices) {
    // img: cards.[card_id].icon
    // site.preferred
    // cards.[card_id].title
    //
    // cards.[card_id].body.default
    // cards.[card_id].body.[compliant route id]

    let cardText = uiText.cards[cardConfig.id];

    // get the icon if it exists, and the icon identifier is not "false" (the string).
    let icon = "";
    if (cardText.icon) {
        icon = uiText.icons[cardText.icon];
        if (icon === undefined) {
            icon = "";
        }
    }

    let preferred = cardConfig.preferred ? `<em>${uiText.site.preferred}</em><br><br>` : "";
    let modalText = uiText.site.card_modal;
    if (cardText.modal) {
        modalText = cardText.modal;
    }
    let modal = cardConfig.hasOwnProperty("modal") ? `<strong><a href="#" class="modal-trigger" data-modal="${cardConfig.modal}">${modalText}</a></strong>` : "";

    let body = "";
    if (cardText.body.hasOwnProperty("default")) {
        body += cardText.body.default;
    }

    let compliantRoutes = [];
    for (let i = 0; i < results.length; i++) {
        let r = results[i];
        if (r.compliant === "yes") {
            compliantRoutes.push(r.route);
        }
    }

    if (cardConfig.hasOwnProperty("display_if_compliant")) {
        for (let i = 0; i < cardConfig.display_if_compliant.length; i++) {
            let route = cardConfig.display_if_compliant[i];
            if (compliantRoutes.includes(route)) {
                if (cardText.body.hasOwnProperty(route)) {
                    body += cardText.body[route];
                }
            }
        }
    }

    body = body.replace("{title}", choices.journal.title);
    body = body.replace("{funder}", choices.funder.title);
    body = body.replace("{publisher}", choices.journal.publisher);

    if (choices.institution) {
        body = body.replace("{institution}", choices.institution.title);
    } else {
        body = body.replace("{institution}", uiText.site.card_institution_missing);
    }

    let cardClass = "card"
    let why = "";
    // TODO: this enables a "why am I seeing this?" feature on the card which links to the
    // results explanation on a per-card basis.  We have agreed not to enable this for the moment
    // while we review the text
    //
    // if (cardConfig.compliant && !window.JCT_WIDGET) {
    //     why = `<div class="read_more_banner"><a href="#" class="read_more" data-card="${cardConfig.id}">${jct.lang.site.why_am_i_seeing_this}</a></div>`;
    //     cardClass = "card explainable_card";
    // }

    return `<div class="col col--1of4">
        <article class="${cardClass}">
            ${icon}
            <h4 class="label card__heading">
                ${preferred}
                <span>${cardText.title}</span>
            </h4>
            ${body}
            <p>${modal}</p>
            ${why}
        </article>
    </div>`;
}

////////////////////////////////////////////////
// Modal handling

jct.bindModals = function() {
    let triggers = document.getElementsByClassName("modal-trigger");
    for (let i = 0; i < triggers.length; i++) {
        let trigger = triggers[i];
        trigger.removeEventListener("click", jct.modalTrigger);
        trigger.addEventListener("click", jct.modalTrigger)
    }

    let readMores = document.getElementsByClassName("read_more");
    for (let i = 0; i < readMores.length; i++) {
        let trigger = readMores[i];
        trigger.removeEventListener("click", jct.readMoreTrigger);
        trigger.addEventListener("click", jct.readMoreTrigger)
    }
}

jct.readMoreTrigger = function(event) {
    event.preventDefault();
    let element = event.target;
    let cardId = element.getAttribute("data-card");
    let modal = jct.readMoreModal(cardId);
    jct.modalShow(modal);
}

jct.readMoreModal = function(cardId) {
    let content = jct.explain_card(jct.latest_full_response, cardId);

    let modal_html = `<div class="modal" id="jct_modal_${cardId}" style="display: block">
        <div class="modal-content" id="jct_modal_${cardId}_content">
            <header class="modal-header">
                <h2>
                    <span class="close jct_modal_close" aria-label="Close" role="button" data-id="jct_modal_${cardId}">&times;</span>
                    ${jct.lang.cards[cardId].explain.title}
                </h2>
            </header>
            <div>${content}</div>
        </div>
    </div>`;
    return modal_html;
}

jct.modalTrigger = function(event) {
    event.preventDefault();
    let element = event.target;
    let modalId = element.getAttribute("data-modal");
    let modal = jct.build_modal(modalId);
    jct.modalShow(modal);
    if (jct.modal_setup.hasOwnProperty(modalId)) {
        jct.modal_setup[modalId]();
    }
}

jct.modalShow = function(content) {
    let modal_div = jct.d.gebi("jct_modal_container");
    modal_div.innerHTML = content;

    let closers = document.getElementsByClassName("jct_modal_close");
    for (let i = 0; i < closers.length; i++) {
        closers[i].addEventListener("click", (e) => {
            jct.closeModal();
        });
    }

    window.addEventListener("click", jct._windowCloseModal)
}

jct.closeModal = function() {
    let modal_div = jct.d.gebi("jct_modal_container");
    modal_div.innerText = "";
    window.removeEventListener("click", jct._windowCloseModal)
}

jct._windowCloseModal = function(e) {
    let modals = [].slice.call(jct.d.gebc("modal"));
    if (modals.includes(e.target)){
        jct.closeModal();
    }
}

jct.build_modal = (modal_id) => {
    let modalText = jct.lang ? jct.lang.modals[modal_id] : "";
    if (!modalText) {
        modalText = jct.site_modals[modal_id];
    }
    if (!modalText) {
        return "";
    }
    let modal_html = `<div class="modal" id="jct_modal_${modal_id}" style="display: block">
        <div class="modal-content" id="jct_modal_${modal_id}_content">
            <header class="modal-header">
                <h2>
                    <span class="close jct_modal_close" aria-label="Close" role="button" data-id="jct_modal_${modal_id}">&times;</span>                    
                    ${modalText.title}
                </h2>
            </header>
            <div>${modalText.body}</div>
        </div>
    </div>`
    return modal_html;
}

//////////////////////////////////////////////
// Funder autocomplete

jct.indexFunders = function() {
    for (let i = 0; i < jct.funderlist.length; i++) {
        let funder = jct.funderlist[i];
        let tokens = []
        tokens = tokens.concat(jct.tokenise(funder.country));
        tokens = tokens.concat(jct.tokenise(funder.name));
        tokens = tokens.concat(jct.tokenise(funder.abbr));
        jct.funderlist[i].tokens = tokens
    }
}

jct.tokenise = function(str) {
    if (!str) { return [] }
    return str.trim().split(" ").map(x => x.trim().toLowerCase())
}

jct.searchFunders = function(str) {
    let searchTokens = jct.tokenise(str);

    // find all matching records
    let matches = {};
    for (let j = 0; j < jct.funderlist.length; j++) {
        let funder = jct.funderlist[j];
        for (let i = 0; i < searchTokens.length; i++) {
            let st = searchTokens[i];
            // first check the search tokens
            for (let k = 0; k < funder.tokens.length; k++) {
                let ft = funder.tokens[k]
                let idx = ft.indexOf(st);
                if (idx > -1) {
                    let add = 1;
                    if (idx === 0) {
                        add = 2;
                    }
                    if (matches.hasOwnProperty(funder.id)) {
                        matches[funder.id+funder.name].score += add;
                    } else {
                        matches[funder.id+funder.name] = {"record" : funder, "score" : add}
                    }
                }
            }

            // then also check the funder id, which is a high scoring match
            if (st === funder.id && funder.primary) {
                if (matches.hasOwnProperty(funder.id+funder.name)) {
                    matches[funder.id+funder.name].score += 100;
                } else {
                    matches[funder.id+funder.name] = {"record" : funder, "score" : 100}
                }
            }
        }
    }

    // sort the records by score
    let matchIds = Object.keys(matches);
    let matchRecords = []
    for (let i = 0; i < matchIds.length; i++) {
        let id = matchIds[i];
        matchRecords.push(matches[id]);
    }
    matchRecords.sort((a, b) => a.score < b.score ? 1 : -1);

    return matchRecords
}


////////////////////////////////////////////////
// Utilities

// ----------------------------------------
// Function _emptyElement
// ----------------------------------------
jct._emptyElement = (elem) => {
    while (elem.firstChild) elem.removeChild(elem.firstChild);
}

// ----------------------------------------
// helper function to iterate over all
// ----------------------------------------
jct.d.each = (cls, key, val) => {
    if (cls.indexOf('.') === 0) cls = cls.replace('.','');
    let els = jct.d.gebc(cls);
    for ( let i = 0; i < els.length; i++ ) {
        if (typeof key === 'function') {
            key(els[i]);
        } else {
            els[i][key] = val;
        }
    }
};

// ----------------------------------------
// function to do api calls
// ----------------------------------------
jct.jx = (route,q,after,api) => {
    let base_url = api ? api : jct.api;
    let url;
    if (route) {
        url = new URL(route, base_url);
    } else {
        url = new URL(base_url);
    }
    if (!q === false) {
        let searchParams = new URLSearchParams(q);
        for (const [key, value] of searchParams.entries()) {url.searchParams.append(key, value)}
    }

    // request the calculation
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url.href);
    xhr.send();
    xhr.onload = () => { xhr.status !== 200 ? jct.error(xhr) : (typeof after === 'function' ? after(xhr) : jct.result_loaded(xhr)); };
    xhr.onprogress = (e) => { jct.progress(e); };
    xhr.onerror = () => { jct.error(); };

    // request the funder language for the calculation
    if (route === "calculate") {
        jct.load.funder = false;
        jct.load.response = false;

        if (jct.funder_langs.hasOwnProperty(q.funder)) {
            jct.load_funder(q.funder, jct.funder_langs[q.funder]);
            return;
        }
        let funderUrl = new URL("funder_language/" + q.funder, base_url)
        let fxhr = new XMLHttpRequest();
        // fxhr.open("GET", new URL(base_url + "/funder_language/" + q.funder));
        fxhr.open("GET", funderUrl.href);
        fxhr.send();
        fxhr.onload = () => { fxhr.status !== 200 ? jct.funder_error(fxhr) : jct.funder_loaded(q.funder, fxhr); };
        fxhr.onerror = () => { jct.funder_error(); };
    }
}

// ----------------------------------------
// handy function to add html to elements
// ----------------------------------------
jct.htmlToElement = (html) => {
    let template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}

///////////////////////////////////////////////////////
// Query lifecycle functions

// ----------------------------------------
// function to calculate if all data provided by the input boxes
// ----------------------------------------
jct._calculate_if_all_data_provided = () => {
    if (jct.chosen.journal && jct.chosen.funder && (jct.chosen.institution || jct.d.gebi("jct_notHE").checked)) {
        jct.suggesting = false;
        let qr = {issn: jct.chosen.journal.id};
        qr.funder = jct.chosen.funder.id;
        if (jct.chosen.institution) {
            qr.ror = jct.chosen.institution.id;
        }
        jct.jx('calculate', qr);
        jct.d.gebi("jct_loading").style.display = "block";
    }
}

// ----------------------------------------
// function to handle errors from main api response
// ----------------------------------------
jct.error = (xhr) => {
    jct.latest_response = xhr;
}

// ----------------------------------------
// function to handle progress from main api response
// ----------------------------------------
jct.progress = (e) => {
    // not used
}

// ----------------------------------------
// function to handle success from main api response
// ----------------------------------------
jct.success = () => {
    let js = jct.latest_full_response;

    jct.d.gebi('jct_compliant').style.display = 'none';
    jct.d.gebi('jct_notcompliant').style.display = 'none';
    jct.d.gebi("jct_loading").style.display = "none";

    let paths_results = jct.d.gebi("jct_paths_results");
    jct._emptyElement(paths_results)
    jct.display_result(js);
    if (jct.d.gebi("jct_explain_results")) {
        jct.d.gebi('jct_explain_results').style.display = 'initial';
        jct.d.hide_detailed_results();
        jct.explain(js)
    }
    let print = jct.d.gebi('jct_print');
    if (print) {
        print.style.display = 'initial';
    }
    if (jct.d.gebi("jct_find_out_more")) {
        jct.setup_fom_url();
    }
    jct.bindModals();
}

jct.funder_error = (xhr) => {
    alert("Unable to load funder language pack, please try again");
    // this is going to need to cancel the request to reset the UI
}

jct.funder_loaded = (funder_id, xhr) => {
    let js = JSON.parse(xhr.response);
    jct.load_funder(funder_id, js);
}

jct.load_funder = (funder_id, lang) => {
    jct.funder_langs[funder_id] = lang;
    jct.lang = jct.funder_langs[funder_id];
    jct.load.funder = true;
    jct.doSuccess();
}

jct.doSuccess = () => {
    if (jct.load.funder && jct.load.response) {
        jct.success();
    }
}

jct.result_loaded = (xhr) => {
    let js = JSON.parse(xhr.response);
    if (!jct.result_equals_chosen(js.request)) {
        return;
    }
    jct.latest_full_response = js;
    jct.latest_response = js.results;
    jct.load.response = true;
    jct.doSuccess();
}

//-----------------------------------------
// function to display the results
//-----------------------------------------
jct.display_result = (js) => {
    if (js.compliant) {
        let compliantHeader = jct.d.gebi('jct_compliant');
        compliantHeader.innerText = jct.lang.site.compliant;
        compliantHeader.style.display = 'block';

        jct._setComplianceTheme(true);
    } else {
        let compliantHeader = jct.d.gebi('jct_notcompliant');
        compliantHeader.innerText = jct.lang.site.non_compliant;
        compliantHeader.style.display = 'block';

        jct._setComplianceTheme(false);
    }

    // jct.d.gebi(js.compliant ? 'jct_compliant' : 'jct_notcompliant').style.display = 'block';
    jct.d.gebi("jct_results").style.display = 'block';
    // if (js.compliant) {
    //
    // }
    // else {
    //
    // }
    let cardsToDisplay = js.cards;
    jct.displayCards(cardsToDisplay, js.results);

    x = window.matchMedia("(max-width: 767px)")
    let results_section_top = jct.d.gebi("jct_results_plugin").offsetTop
    let inputs_height = 0
    if (!x.matches) {
        inputs_height = jct.d.gebi("jct_journal").offsetHeight
    }
    if (typeof window.JCT_WIDGET == 'undefined'){
        window.scrollTo(0, results_section_top - inputs_height)
    }
}

// ----------------------------------------
// function to set the theme (add appropriate div classes) based on compliance of results
// ----------------------------------------
jct._setComplianceTheme = (compliant) => {
    let query_div = jct.d.gebi('jct_query');
    let results_div = jct.d.gebi('jct_results');
    if (compliant === undefined) {
        if (query_div.classList.contains("query--non-compliant")) {
            query_div.classList.remove("query--non-compliant");
        }
        if (results_div.classList.contains("results--non-compliant")) {
            results_div.classList.remove("results--non-compliant");
        }
        if (query_div.classList.contains("query--compliant")) {
            query_div.classList.remove("query--compliant");
        }
        if (results_div.classList.contains("results--compliant")) {
            results_div.classList.remove("results--compliant");
        }
    }
    else if (compliant){
        if (query_div.classList.contains("query--non-compliant")) {
            query_div.classList.remove("query--non-compliant");
        }
        if (results_div.classList.contains("results--non-compliant")) {
            results_div.classList.remove("results--non-compliant");
        }
        query_div.classList.add('query--compliant');
        results_div.classList.add('results--compliant');
    }
    else {
        if (query_div.classList.contains("query--compliant")) {
            query_div.classList.remove("query--compliant");
        }
        if (results_div.classList.contains("results--compliant")) {
            results_div.classList.remove("results--compliant");
        }
        query_div.classList.add('query--non-compliant');
        results_div.classList.add('results--non-compliant');
    }
}

// ----------------------------------------
// Function to scroll to the result tiles
// ----------------------------------------
jct.scroll_to_result_tiles = () => {
    x = window.matchMedia("(max-width: 767px)")
    let results_section_top = jct.d.gebi("jct_results_plugin").offsetTop
    let inputs_height = 0
    if (!x.matches) {
        inputs_height = jct.d.gebi("jct_journal").offsetHeight
    }
    window.scrollTo(0, results_section_top - inputs_height)
    //results_section.scrollIntoView({scrollIntoViewOptions: true, behaviour: "smooth"})
}

// ----------------------------------------
// function to check if the results obtained from the api
// are the same as the currently chosen user options
// ----------------------------------------
jct.result_equals_chosen = (js) => {
    // jct.chosen holds the current chosen object
    // js is the result request
    // The chosen journal id should exist in the list of ISSNs returned by the request. If no data, going with true
    let j_matches = (jct.chosen.journal && js.journal && js.journal[0]) ?
        (js.journal[0].issn.includes(jct.chosen.journal.id)) : true;
    // The funder ids should be equal. If no data, going with true
    let f_matches = (jct.chosen.funder && js.funder && js.funder[0]) ?
        (jct.chosen.funder.id === js.funder[0].id) : true;
    // The institution may not exist in case of notHE.
    // The institution ids should be equal. If no data, going with true
    let i_matches = (jct.chosen.institution && js.institution && js.institution[0]) ?
        (jct.chosen.institution.id === js.institution[0].id) : true;
    let result = j_matches && i_matches && f_matches;
    // Add missing details to jct.chosen (when a user doesn't select from drop down)
    if (result) {
        // Add missing details to jct.chosen.journal
        if (jct.chosen.journal && js.journal && js.journal[0]) {
            if (!jct.chosen.journal.title && js.journal[0].title) {
                jct.chosen.journal.title = js.journal[0].title
            }
            if (!jct.chosen.journal.publisher && js.journal[0].publisher) {
                jct.chosen.journal.publisher = js.journal[0].publisher
            }
        }
        // Add missing details to jct.chosen.funder
        if (jct.chosen.funder && js.funder && js.funder[0]) {
            if (!jct.chosen.funder.title && js.funder[0].title) {
                jct.chosen.funder.title = js.funder[0].title
            }
        }
        // Add missing details to jct.chosen.institution
        if (jct.chosen.institution && js.institution && js.institution[0]) {
            if (!jct.chosen.institution.title && js.institution[0].title) {
                jct.chosen.institution.title = js.institution[0].title
            }
        }
    }
    return result;
}

///////////////////////////////////////////////////////
// Autosuggest input box management

// ----------------------------------------
// function to set focus on next element after choosing from auto suggestion and
// calculate if all data provided
// ----------------------------------------
jct.choose = (e, el, which) => {
    jct.chosen[which] = el;
    let next = jct.inputsCycle[which];
    if (next) {
        let inp = jct.clinputs[next];
        if (!inp.hasChoice()) {
            inp.activate();
        }
    }
    if (which === "institution") {
        jct.d.gebi('jct_notHE').checked = false;
    }
    // if (which === 'journal') {
    //     jct.d.gebi('jct_funder').focus();
    // } else if (which === 'funder') {
    //     jct.d.gebi('jct_institution').focus();
    // } else {
    //     jct.d.gebi('jct_institution').blur();
    //     jct.d.gebi('jct_notHE').checked = false;
    // }
    jct._calculate_if_all_data_provided();
}

// ----------------------------------------
// function to apply default values to the select boxes
// and which runs the compliance check if all boxes are set
// ----------------------------------------
jct.set_each_default = (type, value) => {
    let doChoose = (selectedObject) => {
        jct.chosen[type] = selectedObject;
        jct._calculate_if_all_data_provided();
    }
    jct.clinputs[type].setChoice(value, doChoose);
}

//////////////////////////////////////////////////////////////
// Toggling detailed results

// ----------------------------------------
// function to show detailed results
// ----------------------------------------
jct.d.show_detailed_results = () => {
    let explainResults = jct.d.gebi("jct_explain_results");
    if (explainResults) {
        explainResults.innerHTML = 'Hide explanation';
    }
    jct.d.gebi('jct_detailed_results').style.display = "flex";
    // let print = jct.d.gebi('jct_print');
    // if (print) {
    //     print.style.display = 'initial';
    // }
}

// ----------------------------------------
// function to hide detailed results
// ----------------------------------------
jct.d.hide_detailed_results = () => {
    let explainResults = jct.d.gebi("jct_explain_results");
    if (explainResults) {
        explainResults.innerHTML = 'Explain this result';
    }
    jct.d.gebi('jct_detailed_results').style.display = "none";
    // let print = jct.d.gebi('jct_print');
    // if (print) {
    //     print.style.display = 'none';
    // }
}

// ----------------------------------------
// function to toggle detailed results
// ----------------------------------------
jct.d.toggle_detailed_results = () => {
    let section = jct.d.gebi('jct_detailed_results');
    if (section.style.display === "none") {
        jct.d.show_detailed_results();
    } else {
        jct.d.hide_detailed_results();
    }
}

jct.suggest_prepare = (txt, stop_words) => {
    txt = txt.toLowerCase().trim();
    for (let sw of stop_words) {
        let fullThing = new RegExp("^" + sw + "$");
        let atEnd = new RegExp(" " + sw + "$");
        let atStart = new RegExp("^" + sw + " ");
        let inMiddle = new RegExp(" " + sw + " ");

        txt = txt.replace(fullThing, "").replace(atEnd, "").replace(atStart, "").replace(inMiddle, " ")
    }
    while (true) {
        if (!(txt.includes("  "))) {
            break
        }
        txt.replace("  ", " ")
    }
    return txt
}

//////////////////////////////////////////////////////////
// Initialisation

// ----------------------------------------
// Setup JCT on a fresh page
// ----------------------------------------
jct.setup = (manageUrl=true) => {
    jct.d.gebi("jct_inputs_plugin").innerHTML = jct.inputs_plugin_html;
    jct.d.gebi("jct_results_plugin").innerHTML = jct.results_plugin_html;
    jct.d.gebi("jct_tiles_plugin").innerHTML = jct.tiles_plugin_html;
    let f = jct.d.gebi("jct_funder");
    jct.suggesting = true;

    // index the funders for autocomplete (this must be done before we initialise or trigger the CLInputs)
    jct.indexFunders();

    window.onscroll = (e) => {
        x = window.matchMedia("(max-width: 767px)")
        let inputs = jct.d.gebi("jct_inputs_plugin")
        if (window.pageYOffset > jct.input_top && !x.matches) {
            inputs.classList.add("sticky")
        }
        else {
            inputs.classList.remove("sticky")
        }

    }

    let scroll_to_top_if_sticky = () => {
        if (jct.d.gebi("jct_inputs_plugin").classList.contains("sticky")) {
            window.scrollTo(0, 0);
        }
    }

    jct.inputValues = {
        Journal: "",
        Funder: "",
        Institution: "",
        notHE: ""
    }

    jct.clinputs.journal = clinput.init({
        element: jct.d.gebi("jct_journal-container"),
        id: "jct_journal",
        label: "Journal",
        inputAttributes : {
            which: "journal",
            placeholder: "By ISSN or title",
            required: true,
            autocomplete: "off"
        },
        options : function(text, callback) {
            let effectiveTextLength = text.length;
            let pattern = /[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9xX]/;
            if (!pattern.test(text)) {
                let effective_text = jct.suggest_prepare(text, ["of", "the", "and", "journa", "journal"])
                effectiveTextLength = effective_text.length;
            }
            if (effectiveTextLength >= 3) {
                let ourcb = (xhr) => {
                    let js = JSON.parse(xhr.response);
                    callback(js.data);
                }
                jct.jx('suggest/journal/'+text, false, ourcb);
            }
        },
        optionsTemplate : function(obj) {
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
        selectedTemplate : function(obj) {
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
        onChoice: function(e,el) {
            jct.choose(e,el, "journal");
        },
        rateLimit: 400,
        optionsLimit: 10,
        allowClear: true,
        newValue: function(text) {
            let rx = /^\d{4}-\d{3}[\dXx]{1}$/
            let match = text.match(rx);
            if (match) {
                return {
                    issn: [text],
                    id: text
                }
            }
            return false;
        }
    });

    jct.clinputs.funder = clinput.init({
        element: jct.d.gebi("jct_funder-container"),
        id: "jct_funder",
        label: "My funder",
        inputAttributes : {
            which: "funder",
            placeholder: "By funder name",
            required: true,
            autocomplete: "off"
        },
        options : function(text, callback) {
            if (text.length > 1) {
                let results = jct.searchFunders(text);
                let options = results.map((x) => x.record);
                callback(options);
            }
        },
        optionsTemplate : function(obj) {
            let entry = obj.name;
            if (obj.country) {
                entry += ", " + obj.country;
            }
            if (obj.abbr) {
                entry += " (" + obj.abbr + ")";
            }
            return '<a class="optionsTemplate"><span class="jct__option_publisher_title">' + entry + '</span>';
        },
        selectedTemplate : function(obj) {
            let entry = obj.name;
            if (obj.country) {
                entry += ", " + obj.country;
            }
            if (obj.abbr) {
                entry += " (" + obj.abbr + ")";
            }
            return entry;
        },
        onChoice: function(e,el) {
            jct.choose(e,el, "funder");
        },
        selectedObjectToSearchString: function(selected) {
            return selected.name
        },
        rateLimit: 0,
        optionsLimit: 10,
        allowClear: true,
    });

    jct.clinputs.institution = clinput.init({
        element: jct.d.gebi("jct_institution-container"),
        id: "jct_institution",
        label: "My institution",
        inputAttributes : {
            which: "institution",
            placeholder: "By ROR or name",
            required: true,
            autocomplete: "off"
        },
        options : function(text, callback) {
            let effective_text = jct.suggest_prepare(text, ["of", "the", "and", "universi", "universit", "university"])
            let effectiveTextLength = effective_text.length;
            if (effectiveTextLength >= 3) {
                let ourcb = (xhr) => {
                    let js = JSON.parse(xhr.response);
                    callback(js.data);
                }
                jct.jx('suggest/institution/'+text, false, ourcb);
            }
        },
        optionsTemplate : function(obj) {
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
            frag += '</a>'
            return frag;
        },
        selectedTemplate : function(obj) {
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
        onChoice: function(e,el) {
            jct.choose(e,el, "institution");
        },
        rateLimit: 400,
        optionsLimit: 10,
        allowClear: true,
    });

    jct.input_top = jct.d.gebi("jct_journal-container").getElementsByTagName("input")[0].getBoundingClientRect().top

    jct.d.gebi("jct_journal").addEventListener("click", scroll_to_top_if_sticky)
    jct.d.gebi("jct_funder").addEventListener("click", scroll_to_top_if_sticky)
    jct.d.gebi("jct_institution").addEventListener("click", scroll_to_top_if_sticky)

    jct.d.gebi("jct_notHE").addEventListener("click", (event) => {
        if (event.target.checked && jct.chosen.institution) {
            jct.clinputs.institution.clear();
            jct.chosen.institution = "";
        }
        jct._calculate_if_all_data_provided();
    })

    jct.d.gebi('jct_restart').addEventListener("click", (e) => {
        location.reload();
    })

    let explainResults = jct.d.gebi("jct_explain_results");
    if (explainResults) {
        explainResults.addEventListener("click", (e) => {
            jct.d.toggle_detailed_results();
        })
    }

    // if we've been given URL params, read them then reset the url
    if (manageUrl) {
        let urlParams = new URLSearchParams(window.location.search);
        let setDefault = false;
        if (urlParams.get("issn")) {
            jct.set_each_default('journal', urlParams.get("issn"));
            setDefault = true;
        }
        if (urlParams.get("funder")) {
            jct.set_each_default("funder", urlParams.get("funder"));
            setDefault = true;
        }
        if (urlParams.get("ror")) {
            jct.set_each_default("institution", urlParams.get("ror"));
            setDefault = true;
        }
        if (urlParams.get("not_he") && urlParams.get("not_he") === "true") {
            let not_he_element = jct.d.gebi('jct_notHE');
            if (not_he_element.checked === false) {
                not_he_element.click();
            }
            setDefault = true;
        }
        if (setDefault) {
            window.history.replaceState("", "", "/");
        }
    }

    // finally, bind all the modals on the page
    jct.bindModals();
}
