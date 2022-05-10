jct.site_modals.share_results = {
    title: "Share this result",
    body: `<p>To share this result, copy the following link
            <button class="button button--primary" style="float: right;" onClick="jct.copy_results_url()">Copy</button>
        </p>
        <p id="jct_results_url"></p>`
}

jct.explain = (q) => {
    // start by clearing anything that was in the explain section before
    let detailed_results = jct.d.gebi("jct_detailed_results_section")
    detailed_results.innerHTML = "";

    let yq = jct._yourQuery(q);
    let ways = jct._renderWays(q);
    let routes = jct._renderRoutes(q);

    let routesText = jct._serialiseRoutes(routes);

    let elem = jct.htmlToElement(`<div id='jct_detailed_result_text'>${yq} <hr> ${ways} ${routesText}</div>`);
    detailed_results.append(elem);

    jct._resultPrint();
}

jct.explain_card = (q, cardId) => {
    let yq = jct._yourQuery(q);
    let way = jct.lang.cards[cardId].explain.text;

    let card = false;
    for (let i = 0; i < q.cards.length; i++) {
        if (q.cards[i].id === cardId) {
            card = q.cards[i];
            break;
        }
    }

    let interestingRoutes = [];
    if (card.match_routes) {
        if (card.match_routes.must) {
            interestingRoutes = interestingRoutes.concat(card.match_routes.must);
        }
        if (card.match_routes.or) {
            interestingRoutes = interestingRoutes.concat(card.match_routes.or);
        }
        if (card.match_routes.not) {
            interestingRoutes = interestingRoutes.concat(card.match_routes.not);
        }
    }

    let routes = jct._renderRoutes(q, interestingRoutes);
    let routesText = jct._serialiseRoutes(routes);

    return `${way} ${yq} ${routesText}`;
}

jct._serialiseRoutes = (routes) => {
    let compliant = "";
    if (routes.compliant.length > 0) {
        compliant = `<hr><h2>${jct.lang.explain.supporting_data.compliant_routes}</h2>` + routes.compliant.join("");
    }

    let non_compliant = "";
    if (routes.non_compliant.length > 0) {
        non_compliant = `<hr><h2>${jct.lang.explain.supporting_data.non_compliant_routes}</h2>` + routes.non_compliant.join("");
    }

    let unknown = "";
    if (routes.unknown.length > 0) {
        unknown = `<hr><h2>${jct.lang.explain.supporting_data.unknown_routes}</h2>` + routes.unknown.join("");
    }

    return `${compliant} ${non_compliant} ${unknown}`
}

jct._resultPrint = () => {
    let print = jct.d.gebi('jct_print');
    if (print) {
        print.addEventListener("click", () => {
            let a = window.open('', '', 'height=500, width=500');
            let compliance = jct.d.gebc("jct_compliance")[0];
            let results_to_print = jct.d.gebi("jct_detailed_result_text");
            let share_url = jct.d.gebi("jct_results_url");
            let share_text = ''
            if (share_url) {
                share_text = `To view these results, visit <a href="`+ share_url.innerHTML +`">`+ share_url.innerHTML + `</a>`
            }
            a.document.write(compliance.innerHTML);
            a.document.write(results_to_print.innerHTML);
            a.document.write(share_text);
            a.document.close();
            a.print();
        })
    }
}

jct._renderWay = (cardId) => {
    let wayTitle = jct.lang.cards[cardId].explain.title;
    let wayText = jct.lang.cards[cardId].explain.text;
    return `<h3>${wayTitle}</h3>
            <p>${wayText}</p>`;
}

jct._renderWays = (q) => {
    let title = jct.lang.explain.ways_to_comply.title;
    let intro = jct.lang.explain.ways_to_comply.text;

    let ways = `<h2>${title}</h2>
                <p>${intro}</p>`;

    let compliantCount = 0;
    let cardsToDisplay = q.cards;
    for (let i = 0; i < cardsToDisplay.length; i++) {
        let card = cardsToDisplay[i];
        if (!card.compliant) {
            continue
        }
        compliantCount++;
        ways += jct._renderWay(card.id);
    }

    if (compliantCount === 0) {
        ways += "<p><em>" + jct.lang.explain.ways_to_comply.none + "</em></p>";
    }

    return ways;
}

