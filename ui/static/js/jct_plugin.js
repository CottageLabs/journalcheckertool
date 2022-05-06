
// -------- i_am_a_widget --------

window.JCT_WIDGET = true;



// -------- api_endpoint --------

window.JCT_API_endpoint = 'https://api.journalcheckertool.org';
window.JCT_UI_BASE_URL = "https://journalcheckertool.org";



// -------- clinput --------

let clinput = {};

clinput.CLInput = class {
    constructor(params) {
        this.timer = null;
        this.delay = params.rateLimit || 0;
        this.value = "";
        this.options_method = params.options;
        this.optionsTemplate = params.optionsTemplate;
        this.selectedTemplate = params.selectedTemplate;
        this.options = [];
        this.id = params.id;
        this.optionsLimit = params.optionsLimit || 0;
        this.element = params.element;
        this.onChoice = params.onChoice;
        this.newValueMethod = params.newValue || false;
        this.selectedObjectToSearchString = params.selectedObjectToSearchString || false
        // this.lastSearchValue = "";
        this.setLastSearchValue("");
        this.selectedObject = false;

        let label = params.label;
        let inputAttrs = params.inputAttributes;

        let attrs = []
        let keys = Object.keys(inputAttrs)
        for (var i = 0; i < keys.length; i++) {
            var key = keys[i];
            var val = inputAttrs[key];
            attrs.push(key + "=\"" + val + "\"");
        }
        let attrsFrag = attrs.join(" ");

        this.element.innerHTML = '<label for="' + this.id + '">' + label + '</label> \
                <input type="text" id="' + this.id + '" name="' + this.id + '" which="' + this.id + '" ' + attrsFrag + '>\
                <div id="' + this.id + '--options"></div>';

        let input = document.getElementById(this.id);
        input.addEventListener("focus", () => {this.activateInput()});
        input.addEventListener("blur", () => {this.recordSearchValue(true)});
        input.addEventListener("keydown", (e) => {
            let entries = document.getElementsByClassName("clinput__option_"+this.id);
            let arrowPress = (code, entries) => {
                if(code === "ArrowDown"){
                    entries[0].focus();
                    e.preventDefault();
                }
            }
            if (entries.length > 0) {
                this._dispatchForCode(event, arrowPress, entries);
            }
        });
    }

    activate() {
        let input = document.getElementById(this.id);
        input.focus();
    }

    setChoice(value, callback) {
        this.value = value;
        this.options_method(value, (data) => {
            this.optionsReceived(data, true)
            if (this.options.length > 0) {
                this.selectedObject = this.options[0];
                this.showSelectedObject();
            }
            callback(this.selectedObject);
        });
    }

    hasChoice() {
        return !!this.selectedObject;
    }

    unsetTimer() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }

    setLastSearchValue(val) {
        this.lastSearchValue = val;
    }

    recordSearchValue(root) {
        let input = document.getElementById(this.id);
        let newVal = input.value;
        if (newVal !== this.lastSearchValue) {
            // this.lastSearchValue = input.value;
            this.setLastSearchValue(input.value);
            this.selectedObject = false;
        }

        if (this.selectedObject) {
            this.showSelectedObject()
        } else {
            this._setInputValue("");
        }
    }

    _setInputValue(val) {
        let input = document.getElementById(this.id);
        input.value = val;
        input.setAttribute("title", val);
    }

    clear() {
        this._setInputValue("");
        this.selectedObject = false;
        // this.lastSearchValue = "";
        this.setLastSearchValue("");
    }

    activateInput() {
        let input = document.getElementById(this.id);
        this._setInputValue(this.lastSearchValue);
        this.value = "";

        if (this.selectedObject) {
            let lsv = this.lastSearchValue.toLowerCase();
            let keys = Object.keys(this.selectedObject);

            if (lsv) {
                keycheck:
                    for (let i = 0; i < keys.length; i++) {
                        let key = keys[i];
                        let v = this.selectedObject[key];
                        if (Array.isArray(v)) {
                            for (var j = 0; j < v.length; j++) {
                                let ve = v[j];
                                if (ve.toLowerCase().includes(lsv)) {
                                    this._setInputValue(ve);
                                    break keycheck;
                                }
                            }
                        } else {
                            if (v && v.toLowerCase().includes(lsv)) {
                                this._setInputValue(v);
                                break keycheck;
                            }
                        }
                    }
            } else {
                if (this.selectedObjectToSearchString) {
                    let ss = this.selectedObjectToSearchString(this.selectedObject);
                    this._setInputValue(ss);
                } else {
                    this._setInputValue(this.selectedObject[keys[0]])
                }
            }
        }

        if (!this.timer) {
            this.timer = window.setInterval(() => {
                this.clearOptions();
                this.lookupOptions();
                // this.unsetTimer();
            }, this.delay);
        }
    }

    clearOptions() {
        let input = document.getElementById(this.id);
        if (document.activeElement === input) {
            return;
        }

        let entries = this.element.getElementsByClassName("clinput__option_" + this.id)
        for (let i = 0; i < entries.length; i++) {
            if (document.activeElement === entries[i]) {
                return;
            }
        }
        document.getElementById(this.id + "--options").innerHTML = "";
    }

    lookupOptions() {
        let input = document.getElementById(this.id);
        if (document.activeElement !== input) {
            return;
        }
        if (this.value !== input.value && input.value.length > 0) {
            this.value = input.value;
            this.options_method(this.value, (data) => {this.optionsReceived(data)});
        } else if (input.value.length === 0) {
            let optsContainer = document.getElementById(this.id + "--options");
            optsContainer.innerHTML = "";
        }
    }

    optionsReceived(data, silent) {
        if (silent === undefined) {
            silent = false;
        }
        if (!this.optionsLimit) {
            this.options = data;
        } else {
            this.options = data.slice(0, this.optionsLimit);
        }
        if (this.newValueMethod && this.options.length === 0) {
            let nv = this.newValueMethod(this.value);
            if (nv) {
                this.options = [nv].concat(this.options);
            }
        }
        if (!silent) {
            this._renderOptions();
        }
    }

    _dispatchForCode(event, callback, entries){
        let code;

        if (event.key !== undefined) {
            code = event.key;
        } else if (event.keyIdentifier !== undefined) {
            code = event.keyIdentifier;
        } else if (event.keyCode !== undefined) {
            code = event.keyCode;
        }

        callback(code, entries);
    };

    _renderOptions() {
        let optsContainer = document.getElementById(this.id + "--options")
        if (this.options.length === 0) {
            optsContainer.innerHTML = "";
            return;
        }

        let frag = "<ul class='clinput__options clinput__options_" + this.id + "'>";
        for (let s = 0; s < this.options.length; s++) {
            frag += '<li tabIndex=' + s + ' class="clinput__option clinput__option_' + this.id + '" data-idx=' + s + '">' + this.optionsTemplate(this.options[s]) + '</li>';
        }
        frag += '</ul>';
        optsContainer.innerHTML = frag;

        let entries = this.element.getElementsByClassName("clinput__option_" + this.id)

        for (let i = 0; i < entries.length; i++) {
            entries[i].addEventListener("mouseover", () => {
                this.setFocusToOption(entries, i);
            });
            entries[i].addEventListener("mouseout", () => {
                this.setFocusToOption(entries, i);
            });
            entries[i].addEventListener("click", (e) => {
                this.chooseOption(e,i);
            });
            entries[i].addEventListener("focus", () => {
                this._setInputValue(this.lastSearchValue);
            });
            entries[i].addEventListener("blur", () => {
                this.recordSearchValue();
            });
            entries[i].addEventListener("keydown", (e) => {
                let arrowPress = (code, entries) => {
                    let idx = parseInt(e.target.getAttribute("data-idx"));
                    if (entries.length !== 0) {
                        if (code === "ArrowDown") {
                            if (idx < entries.length - 1) {
                                entries[idx + 1].focus();
                                e.preventDefault();
                            }
                        } else if (code === "ArrowUp") {
                            this.selecting = true;
                            if (idx > 0) {
                                entries[idx - 1].focus();
                            } else {
                                document.getElementById(this.id).focus();
                            }
                        } else if (code === "Enter") {
                            this.selecting = true;
                            this.chooseOption(e,idx);
                        } else if (code === "Tab") {
                            this.selecting = true;
                            this.chooseOption(e,idx);
                            e.preventDefault();
                        }
                    }
                };
                this._dispatchForCode(event, arrowPress, entries);
            });
        }
    }

    chooseOption(e,idx){
        let input = document.getElementById(this.id);
        let options = document.getElementsByClassName("clinput__options_" + this.id);
        options[0].innerHTML = "";
        // this.lastSearchValue = input.value;
        this.setLastSearchValue(input.value);
        this.selectedObject = this.options[idx];
        this.showSelectedObject();
        // input.blur();
        this.onChoice(e,this.options[idx]);
    }

    setFocusToOption(elements, i){
        if (i < 0) {
            document.getElementById(this.id).focus();
        }
        else if (i < elements.length) {
            elements[i].focus();
        }
    }

    showSelectedObject() {
        this._setInputValue(this.selectedTemplate(this.selectedObject));
    }
}

