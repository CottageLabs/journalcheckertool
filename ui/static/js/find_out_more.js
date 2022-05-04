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