jct._renderRoutes = (q, include) => {
    let response = {
        compliant: [],
        non_compliant: [],
        unknown: []
    }
    q.results.forEach((r) => {
        if (include && !include.includes(r.route)) {
            return;
        }

        let name = jct.lang.explain.routes[r.route].label;
        let statement = jct.lang.explain.routes[r.route][r.compliant].statement;
        let explanation = jct.lang.explain.routes[r.route][r.compliant].explanation;
        let qualification = jct.get_qualifications(r.qualifications);
        let route = `<h3>` + name + `</h3>` +
            `<p>`  + statement + `</p>` +
            `<p>`  + qualification + `</p>` +
            `<p>`  + explanation + `</p>`;

        let is_in_doaj = jct.is_in_doaj(r.route, r.log);
        let is_in_progress_doaj = jct.is_in_progress_doaj(r.route, r.log);
        if (r.log) {
            let route_defined = r.route in jct.lang.api_codes.logs;
            r.log.forEach((log) => {
                let action = log.code;
                // FIXME: these seem very specific, I don't think they should be here, but I need
                // to understand them before I can factor them out
                if (is_in_doaj && action === 'FullOA.NotInProgressDOAJ') {
                    return;
                }
                if (is_in_progress_doaj && action === 'FullOA.NotInDOAJ') {
                    return;
                }
                if (route_defined && log.code in jct.lang.api_codes.logs[r.route]) {
                    action = jct.lang.api_codes.logs[r.route][log.code];
                }
                let parameters = ''
                if (log.parameters) {
                    for (let [parameter,values] of Object.entries(log.parameters)) {
                        let parent_key = log.code + '.Properties';
                        if (route_defined && parent_key in jct.lang.api_codes.logs[r.route] &&
                            parameter in jct.lang.api_codes.logs[r.route][parent_key] &&
                            jct.lang.api_codes.logs[r.route][parent_key][parameter]) {
                            // The key is displayed irrespective of the value existing
                            parameters += jct.lang.api_codes.logs[r.route][parent_key][parameter] + "<br/>";
                        }

                        if (values && values.length > 0) {
                            parameters += "<ul>";
                            values.forEach((value) => {
                                if (parameter === 'version') {
                                    value = jct.version_rename(value);
                                }
                                parameters += "<li>" + value + "</li>";
                            })
                            parameters += "</ul>";
                        }
                    }
                }
                route += "<ul><li>" + action + "</li>";
                route += parameters;
                route += "</ul>";
            })
        }

        if (r.compliant === "yes") {
            response.compliant.push(route);
        } else if (r.compliant === "no") {
            response.non_compliant.push(route);
        } else {
            response.unknown.push(route);
        }
    });

    return response;
}