clinput.init = (params) => {
    return new clinput.CLInput(params)
}


// -------- jct --------

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
        // FIXME: need to make the second and third only replace at the start and the end
        txt = txt.replace(" " + sw + " ", " ").replace(sw + " ", "").replace(" " + sw, "")
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
                // let effective_text = text.toLowerCase().replace(' of','').replace('the ','');
                let effective_text = jct.suggest_prepare(text, ["of", "the", "and", "journa", "journal"])
                effectiveTextLength = effective_text.length
                // text = text.toLowerCase().replace(' of','').replace('the ','');
            }
            if (effectiveTextLength > 3) {
                let ourcb = (xhr) => {
                    let js = JSON.parse(xhr.response);
                    callback(js.data);
                }
                // jct.jx('suggest/journal/'+text, false, ourcb);
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
            text = text.toLowerCase(); //.replace(' of','').replace('the ','');
            if (text.length > 1) {
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



// -------- funders --------

jct.funderlist=[{"country": null, "primary": true, "id": "academyoffinlandaka", "abbr": "AKA", "name": "Academy of Finland"}, {"country": null, "primary": true, "id": "aligningscienceacrossparkinsonsasap", "abbr": "ASAP", "name": "Aligning Science Across Parkinson's"}, {"country": null, "primary": true, "id": "austriansciencefundfwf", "abbr": "FWF", "name": "Austrian Science Fund"}, {"country": null, "primary": true, "id": "billmelindagatesfoundation", "abbr": null, "name": "Bill & Melinda Gates Foundation"}, {"country": null, "primary": true, "id": "europeancommissionhorizoneuropeframeworkprogramme", "abbr": null, "name": "European Commission (Horizon Europe Framework Programme)"}, {"country": "Sweden", "primary": true, "id": "formassweden", "abbr": null, "name": "Formas"}, {"country": "Sweden", "primary": true, "id": "fortesweden", "abbr": null, "name": "FORTE"}, {"country": null, "primary": true, "id": "frenchnationalresearchagencyanr", "abbr": "ANR", "name": "French National Research Agency"}, {"country": "Jordan", "primary": true, "id": "highercouncilforscienceandtechnologyhcstjordan", "abbr": "HCST", "name": "Higher Council for Science and Technology"}, {"country": null, "primary": true, "id": "howardhughesmedicalinstitutehhmi", "abbr": "HHMI", "name": "Howard Hughes Medical Institute"}, {"country": null, "primary": true, "id": "luxembourgnationalresearchfundfnr", "abbr": "FNR", "name": "Luxembourg National Research Fund"}, {"country": "Italy", "primary": true, "id": "nationalinstitutefornuclearphysicsinfnitaly", "abbr": "INFN", "name": "National Institute for Nuclear Physics"}, {"country": "Zambia", "primary": true, "id": "nationalscienceandtechnologycouncilnstczambia", "abbr": "NSTC", "name": "National Science and Technology Council"}, {"country": "Poland", "primary": true, "id": "nationalsciencecentrepolandncn", "abbr": "NCN", "name": "National Science Centre"}, {"country": null, "primary": true, "id": "netherlandsorganisationforscientificresearchnwo", "abbr": "NWO", "name": "Netherlands Organisation for Scientific Research"}, {"country": null, "primary": true, "id": "researchcouncilofnorwayrcn", "abbr": "RCN", "name": "Research Council of Norway"}, {"country": null, "primary": true, "id": "sciencefoundationirelandsfi", "abbr": "SFI", "name": "Science Foundation Ireland"}, {"country": null, "primary": true, "id": "slovenianresearchagencyarrs", "abbr": "ARRS", "name": "Slovenian Research Agency"}, {"country": null, "primary": true, "id": "southafricanmedicalresearchcouncilsamrc", "abbr": "SAMRC", "name": "South African Medical Research Council"}, {"country": null, "primary": true, "id": "specialprogrammeforresearchandtrainingintropicaldiseasestdr", "abbr": "TDR", "name": "Special Programme for Research and Training in Tropical Diseases"}, {"country": null, "primary": true, "id": "templetonworldcharityfoundationtwcf", "abbr": "TWCF", "name": "Templeton World Charity Foundation"}, {"country": null, "primary": true, "id": "unitedkingdomresearchinnovationukri", "abbr": "UKRI", "name": "UK Research and Innovation."}, {"country": null, "primary": false, "id": "unitedkingdomresearchinnovationukri", "abbr": "AHRC (UKRI)", "name": "Arts and Humanities Research Council"}, {"country": null, "primary": false, "id": "unitedkingdomresearchinnovationukri", "abbr": "BBSRC (UKRI)", "name": "Biotechnology and Biological Sciences Research Council"}, {"country": null, "primary": false, "id": "unitedkingdomresearchinnovationukri", "abbr": "ESRC (UKRI)", "name": "Economic and Social Research Council"}, {"country": null, "primary": false, "id": "unitedkingdomresearchinnovationukri", "abbr": "EPSRC (UKRI)", "name": "Engineering and Physical Sciences Research Council"}, {"country": null, "primary": false, "id": "unitedkingdomresearchinnovationukri", "abbr": "UKRI", "name": "Innovate UK"}, {"country": null, "primary": false, "id": "unitedkingdomresearchinnovationukri", "abbr": "MRC (UKRI)", "name": "Medical Research Council"}, {"country": null, "primary": false, "id": "unitedkingdomresearchinnovationukri", "abbr": "NERC (UKRI)", "name": "Natural Environment Research Council"}, {"country": null, "primary": false, "id": "unitedkingdomresearchinnovationukri", "abbr": "UKRI", "name": "Research England"}, {"country": null, "primary": false, "id": "unitedkingdomresearchinnovationukri", "abbr": "STFC (UKRI)", "name": "Science and Technology Facilities Council"}, {"country": "Sweden", "primary": true, "id": "vinnovasweden", "abbr": null, "name": "Vinnova"}, {"country": null, "primary": true, "id": "wellcome", "abbr": null, "name": "Wellcome"}, {"country": null, "primary": true, "id": "worldhealthorganizationwho", "abbr": "WHO", "name": "World Health Organization"}]


// -------- find_out_more --------

jct.get_fom_url = () => {
    let url = jct.host;
    url += "/";

    let jid, fid, iid, not_he = false;
    try {
        jid = jct.chosen.journal.id;
    } catch {}
    try {
        fid = jct.chosen.funder.id;
    } catch {}
    try {
        iid = jct.chosen.institution.id;
    } catch {}
    try {
        not_he = jct.d.gebi('jct_notHE').checked;
    } catch {}

    let args = [];
    if (jid) {
        args.push("issn=" + jid);
    }
    if (fid) {
        args.push("funder=" + fid);
    }
    if (iid) {
        args.push("ror=" + iid);
    }
    if (not_he) {
        args.push("not_he=" + not_he);
    }

    if (args.length > 0) {
        let query = args.join("&");
        url += "?" + query;
    }
    return url;
}

jct.setup_fom_url = () => {
    let fom = jct.d.gebi("jct_find_out_more");
    if (fom) {
        let url = jct.get_fom_url();
        fom.setAttribute("href", url);
    }
}

jct.display_results_url = () => {
    let fom = jct.d.gebi("jct_results_url");
    if (fom) {
        let url = jct.get_fom_url();
        fom.innerText = url;
    }
}

jct.copy_results_url = () => {
    let share_url = jct.d.gebi("jct_results_url");
    if (share_url) {
        navigator.clipboard.writeText(share_url.innerText)
    }
}



// -------- feedback --------

jct.site_modals.feedback = {
    title: `Feedback? Suggestion? Contact us here.`,
    body: `<p>This tool is delivered by <a href="https://cottagelabs.com/" target="_blank" rel="noopener">
        Cottage Labs</a> on behalf of <a href="https://www.coalition-s.org/" target="_blank" rel="noopener">cOAlition S</a>. </p>
        <p>If you believe that there is an error in the result given by the tool or how the tool is functioning 
        please use this form. Your current search details will be automatically included in your feedback. 
        We will respond within 3 working days.</p>
        <form id="contact_form">
            <div class="modal-inputs">
                <label for="name">Name</label>
                <input class="contact_input" type="text" id="name" name="name" placeholder="Your name..">
            </div>
            <div class="modal-inputs">
                <label for="email">Email</label>
                <input class="contact_input" type="email" id="email" name="email" placeholder="Your email..">
            </div>
            <div class="modal-inputs">
                <label for="message">Comment</label>
                <textarea class="contact_input" id="message" name="message" placeholder="Write something.."></textarea>
            </div>
            <div class="modal-inputs">
                <button class="button button--primary contact_submit" type="submit">
                    <svg width="24" height="25" viewbox="0 0 24 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M4.88002 24.4048C4.99391 24.4685 5.11979 24.5 
                        5.24492 24.5C5.4165 24.5 5.58734 24.4416 5.72445 24.3269L10.9109 20.0044H14.2242C19.6018 20.0044 
                        23.9768 15.6286 23.9768 10.2518C23.9768 4.87501 19.6018 0.5 14.225 0.5H9.75255C4.37501 0.5 0 
                        4.87501 0 10.2518C0 13.8438 2.01854 17.1609 5.18872 18.8527L4.50389 23.6443C4.45968 23.9523 
                        4.60953 24.2542 4.88002 24.4048ZM1.49855 10.2518C1.49855 5.70071 5.20071 1.99855 9.75255 
                        1.99855H14.2242C18.7761 1.99855 22.4782 5.69996 22.4782 10.2518C22.4782 14.8036 18.7761 
                        18.5058 14.2242 18.5058H10.6397C10.4644 18.5058 10.295 18.5672 10.1602 18.6789L6.26243 21.9277L6.74721 
                        18.5298C6.79442 18.2016 6.62059 17.8824 6.32013 17.7438C3.39122 16.3891 1.49855 13.449 1.49855 
                        10.2518ZM6.74347 8.01597H17.2333C17.6477 8.01597 17.9826 7.6803 17.9826 7.2667C17.9826 6.8531 
                        17.6477 6.51743 17.2333 6.51743H6.74347C6.32987 6.51743 5.99419 6.8531 5.99419 7.2667C5.99419 
                        7.6803 6.32987 8.01597 6.74347 8.01597ZM6.74347 14.0102H12.7377C13.152 14.0102 13.4869 13.6752 
                        13.4869 13.2609C13.4869 12.8473 13.152 12.5116 12.7377 12.5116H6.74347C6.32987 12.5116 5.99419 
                        12.8473 5.99419 13.2609C5.99419 13.6752 6.32987 14.0102 6.74347 14.0102ZM17.2333 11.0131H6.74347C6.32987 
                        11.0131 5.99419 10.6774 5.99419 10.2638C5.99419 9.8502 6.32987 9.51452 6.74347 9.51452H17.2333C17.6477 
                        9.51452 17.9826 9.8502 17.9826 10.2638C17.9826 10.6774 17.6477 11.0131 17.2333 11.0131Z" fill="black"></path>
                    </svg>
                    Send
                </button>
            </div>
        </form>
        <div id="feedback_success" style="display: none;"><h1>Email sent successfully.</h1></div>
        <div id="feedback_error" style="display: none;"><h1>Ooops, something went wrong.</h1></div>
        <p>
            <a href="/notices#privacy_notice">Privacy Notice</a> •
            <a href="/notices#disclaimer_and_copyright">Disclaimer & Copyright</a>
        </p>` // Feedback modal uses generic id names. If embedding in the plugin, need to change id names
}

jct.modal_setup.feedback = () => {
    // WARNING: Feedback modal uses generic id names. If embedding in the plugin, need to change id names
    jct.d.gebi("contact_form")
        .addEventListener("submit", (event) => {
            event.preventDefault()
        let name  = jct.d.gebi("name").value;
        let email = jct.d.gebi("email").value;
        let message = jct.d.gebi("message").value;
        let timestamp = new Date().toUTCString()

        let data =
            JSON.stringify({
                "name" : name,
                "email" : email,
                "feedback" : message,
                "context" : {
                    "request" : {
                        "timestamp" : timestamp,
                        "issn" : jct.chosen.journal ? jct.chosen.journal.id : "",
                        "funder" : jct.chosen.funder ? jct.chosen.funder.id : "",
                        "ror" : jct.chosen.institution ? jct.chosen.institution.id : "",
                        "navigator data": {
                            "appCodeName": navigator.appCodeName,
                            "appName": navigator.appName,
                            "appVersion": navigator.appVersion,
                            "cookieEnabled": navigator.cookieEnabled,
                            "language": navigator.language,
                            "platform": navigator.platform,
                            "userAgent": navigator.userAgent,
                            "vendor": navigator.vendor
                        }
                    },
                    "results" : [
                        jct.latest_response
                    ],
                    "url" : jct.get_fom_url()
                }
            });

        let xhr = new XMLHttpRequest();
        xhr.open('POST', jct.api + '/feedback');
        xhr.onload = () => {
            alert("message sent successfully")
            //jct.d.gebi("feedback_success").style.display = "block"
        };
        xhr.onerror = () => {
            //jct.d.gebi("feedback_error").style.display = "block"
            alert("Oops, something went wrong");
        };
        xhr.setRequestHeader('Content-type', 'application/json');
        xhr.send(data);
        jct.closeModal();
        return false
    });
}




// -------- plugin --------


// ----------------------------------------
// Function to add plugin containers
// ----------------------------------------
jct.add_plugin_containers = () => {
    // ----------------------------------------
    // html for holding the query
    // ----------------------------------------
    let query_container_html = `
        <div class="query" id="jct_query">
            <div class="header-logo">
                <h2 class="label">
                    <svg width="13" height="20" viewbox="0 0 13 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M6.28479 2.14158C5.43898 2.14158 4.62781 2.47934 4.02973 3.08057C3.43165 3.6818 3.09564 4.49725 3.09564 5.34752V6.07785H0.965235V5.34752C0.965235 3.92928 1.52568 2.56912 2.52329 1.56626C3.5209 0.563403 4.87395 0 6.28479 0C7.69562 0 9.04868 0.563403 10.0463 1.56626C11.0439 2.56912 11.6043 3.92928 11.6043 5.34752V10.3707C12.2009 11.3357 12.5455 12.4746 12.5455 13.6944C12.5455 17.1769 9.73706 20 6.27273 20C2.8084 20 0 17.1769 0 13.6944C0 10.2119 2.8084 7.38877 6.27273 7.38877C7.44213 7.38877 8.5368 7.71045 9.47393 8.27058V5.34752C9.47393 4.49725 9.13793 3.6818 8.53984 3.08057C7.94176 2.47934 7.13059 2.14158 6.28479 2.14158ZM6.27273 9.53034C3.98499 9.53034 2.13041 11.3946 2.13041 13.6944C2.13041 15.9941 3.98499 17.8584 6.27273 17.8584C8.56047 17.8584 10.415 15.9941 10.415 13.6944C10.415 11.3946 8.56047 9.53034 6.27273 9.53034Z" fill="#F47115"></path>
                        <path d="M6.29321 15.4802C7.26388 15.4802 8.05077 14.6892 8.05077 13.7134C8.05077 12.7376 7.26388 11.9466 6.29321 11.9466C5.32254 11.9466 4.53566 12.7376 4.53566 13.7134C4.53566 14.6892 5.32254 15.4802 6.29321 15.4802Z" fill="#F47115"></path>
                    </svg>
                    <a href="https://journalcheckertool.org">cOAlition S: Journal Checker Tool</a>
                </h2>
            </div>
            <div class="row row-inputs" id="jct_inputs_plugin"></div>
        </div>
    `;

    // ----------------------------------------
    // html for holding the result
    // ----------------------------------------
    let results_container_html = `
        <div class="container results" id="jct_results" style="display: none">
            <div id="jct_results_plugin"></div>
            <div id="jct_tiles_plugin"></div>
            <div class="row">
                <div class="col col--1of2 col--centered">
                    <a href="#" class="button button--secondary" id="jct_find_out_more" target="_blank">Find out more</a>
                </div>
                <div class="col col--2of2 col--centered">
                    <button class="button button--primary" id="jct_restart">
                        <svg width="30" height="25" viewBox="0 0 30 25" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M1.57592 9.07816L2.94589 10.4481C3.92217 4.80549 8.85311 0.5 14.7704 0.5C18.2125 0.5 21.4922 1.98062 23.7704 4.56246C24.1073 4.94462 24.0713 5.528 23.6891 5.86585C23.3079 6.20277 22.7245 6.16677 22.3857 5.78462C20.4584 3.59877 17.6817 2.34615 14.7704 2.34615C9.70014 2.34615 5.48545 6.08244 4.73523 10.9461L6.97131 9.8277C7.42823 9.5997 7.98208 9.78431 8.21008 10.2403C8.43808 10.6963 8.25346 11.2511 7.79746 11.4791L4.14234 13.3066C4.01456 13.3779 3.86813 13.4198 3.71225 13.4229L3.69346 13.4231C3.59256 13.4231 3.49231 13.4066 3.39684 13.3743C3.26521 13.3298 3.14264 13.2553 3.03992 13.1526L0.270692 10.3834C-0.0902308 10.0225 -0.0902308 9.43908 0.270692 9.07816C0.631615 8.71724 1.215 8.71724 1.57592 9.07816ZM5.77034 20.4385C8.04942 23.0194 11.3291 24.5 14.7703 24.5C20.6873 24.5 25.6181 20.1949 26.5947 14.5526L27.964 15.9218C28.144 16.1018 28.3803 16.1923 28.6166 16.1923C28.8529 16.1923 29.0892 16.1018 29.2692 15.9228C29.6301 15.5618 29.6301 14.9785 29.2692 14.6175L26.5271 11.8754C26.3584 11.6919 26.1165 11.5769 25.8473 11.5769C25.6855 11.5769 25.5336 11.6185 25.4015 11.6914L21.7424 13.5209C21.2864 13.7489 21.1018 14.3037 21.3298 14.7597C21.5587 15.2157 22.1135 15.3985 22.5686 15.1723L24.8055 14.0535C24.0555 18.9173 19.8407 22.6538 14.7703 22.6538C11.859 22.6538 9.08326 21.4012 7.15403 19.2163C6.81711 18.8351 6.23372 18.7972 5.85157 19.1351C5.46942 19.472 5.43249 20.0563 5.77034 20.4385Z" fill="#2B2B2B"/>
                        </svg>Start over
                    </button>
                </div>
            </div>
            <section class="row row--centered">
                <p class="col col--1of2 alert">
                  The information provided by the <em>Journal Checker Tool</em> represents cOAlition S’s current
                  understanding in relation to the policies of the journals contained within it. We will endeavour to
                  keep it up to date and accurate, but we do not accept any liability in relation to any errors or omissions.
                </p>
            </section>
        </div>
    `;

    // ----------------------------------------
    // html for holding the modals
    // ----------------------------------------
    let modal_container_html = `
        <div id="jct_modal_container"></div>
    `;

    let plugin_div = jct.d.gebi("jct_plugin");
    if (plugin_div.children.length === 0) {
        plugin_div.innerHTML = query_container_html + results_container_html + modal_container_html;
    }
}

// ----------------------------------------
// Function to initialize the plugin with values
// ----------------------------------------
jct.set_defaults = () => {
    if (jct_query_options && jct_query_options.journal) {
        jct.set_each_default('journal', jct_query_options.journal);
    }
    if (jct_query_options && jct_query_options.funder) {
        jct.set_each_default('funder', jct_query_options.funder);
    }
    if (jct_query_options && jct_query_options.not_he) {
        let not_he_element = jct.d.gebi('jct_notHE');
        if (not_he_element.checked === false) {
            not_he_element.click();
        }
    } else if (jct_query_options && jct_query_options.institution) {
        jct.set_each_default('institution', jct_query_options.institution);
    }
}

// ----------------------------------------
// Function to setup the plugin
// ----------------------------------------
jct.setup_plugin = () => {
    jct.add_plugin_containers();
    jct.setup(false);
    jct.set_defaults();
}