jct._yourQuery = (q) => {
    let compliant_count = 0;
    let non_compliant_count = 0;
    let unknown_count = 0;

    for (let i = 0; i < q.results.length; i++) {
        let result = q.results[i];
        if (result.compliant === "yes") {
            compliant_count++;
        } else if (result.compliant === "no") {
            non_compliant_count++;
        } else {
            unknown_count++;
        }
    }

    let issns = jct.chosen.journal.issns.join(", ");
    let publisher = jct.chosen.journal.publisher !== undefined ? jct.chosen.journal.publisher : jct.lang.explain.your_query.publisher_not_known;

    let journal = jct.lang.explain.your_query.journal_title_unknown;
    if (jct.chosen.journal.title) {
        journal = jct.chosen.journal.title;
    }
    journal += " (ISSN: " + issns + ")";

    let text = `<h3>${jct.lang.explain.your_query.title}</h3>
        <p>${jct.lang.explain.your_query.text}
        <ul>
            <li>${jct.lang.explain.your_query.journal_label}: </li>
            <ul class="second">
                <li> ` + journal + `</li>
                <li> ${jct.lang.explain.your_query.publisher_label}: ` + publisher + `</li>
            </ul>
            <li>${jct.lang.explain.your_query.funder_label}: ` + jct.chosen.funder.name + `</li>`

    if (jct.chosen.institution){
        let inner_text = `${jct.lang.explain.your_query.institution_label}: ` + jct.chosen.institution.title;
        if (jct.chosen.institution.alternate && !(/^[a-zA-Z0-9 ]+$/.test(jct.chosen.institution.alternate))) {
            inner_text += ' (' + jct.chosen.institution.alternate + ')';
        }
        if (jct.chosen.institution.country) {
            inner_text += ', ' + jct.chosen.institution.country;
        }
        if (jct.chosen.institution.id) {
            inner_text += ' (ROR: ' + jct.chosen.institution.id + ')';
        }
        text += `<li>` + inner_text + `</li>`
    }
    else {
        text += `<li>${jct.lang.explain.your_query.unaffiliated}</li>`
    }

    let statement = jct.lang.explain.your_query.statement;
    statement = statement.replace("{date}", new Date(q.request.started).toUTCString());
    statement = statement.replace("{compliant}", compliant_count);
    statement = statement.replace("{compliant_plural}", compliant_count !== 1 ? "s" : "");
    statement = statement.replace("{non_compliant}", non_compliant_count);
    statement = statement.replace("{non_compliant_plural}", non_compliant_count !== 1 ? "s" : "");
    statement = statement.replace("{unknown}", unknown_count);
    statement = statement.replace("{unknown_plural}", unknown_count !== 1 ? "s" : "");

    text += `</ul>${statement}</p>`;
    return text;
}

jct.modal_setup.share_results = function () {
    jct.display_results_url();
}

jct.get_qualifications = (qualifications) => {
    let qualification = '';
    if ((typeof qualifications !== "undefined") && qualifications.length > 0) {
        for (let [key,values] of Object.entries(qualifications[0])) {
            if (key in jct.lang.api_codes.qualifications && 'description' in jct.lang.api_codes.qualifications[key]) {
                qualification = jct.lang.api_codes.qualifications[key]['description'] + "<br/>";
                if (values) {
                    for (let [k2,v2] of Object.entries(values)) {
                        if (v2) {
                            let label = k2;
                            if (key in jct.lang.api_codes.qualifications && k2 in jct.lang.api_codes.qualifications[key]) {
                                label = jct.lang.api_codes.qualifications[key][k2]
                            }
                            qualification += label + ' ' + v2 + "<br/>";
                        }
                    }
                }
            }
        }
    }
    if (qualification) {
        return `<p>` + jct.lang.explain.supporting_data.qualifications_prefix + ` ` + qualification + `</p>`;
    }
    return qualification
}

jct.is_in_doaj = (route, logs) => {
    if (route !== 'fully_oa') { return false }
    let is_in = false;
    logs.forEach((log) => {
        if (log.code === 'FullOA.InDOAJ') {
            is_in = true;
        }
    })
    return is_in
}

jct.is_in_progress_doaj = (route, logs) => {
    if (route !== 'fully_oa') { return false }
    let is_in = false;
    logs.forEach((log) => {
        if (log.code === 'FullOA.InProgressDOAJ') {
            is_in = true;
        }
    })
    return is_in
}

jct.version_rename = (val) => {
    let new_val;
    switch(val) {
        case "publishedVersion":
            new_val = jct.lang.explain.versions.publishedVersion;
            break;
        case "acceptedVersion":
            new_val = jct.lang.explain.versions.acceptedVersion;
            break;
        case "submittedVersion":
            new_val = jct.lang.explain.versions.submittedVersion;
            break;
        default:
            new_val = val;
   }
   return new_val
}
