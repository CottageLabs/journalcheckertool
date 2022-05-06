let devui = {};

devui.lang = {"icons": {"fully_oa": "<span class=\"card__icon\"> <svg width=\"16\" height=\"22\" viewBox=\"0 0 16 22\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"> <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M2.75 4.8125V8.9375H1.71531C0.769312 8.9375 0 9.70681 0 10.6528V20.2806C0 21.2286 0.771375 22 1.71875 22H13.4056C14.3536 22 15.125 21.2286 15.125 20.2806V10.6528C15.125 9.70681 14.3557 8.9375 13.4097 8.9375H4.125V4.8125C4.125 2.91706 5.66706 1.375 7.5625 1.375C9.45794 1.375 11 2.91706 11 4.8125V6.1875C11 6.567 11.3073 6.875 11.6875 6.875C12.0677 6.875 12.375 6.567 12.375 6.1875V4.8125C12.375 2.15875 10.2156 0 7.5625 0C4.90875 0 2.75 2.15875 2.75 4.8125ZM1.71531 10.3125C1.52762 10.3125 1.375 10.4651 1.375 10.6528V20.2806C1.375 20.4703 1.52969 20.625 1.71875 20.625H13.4056C13.5953 20.625 13.75 20.4703 13.75 20.2806V10.6528C13.75 10.4651 13.5974 10.3125 13.4097 10.3125H1.71531ZM6.875 17.1875C6.875 17.5677 7.183 17.875 7.5625 17.875C7.942 17.875 8.25 17.5677 8.25 17.1875V13.75C8.25 13.3698 7.942 13.0625 7.5625 13.0625C7.183 13.0625 6.875 13.3698 6.875 13.75V17.1875Z\" fill=\"black\"></path> </svg> </span>", "tj": "<span class=\"card__icon\"> <svg width=\"22\" height=\"22\" viewbox=\"0 0 22 22\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"> <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M10.3125 21.3125C10.3125 21.6927 10.6205 22 11 22C11.3795 22 11.6875 21.6927 11.6875 21.3125V0.6875C11.6875 0.308 11.3795 0 11 0C10.6205 0 10.3125 0.308 10.3125 0.6875V21.3125ZM8.25 19.25H1.71737C0.770687 19.25 0 18.4793 0 17.5326V4.455C0 3.51519 0.765188 2.75 1.705 2.75H8.18744C8.56694 2.75 8.87494 3.058 8.87494 3.4375C8.87494 3.817 8.56694 4.125 8.18744 4.125H1.705C1.52281 4.125 1.375 4.27281 1.375 4.455V17.5319C1.375 17.7176 1.53175 17.875 1.71737 17.875H8.25C8.6295 17.875 8.9375 18.1823 8.9375 18.5625C8.9375 18.9427 8.6295 19.25 8.25 19.25ZM19.3118 18.5625C19.3118 18.1844 19.6211 17.875 19.9993 17.875C20.3774 17.875 20.6868 18.1844 20.6868 18.5625C20.6868 18.9406 20.3774 19.25 19.9993 19.25C19.6211 19.25 19.3118 18.9406 19.3118 18.5625ZM17.2493 18.5625C17.2493 18.1844 17.5586 17.875 17.9368 17.875C18.3149 17.875 18.6243 18.1844 18.6243 18.5625C18.6243 18.9406 18.3149 19.25 17.9368 19.25C17.5586 19.25 17.2493 18.9406 17.2493 18.5625ZM15.1868 18.5625C15.1868 18.1844 15.4961 17.875 15.8743 17.875C16.2524 17.875 16.5618 18.1844 16.5618 18.5625C16.5618 18.9406 16.2524 19.25 15.8743 19.25C15.4961 19.25 15.1868 18.9406 15.1868 18.5625ZM13.1243 18.5625C13.1243 18.1844 13.4336 17.875 13.8118 17.875C14.1899 17.875 14.4993 18.1844 14.4993 18.5625C14.4993 18.9406 14.1899 19.25 13.8118 19.25C13.4336 19.25 13.1243 18.9406 13.1243 18.5625ZM20.6249 17.3731C20.6249 16.995 20.9343 16.6856 21.3124 16.6856C21.6905 16.6856 21.9999 16.995 21.9999 17.3731C21.9999 17.7588 21.6905 18.0606 21.3124 18.0606C20.9343 18.0606 20.6249 17.7581 20.6249 17.3731ZM20.6249 15.3106C20.6249 14.9325 20.9343 14.6231 21.3124 14.6231C21.6905 14.6231 21.9999 14.9325 21.9999 15.3106C21.9999 15.6963 21.6905 15.9981 21.3124 15.9981C20.9343 15.9981 20.6249 15.6956 20.6249 15.3106ZM20.6249 13.2481C20.6249 12.87 20.9343 12.5606 21.3124 12.5606C21.6905 12.5606 21.9999 12.87 21.9999 13.2481C21.9999 13.6338 21.6905 13.9356 21.3124 13.9356C20.9343 13.9356 20.6249 13.6331 20.6249 13.2481ZM20.6249 11.1925C20.6249 10.8075 20.9343 10.4981 21.3124 10.4981C21.6905 10.4981 21.9999 10.8075 21.9999 11.1925C21.9999 11.5706 21.6905 11.8731 21.3124 11.8731C20.9343 11.8731 20.6249 11.5706 20.6249 11.1925ZM20.6249 9.12313C20.6249 8.745 20.9343 8.4425 21.3124 8.4425C21.6905 8.4425 21.9999 8.745 21.9999 9.12313C21.9999 9.50813 21.6905 9.8175 21.3124 9.8175C20.9343 9.8175 20.6249 9.50813 20.6249 9.12313ZM20.6249 7.0675C20.6249 6.6825 20.9343 6.37313 21.3124 6.37313C21.6905 6.37313 21.9999 6.6825 21.9999 7.0675C21.9999 7.44562 21.6905 7.74813 21.3124 7.74813C20.9343 7.74813 20.6249 7.44562 20.6249 7.0675ZM20.6249 4.99813C20.6249 4.62 20.9343 4.3175 21.3124 4.3175C21.6905 4.3175 21.9999 4.62 21.9999 4.99813C21.9999 5.38312 21.6905 5.6925 21.3124 5.6925C20.9343 5.6925 20.6249 5.38312 20.6249 4.99813ZM20.3155 4.125H20.3086C19.9305 4.09062 19.6555 3.76063 19.683 3.3825C19.7174 3.00437 20.0474 2.7225 20.4324 2.75688H20.4255C20.8036 2.79125 21.0855 3.12125 21.058 3.49938C21.0236 3.85688 20.728 4.13188 20.3705 4.13188C20.359 4.13188 20.3473 4.12974 20.337 4.12785C20.3287 4.12635 20.3213 4.125 20.3155 4.125ZM17.6205 3.4375C17.6205 3.05938 17.9299 2.75 18.308 2.75C18.6861 2.75 18.9955 3.05938 18.9955 3.4375C18.9955 3.81562 18.6861 4.125 18.308 4.125C17.9299 4.125 17.6205 3.81562 17.6205 3.4375ZM15.558 3.4375C15.558 3.05938 15.8674 2.75 16.2455 2.75C16.6236 2.75 16.933 3.05938 16.933 3.4375C16.933 3.81562 16.6236 4.125 16.2455 4.125C15.8674 4.125 15.558 3.81562 15.558 3.4375ZM13.4955 3.4375C13.4955 3.05938 13.8049 2.75 14.183 2.75C14.5611 2.75 14.8705 3.05938 14.8705 3.4375C14.8705 3.81562 14.5611 4.125 14.183 4.125C13.8049 4.125 13.4955 3.81562 13.4955 3.4375Z\" fill=\"black\"> </path> </svg> </span>", "self_archiving": "<span class=\"card__icon\"> <svg width=\"22\" height=\"22\" viewbox=\"0 0 22 22\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"> <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M22 5.15831C22 5.98803 21.4085 6.68203 20.625 6.84086V20.2778C20.625 21.2273 19.8523 22 18.9028 22H3.09719C2.14775 22 1.375 21.2273 1.375 20.2778V6.84086C0.591483 6.68203 0 5.98803 0 5.15831V1.71669C0 0.77 0.77 0 1.71669 0H20.2833C21.23 0 22 0.77 22 1.71669V5.15831ZM20.2833 5.5H19.9375H2.0625H1.71669C1.52831 5.5 1.375 5.34669 1.375 5.15831V1.71669C1.375 1.52831 1.52831 1.375 1.71669 1.375H20.2833C20.4717 1.375 20.625 1.52831 20.625 1.71669V5.15831C20.625 5.34669 20.4717 5.5 20.2833 5.5ZM2.75 20.2778V6.875H19.25V20.2778C19.25 20.4689 19.0939 20.625 18.9028 20.625H3.09719C2.90606 20.625 2.75 20.4689 2.75 20.2778ZM7.5625 11H14.4375C14.8177 11 15.125 10.692 15.125 10.3125C15.125 9.933 14.8177 9.625 14.4375 9.625H7.5625C7.183 9.625 6.875 9.933 6.875 10.3125C6.875 10.692 7.183 11 7.5625 11Z\" fill=\"black\"> </path> </svg> </span>", "ta": "<span class=\"card__icon\"> <svg width=\"22\" height=\"22\" viewbox=\"0 0 22 22\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"> <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M0 4.8125C0 5.192 0.308 5.5 0.6875 5.5H4.125V17.1875V19.25C4.125 20.7666 5.35838 22 6.875 22H19.25C20.7666 22 22 20.7666 22 19.25V17.1875C22 16.8073 21.6927 16.5 21.3125 16.5H19.25V2.75C19.25 1.23337 18.0166 0 16.5 0H2.75C1.23337 0 0 1.23337 0 2.75V4.8125ZM17.875 2.75C17.875 1.99169 17.2583 1.375 16.5 1.375H5.13107C5.36564 1.7797 5.5 2.24942 5.5 2.75V4.8125V17.1875V19.25C5.5 20.0083 6.11669 20.625 6.875 20.625C7.63331 20.625 8.25 20.0083 8.25 19.25V17.1875C8.25 16.8073 8.558 16.5 8.9375 16.5H17.875V2.75ZM9.625 17.875H18.5625H20.625V19.25C20.625 20.0083 20.0083 20.625 19.25 20.625H9.25607C9.49064 20.2203 9.625 19.7506 9.625 19.25V17.875ZM1.375 2.75C1.375 1.99169 1.99169 1.375 2.75 1.375C3.50831 1.375 4.125 1.99169 4.125 2.75V4.125H1.375V2.75ZM15.8125 5.5H7.5625C7.183 5.5 6.875 5.192 6.875 4.8125C6.875 4.433 7.183 4.125 7.5625 4.125H15.8125C16.1927 4.125 16.5 4.433 16.5 4.8125C16.5 5.192 16.1927 5.5 15.8125 5.5ZM7.5625 8.25H15.8125C16.1927 8.25 16.5 7.942 16.5 7.5625C16.5 7.183 16.1927 6.875 15.8125 6.875H7.5625C7.183 6.875 6.875 7.183 6.875 7.5625C6.875 7.942 7.183 8.25 7.5625 8.25ZM15.8125 11H7.5625C7.183 11 6.875 10.692 6.875 10.3125C6.875 9.933 7.183 9.625 7.5625 9.625H15.8125C16.1927 9.625 16.5 9.933 16.5 10.3125C16.5 10.692 16.1927 11 15.8125 11ZM7.5625 13.75H11.6875C12.0677 13.75 12.375 13.4427 12.375 13.0625C12.375 12.6823 12.0677 12.375 11.6875 12.375H7.5625C7.183 12.375 6.875 12.6823 6.875 13.0625C6.875 13.4427 7.183 13.75 7.5625 13.75Z\" fill=\"black\"> </path> </svg> </span>"}, "explain": {"supporting_data": {"non_compliant_routes": "Non-Compliant Routes", "qualifications_prefix": "Please note, ", "title": "Data Supporting your Ways to Comply", "compliant_routes": "Compliant Routes", "text": "This section tells you about the routes that support your ways to compliance", "unknown_routes": "Unknown Routes"}, "versions": {"publishedVersion": "Published version", "submittedVersion": "Submitted version", "acceptedVersion": "Accepted version"}, "qualification_match": {"not": "None of the following qualifications must be present:", "or": "At least one of the following qualifications must be present:", "must": "The following qualifications must be present:"}, "qualifications": {"self_archiving.rights_retention_author_advice": "RR Author Advice (need wording for this)", "fully_oa.doaj_under_review": "Under review at DOAJ", "ta.corresponding_authors": "TA is only open to corresponding authors"}, "ways_to_comply": {"text": "This section tells you about your ways to comply with your funder's Open Access policies", "none": "There are no ways to comply with your funder's policy", "title": "Ways to Comply"}, "route_match": {"not": "None of the following routes must be compliant:", "or": "At least one of the following routes must be compliant:", "must": "The following routes must all be compliant:"}, "how": {"fully_oa.doaj_under_review": {"not": "This journal is not under review at DOAJ", "must_or": "This journal is under review at DOAJ"}, "self_archiving": {"not": "This journal does not support Self-Archiving", "must_or": "This journal supports Self Archiving"}, "self_archiving.rights_retention_author_advice": {"not": "NOT RR Author Advice (need wording for this)", "must_or": "RR Author Advice [must] (need wording for this)"}, "hybrid": {"not": "This journal is not hybrid", "must_or": "This journal is hybrid"}, "fully_oa": {"not": "This journal is fully Open Access", "must_or": "This journal is fully Open Access"}, "tj": {"not": "This journal is not a Transformative Journal", "must_or": "This journal is a Transformative Journal"}, "ta.corresponding_authors": {"not": "TA is open to all authors", "must_or": "TA is only open to corresponding authors"}, "ta": {"not": "This journal does not appear in a Transformative Agreement", "must_or": "This journal appears in a Transformative Agreement"}}, "your_query": {"institution_label": "Institution", "unaffiliated": "Not part of Higher Education", "title": "Your query", "text": "You asked us to calculate whether you can comply with Plan S under the following conditions:", "publisher_label": "Publisher", "journal_title_unknown": "Unknown Title", "statement": "We carried out this query at {date}, and found {compliant} route{compliant_plural} that enable compliance, {non_compliant} non-compliant route{non_compliant_plural} and {unknown} undetermined route{unknown_plural}.", "publisher_not_known": "Not known", "funder_label": "Funder", "journal_label": "Journal"}, "routes": {"hybrid": {"unknown": {"explanation": "The following checks were carried out to determine if this is a hybrid journal:", "statement": "We are <b>unable to determine</b> if this journal is a hybrid journal"}, "yes": {"explanation": "The following checks were carried out to determine if this is a hybrid journal:", "statement": "This journal is a hybrid journal, and therefore you <b>can comply</b> with your funder's policy via this route"}, "no": {"explanation": "The following checks were carried out to determine if this is a hybrid journal:", "statement": "This journal is not a hybrid journal, and therefore you <b>cannot comply</b> with your funder's policy via this route"}, "label": "Hybrid Route"}, "fully_oa": {"unknown": {"explanation": "The following checks in the Directory of Open Access Journals (DOAJ) were carried out to determine compliance:", "statement": "We are <b>unable to determine if you are complaint</b> via the fully open access journal route."}, "yes": {"explanation": "The following checks in the Directory of Open Access Journals (DOAJ) were carried out to determine if your chosen journal is an open access journal that enables compliance:", "statement": "You are able to comply with Plan S as this is a fully open access journal."}, "no": {"explanation": "The following checks in the Directory of Open Access Journals (DOAJ) were carried out to determine that this is not a route to compliance:", "statement": "You are not able to <b>comply with Plan S</b> via the fully open access journal route."}, "label": "Open Access Journal Route"}, "tj": {"unknown": {"explanation": "The following checks were carried out on the JCT's Transformative Journal Index to determine compliance:", "statement": "We are unable to determine if this journal is a Transformative Journal and therefore <b>unable to determine compliance</b> via this route."}, "yes": {"explanation": "The following checks were carried out on the JCT's Transformative Journal Index to determine that this is a compliant route:", "statement": "This journal is a Transformative Journal and therefore you <b>can comply with Plan S</b> via this route."}, "no": {"explanation": "The following checks were carried out on the JCT's Transformative Journal Index to determine that this is not a compliant route:", "statement": "This journal is not a Transformative Journal and therefore you <b>cannot comply with Plan S</b> via this route."}, "label": "Transformative Journal Route"}, "self_archiving": {"unknown": {"explanation": "The following checks were carried out to determine compliance:", "statement": "We are <b>unable to determine</b> if you are able to comply with Plan S via Self-archiving, when publishing in this journal."}, "yes": {"explanation": "The following checks were carried out to determine whether the right exists to comply with Plan S via self-archiving. Data from Open Access Button Permissions (OAB Permissions) is used to see if the publisher's policy of self-archiving enables compliance. If it does not or if an unknown answer has been returned then the cOAlition S Implementation Roadmap data is checked to see if cOAlition S's Rights Retention Strategy provides a route to compliance:", "statement": "You are able to comply with Plan S via Self-archiving."}, "no": {"explanation": "The following checks were carried out to determine that this is not a compliant route:", "statement": "Self-archiving does not enable <b>Plan S</b> compliance when publishing in this journal."}, "label": "Self Archiving Route"}, "ta": {"unknown": {"explanation": "The following checks were carried out on the JCT's Transformative Agreement Index to determine compliance:", "statement": "We are <b>unable to determine</b> if you are able to comply with Plan S via a Transformative Agreement."}, "yes": {"explanation": "The following checks were carried out on the JCT's Transformative Agreement Index to determine if a Transformative Agreement is available that would enable compliance:", "statement": "You are able to comply with Plan S via a Transformative Agreement."}, "no": {"explanation": "The following checks were carried out on the JCT's Transformative Agreement Index to determine if a Transformative Agreement is available that would enable compliance:", "statement": "You are not able to <b>comply with Plan S</b> via a Transformative Agreement."}, "label": "Transformative Agreement Route"}}}, "modals": {"preferred": {"body": "<p>The Version of Record (VoR) is different from the Author Accepted Manuscript (AAM). The AAM is the version accepted for publication, including all changes made during peer review. The VoR contains all the changes from the copyediting process, journal formatting/branding etc., but it is also the version maintained and curated by the publisher, who has the responsibility to ensure that any corrections or retractions are applied in a timely and consistent way.</p> <p>For these reasons, the preferred option is to ensure that the VoR is made Open Access. Where the VoR can be made available in accordance with the Plan S principles, and there is a cost, many cOAlition S Organisations make funding available to cover these costs.</p>", "title": "Preferred Route to OA"}, "plan_s": {"body": "<p>Plan S aims for full and immediate Open Access to peer-reviewed scholarly publications from research funded by public and private grants. <a href=\"https://www.coalition-s.org/\" target=\"_blank\" rel=\"noopener\">cOAlition S</a> is the coalition of research funding and performing organisations that have committed to implementing Plan S. The goal of cOAlition S is to accelerate the transition to a scholarly publishing system that is characterised by immediate, free online access to, and largely unrestricted use and re-use (full Open Access) of scholarly publications. </p> <p>The Journal Checker Tool enables researchers to check whether they can comply with their funders Plan S aligned OA policy based on the combination of journal, funder(s) and the institution(s) affiliated with the research to be published. The tool currently only identifies routes to open access compliance for Plan S aligned policies.</p> <p>This is a <a href=\"https://www.coalition-s.org/\" target=\"_blank\" rel=\"noopener\">cOAlition S</a> project.</p> <p> <a href=\"/notices#privacy_notice\">Privacy Notice</a> \u2022 <a href=\"/notices#disclaimer_and_copyright\">Disclaimer & Copyright</a> </p>", "title": "What's this?"}, "sa_rr": {"body": "<p>The cOAlition S <a href=\"https://www.coalition-s.org/wp-content/uploads/2020/10/RRS_onepager.pdf\" target=\"_blank\" rel=\"noopener\">Rights Retention Strategy</a> sets out how you can retain sufficient rights to self-archive your Author Accepted Manuscript in any OA repository at the time of publication with a CC BY license. When using this route to make your research articles OA, no fees are payable to the publisher.</p> <p>Some subscription publishers may impose conditions -- via the License to Publish Agreement or otherwise -- that prevent you from meeting your funders' OA requirements. Authors should check publication terms before submitting a manuscript and should not sign a publishing contract that conflicts with funder conditions. Contact your funder for more information and guidance.</p>", "title": "Compliance through self-archiving using rights retention"}, "tj": {"body": "<p>A <em>Transformative Journal</em> is a subscription/hybrid journal that is committed to transitioning to a fully OA journal. It must gradually increase the share of OA content and offset subscription income from payments for publishing services (to avoid double payments).</p> <p>Check <a href=\"https://www.coalition-s.org/plan-s-funders-implementation/\" target=\"_blank\" rel=\"noopener\">here</a> to confirm if your funder will pay publishing fees.</p>", "title": "Transformative journals"}, "sa": {"body": "<p>Self-archiving is sometimes referred to as <em>green open access</em>. Publishing fees do not apply with this route.</p> <p>Publish your article via the journal\u2019s standard route and do not select an open access option. Following acceptance, deposit the full text version of the author accepted manuscript (the version that includes changes requested by peer-reviewers) to a repository without embargo and under a <a href=\"https://creativecommons.org/licenses/by/2.0/\" target=\"_blank\" rel=\"noopener\">CC BY licence</a>. Your funder may require you to archive your article in a specific repository.</p>", "title": "Self-archiving"}, "ta": {"body": "<p>Consult your institution\u2019s library prior to submitting to this journal. </p> <p><em>Transformative agreements</em> may have eligibility criteria or limits on publication numbers in place that the Journal Checker Tool is currently not able to check. </p>", "title": "Transformative agreements"}}, "site": {"why_am_i_seeing_this": "Why am I seeing this?", "preferred": "<a href=\"#\" class=\"modal-trigger\" data-modal=\"preferred\">Preferred</a>", "compliant": "The following publishing options are aligned with your funder\u2019s OA policy.", "card_modal": "More information", "card_institution_missing": "No institution specified", "non_compliant": "There are no publishing options aligned with your funder\u2019s OA policy."}, "api_codes": {"qualifications": {"rights_retention_author_advice": {"description": "your funder supports you to use the <a href=\"https://www.coalition-s.org/faq-theme/rights-licences/\" target=\"_blank\"  rel=\"noopener\"> cOAlition S rights retention strategy</a> as a route to compliance irrespective of the journal's self-archiving policy."}, "journal": {"description": "a transformative agreement is currently in force for this journal.", "end_date": "End date of the transformative agreement:", "start_date": "Start date of the transformative agreement:"}, "doaj_under_review": {"description": "this journal is currently under review for potential inclusion in DOAJ, it is yet to be approved for inclusion within the public DOAJ database."}, "institution": {"description": "a transformative agreement is currently in force for this institution.", "end_date": "End date of the transformative agreement:", "start_date": "Start date of the transformative agreement:"}, "corresponding_authors": {"description": "the corresponding author of the submitted article must be based at an institution within this transformative agreement for it to provide a route to compliance."}}, "logs": {"hybrid": {"Hybrid.NonCompliant.Properties": {"licence": "The licences available for you to publish in are:"}, "Hybrid.OAWTypeUnknown": "The journal type is not listed in OA.Works, we are unable to determine if it is Hybrid", "Hybrid.InDOAJ": "This journal is in DOAJ, which only lists fully Open Access journals, so this journal is not Hybrid", "Hybrid.NotInOAW": "This journal is not listed as a Hybrid or Transformative Journal in the OA.Works permissions database, so we are unable to tell if it is Hybrid", "Hybrid.Unknown": "We are unable to determine if the journal permits you to publish under a licence compliant with your funder's policy", "Hybrid.InOAW": "This journal is listed as a Hybrid or Transformative Journal in the OA.Works permissions database", "Hybrid.HybridInOAQ": "The journal is listed as Hyrid or Transformative in OA.Works", "Hybrid.NonCompliant": "The journal does not permit you to publish under a licence compliant with your funder's policy", "Hybrid.Compliant.Properties": {"licence": "The licences available for you to publish in are:"}, "Hybrid.NotInDOAJ": "This journal is not in DOAJ", "Hybrid.Compliant": "The journal permits you to publish under a licence compliant with your funder's policy", "Hybrid.NotHybridInOAW": "The journal is not listed as Hybrid or Transformative in OA.Works"}, "fully_oa": {"FullOA.Unknown.Properties": {"missing": "The following required information was missing from the DOAJ record:"}, "FullOA.NonCompliant.Properties": {"licence": "The licences allowed by this journal are:"}, "FullOA.NonCompliant": "This journal does not enable you to publish under a CC BY or equivalent licence required for policy compliance.", "FullOA.NotInDOAJ": "This journal is not present in DOAJ.", "FullOA.Compliant": "This journal enables you to publish under the following licences that are supported by your funder's policy:", "FullOA.Compliant.Properties": {"licence": ""}, "FullOA.InDOAJ": "This journal is present in DOAJ.", "FullOA.InProgressDOAJ": "This journal is currently under review for potential inclusion in DOAJ.", "FullOA.NotInProgressDOAJ": "This journal is not currently under review at DOAJ.", "FullOA.Unknown": "We were unable to determine if this journal provides a route to compliance."}, "tj": {"TJ.NoTJ": "This journal is not a Transformative Journal.", "TJ.NonCompliant": "As this journal is not a Transformative Journal, this route to compliance is not available.", "TJ.Exists": "This journal is a Transformative Journal.", "TJ.Compliant": "This Transformative Journal provides a route to compliance."}, "self_archiving": {"SA.OABNonCompliant": "This journal's self-archiving policy does not enable compliance with your funder's open access policy, for the following reason(s):", "SA.OABIncomplete": "We were unable to determine if this journal provides a route to compliance.", "SA.Compliant": "Self-archiving can be a route to compliance when publishing in this journal.", "SA.OABCompliant.Properties": {"embargo": "There is an embargo period (in months):", "version": "The manuscript version that can be archived is:", "licence": "The licence that can be used on the manuscript to be archived is:"}, "SA.NonCompliant": "Self-archiving is not a route to compliance when publishing in this journal.", "SA.Unknown": "We are unable to determine if this journal provides a route to compliance via self-archiving due to missing information.", "SA.RRException": "This journal does not allow self-archiving with no embargo and with a CC BY licence.", "SA.InOAB": "This journal is present in OAB Permissions.", "SA.OABNonCompliant.Properties": {"embargo": "There is an embargo period (in months):", "version": "The manuscript version that can be archived is:", "licence": "The licence that can be used on the manuscript to be archived is:"}, "SA.RRNoException": "This journal is not known to reject the Rights Retention Strategy", "SA.FunderRRNotActive": "Your funder has not implemented the <a href=\"https://www.coalition-s.org/faq-theme/rights-licences/\" target=\"_blank\"  rel=\"noopener\">Plan S Rights Retention Strategy</a>.", "SA.OABCompliant": "This journals self-archiving policy aligns with your funder's open access policy.", "SA.FunderRRActive": "Your funder has implemented the <a href=\"https://www.coalition-s.org/faq-theme/rights-licences/\" target=\"_blank\"  rel=\"noopener\">Plan S Rights Retention Strategy</a>. Rights retention takes precedence over the journal's self-archiving policy. It provides a route to compliance irrespective of publisher imposed restrictions or embargo periods.", "SA.NotInOAB": "This journal is not present in OAB Permissions.", "SA.OABIncomplete.Properties": {"missing": "The following required information was missing from the OAB Permissions database:"}}, "ta": {"TA.Exists": "A Transformative Agreement containing the selected journal and institution was found within our database.", "TA.Compliant": "A Transformative Agreement is available that can provide a route to compliance.", "TA.NotActive": "Our database shows that the Transformative Agreement containing the selected journal and institution has expired.", "TA.Active": "Our database shows that the Transformative Agreement containing the selected journal and institution is active.", "TA.Unknown": "We do not have sufficient information to determine if a Transformative Agreement is available to provide a route to compliance.", "TA.NoTA": "No Transformative Agreement containing the selected journal and institution was found within our database.", "TA.NonCompliant": "There is no Transformative Agreement available to provide a route to compliance."}}}, "cards": {"self_archiving": {"body": {"default": "<p>Upon acceptance, you can deposit your Author Accepted Manuscript in a repository without embargo and with a <a href=\"https://creativecommons.org/licenses/by/2.0/\" target=\"_blank\" rel=\"noopener\"> CC BY licence</a>. Publishing fees do not apply with this route. </p>"}, "explain": {"text": "This way to comply is available to you if the journal is not fully open access, but has a suitable policy for enabling Self-Archiving", "title": "Self-archiving"}, "title": "Self-archiving", "icon": "self_archiving"}, "rights_retention_non_compliant": {"body": {"default": "<p>cOAlition S has developed a Rights Retention Strategy to give researchers supported by a cOAlition S Funder the freedom to publish in their journal of choice, including subscription journals, whilst remaining fully compliant with Plan S. <a href=\"https://www.coalition-s.org/wp-content/uploads/2020/10/RRS_onepager.pdf\" target=\"_blank\" rel=\"noopener\">More information on how to use it is available here</a>.</p>"}, "title": "Rights retention", "icon": "false"}, "institution_non_compliant": {"body": {"default": "<p>If you or one of your co-authors are affiliated with different institutions, repeat your search with these alternative institutions. Transformative agreements are made between publishers and (consortia of) institutions. While the institution you searched does not currently have an agreement with the publisher of this journal, one of your collaborator\u2019s institutions may have one.</p>"}, "title": "Check with a different institution", "icon": "false"}, "sa_rr": {"body": {"default": "<p>Your funder\u2019s grant conditions set out how you can retain sufficient rights to self-archive the Author Accepted Manuscript in any OA repository. Publishing fees do not apply with this route.</p>"}, "explain": {"text": "This way to comply is available to you if the journal is not fully open access, but your funder has adopted the Rights Retention Strategy for Self-Archiving.", "title": "Compliance through self-archiving using rights retention"}, "title": "Compliance through self-archiving using rights retention", "icon": "self_archiving"}, "fully_oa": {"body": {"default": "<p>Go ahead and submit. Remember to select a <a href=\"https://creativecommons.org/licenses/by/2.0/\" target=\"_blank\" rel=\"noopener\"> CC BY licence</a> to ensure compliance.</p> <p>Upon publication, you have the right to self-archive the final published article as an additional route to compliance rather than an alternative route. </p>"}, "explain": {"text": "This way to comply is available to you if the journal is regarded as fully Open Access by DOAJ", "title": "Full Open Access"}, "title": "Full <br>Open Access", "icon": "fully_oa"}, "tj": {"body": {"default": "<p>Go ahead and submit. Remember to select the open access publishing option with a <a href=\"https://creativecommons.org/licenses/by/2.0/\" target=\"_blank\" rel=\"noopener\"> CC BY licence</a> to ensure compliance.</p> <p>Check <a href=\"https://www.coalition-s.org/plan-s-funders-implementation/\" target=\"_blank\" rel=\"noopener\">here</a> to confirm if your funder will pay publishing fees.</p>"}, "explain": {"text": "This way to comply is available to you if the journal has been identified as a Transformative Journal", "title": "Transformative journal"}, "title": "Transformative <br>journal", "icon": "tj"}, "journal_non_compliant": {"body": {"default": "<p>Repeat your search with an alternative journal to see if it provides a route to compliance with your funder\u2019s Plan S aligned open access policy.</p>"}, "title": "Check with an alternative journal", "icon": "false"}, "ta": {"body": {"default": "<p>Conditions may be in place around publishing through this agreement. <a href=\"#\" class=\"modal-trigger\" data-modal=\"ta\">Make sure to read this information</a>.</p> <p><em>{title}</em> is part of a transformative agreement between <em>{publisher}</em> and <em>{institution}</em></p>"}, "explain": {"text": "This way to comply is available to you if your selected journal and institution are both present in an active Transformative Agreement.", "title": "Transformative agreement"}, "title": "Transformative <br>agreement", "icon": "ta"}, "funder_non_compliant": {"body": {"default": "<p>If your research was funded by multiple Plan S funders, repeat your search using the name of one of the other funders. The implementation timeline for Plan S aligned open access policies is not the same for all funders, therefore results may vary by funder.</p>"}, "title": "Check with a different funder", "icon": "false"}, "ta_aq": {"body": {"default": "<p>The corresponding author of the submitted article must be based at an institution within this transformative agreement for it to provide a route to compliance</p> <p>Other conditions may also be in place around publishing through this agreement.</p> <p><a href=\"#\" class=\"modal-trigger\" data-modal=\"ta\">Make sure to read this information</a>.</p> <p><em>{title}</em> is part of a transformative agreement between <em>{publisher}</em> and <em>{institution}</em></p>"}, "explain": {"text": "This way to comply is available to you if you are the corresponding author and your selected journal and institution are both present in an active Transformative Agreement.", "title": "Transformative agreement"}, "title": "Transformative <br>agreement", "icon": "ta"}}}

devui.logs = {}
devui.logs.fully_oa = {}
devui.logs.fully_oa.compliant = [
    {code : "FullOA.InDOAJ"},
    {code : "FullOA.Compliant", "parameters" : {"licence" : ["cc-by"]}}
]
devui.logs.fully_oa.non_compliant = [
    {code: "FullOA.NotInDOAJ"},
    {code: "FullOA.NotInProgressDOAJ"}
]
devui.logs.fully_oa.unknown = [
    {code : "FullOA.InDOAJ"},
    {code: "FullOA.Unknown", "parameters" : {"missing" : ["licence"]}}
]

devui.logs.self_archiving = {}
devui.logs.self_archiving.compliant = [
    {code: "SA.InOAB"},
    {code: "SA.OABCompliant", "parameters" : {"version" : ["publishedVersion"], "embargo" : ["0"], "licence" : ["cc-by"]}}
]
devui.logs.self_archiving.non_compliant = [
    {code: "SA.NotInOAB"},
    {code: "SA.FunderRRNotActive"},
    {code: "SA.NonCompliant"}
]
devui.logs.self_archiving.unknown = [
    {code: "SA.InOAB"},
    {code: "SA.FunderRRNotActive"},
    {code: "SA.Unknown"}
]

devui.logs.ta = {}
devui.logs.ta.compliant = [
    {code: "TA.Exists"},
    {code: "TA.Active"},
    {code: "TA.Compliant"}
]
devui.logs.ta.non_compliant = [
    {code: "TA.NoTA"}
]
devui.logs.ta.unknown = [
    {code: "TA.Exists"},
    {code: "TA.Active"},
    {code: "TA.Unknown"}
]

devui.logs.tj = {}
devui.logs.tj.compliant = [
    {code: "TJ.Exists"},
    {code: "TJ.Compliant"}
]
devui.logs.tj.non_compliant = [
    {code: "TJ.NoTJ"}
]
devui.logs.tj.unknown = []

devui.cards = {}

devui.cards.fully_oa = {
    "compliant": "true",
    "match_routes": {"must": ["fully_oa"]},
    "id": "fully_oa",
    "preferred": "true"
}

devui.cards.sa_rr = {
    "match_qualifications": {"must": ["self_archiving.rights_retention_author_advice"]},
    "compliant": "true",
        "match_routes": {"not": ["fully_oa"], "must": ["self_archiving"]},
    "id": "sa_rr",
        "modal": "sa_rr"
}

devui.cards.self_archiving = {
    "preferred": "false",
        "compliant": "true",
        "match_routes": {"not": ["fully_oa"], "must": ["self_archiving"]},
    "modal": "sa",
        "match_qualifications": {"not": ["self_archiving.rights_retention_author_advice"]},
    "id": "self_archiving"
}

devui.cards.ta = {
    "match_qualifications": {"not": ["ta.corresponding_authors"]},
    "compliant": "true",
        "match_routes": {"must": ["ta"]},
    "id": "ta",
        "preferred": "true"
}

devui.cards.ta_qa = {
    "match_qualifications": {"must": ["ta.corresponding_authors"]},
    "compliant": "true",
        "match_routes": {"must": ["ta"]},
    "id": "ta_aq",
        "preferred": "true"
}

devui.cards.tj = {
    "modal": "tj",
        "compliant": "true",
        "match_routes": {"must": ["tj"]},
    "id": "tj",
        "preferred": "true"
}

devui.cards.journal_non_compliant = {
    "compliant": "false",
        "match_routes": {"not": ["self_archiving", "fully_oa", "ta", "tj"]},
    "id": "journal_non_compliant",
        "preferred": "false"
}

devui.cards.funder_non_compliant = {
    "compliant": "false",
        "match_routes": {"not": ["self_archiving", "fully_oa", "ta", "tj"]},
    "id": "funder_non_compliant",
        "preferred": "false"
}

devui.cards.institution_non_compliant = {
    "compliant": "false",
        "match_routes": {"not": ["self_archiving", "fully_oa", "ta", "tj"]},
    "id": "institution_non_compliant",
        "preferred": "false"
}

devui.cards.rights_retention_author_advice = {
    "compliant": "false",
        "match_routes": {"not": ["self_archiving", "fully_oa", "ta", "tj"]},
    "id": "rights_retention_non_compliant",
        "preferred": "false"
}

devui.cards.default = {
    compliant: true,
    preferred: false
}

devui.makeAPIResponse = function(compliant_routes, non_compliant_routes, unknown_routes, quals, cards) {
    let results = [];
    for (let i = 0; i < compliant_routes.length; i++) {
        let qualifications = [];
        if (compliant_routes[i] === "self_archiving" && quals.includes("rights_retention_author_advice")) {
            qualifications = [{"rights_retention_author_advice": ""}]
        }
        if (compliant_routes[i] === "ta" && quals.includes("corresponding_authors")) {
            qualifications = [{"corresponding_authors" : ""}]
        }
        results.push({
            route : compliant_routes[i],
            compliant: "yes",
            issn: ["1474-9718", "1474-9726"],
            log:  devui.logs[compliant_routes[i]].compliant,
            qualifications: qualifications
        })
    }
    for (let i = 0; i < non_compliant_routes.length; i++) {
        results.push({
            route : non_compliant_routes[i],
            compliant: "no",
            issn: ["1474-9718", "1474-9726"],
            log:  devui.logs[non_compliant_routes[i]].non_compliant
        })
    }

    for (let i = 0; i < unknown_routes.length; i++) {
        results.push({
            route : unknown_routes[i],
            compliant: "unknown",
            issn: ["1474-9718", "1474-9726"],
            log:  devui.logs[unknown_routes[i]].unknown
        })
    }

    let cards_settings = []
    for (let i = 0; i < cards.length; i++) {
        let cid = cards[i];
        let cfg = {...devui.cards.default};
        if (devui.cards[cid]) {
            cfg = {...devui.cards[cid]};
        }
        cfg.id = cid;
        cards_settings.push(cfg)
    }

    return {
        request: {},
        compliant: compliant_routes.length > 0,
        results: results,
        cards: cards_settings
    }
}

devui.responses = {}
devui.responses.fully_oa = devui.makeAPIResponse(["fully_oa"], ["ta", "tj", "self_archiving"], [], [], []);
devui.responses.sarr = devui.makeAPIResponse(["self_archiving"], ["fully_oa", "ta", "tj"], [], ["rights_retention_author_advice"], []);
devui.responses.sa = devui.makeAPIResponse(["self_archiving"], ["fully_oa", "ta", "tj"], [], [], []);
devui.responses.ta = devui.makeAPIResponse(["ta"], ["fully_oa", "tj", "self_archiving"], [], [], []);
devui.responses.taaq = devui.makeAPIResponse(["ta"], ["fully_oa", "tj", "self_archiving"], [], ["corresponding_authors"], []);
devui.responses.tj = devui.makeAPIResponse(["tj"], ["fully_oa", "ta", "self_archiving"], [],[], [])
devui.responses.non_compliant = devui.makeAPIResponse([], ["tj", "ta", "self_archiving", "fully_oa"], [], [], [])
devui.responses.max = devui.makeAPIResponse(["self_archiving", "fully_oa", "ta", "tj"], [], [], ["corresponding_authors"], ["fully_oa", "sa_rr", "self_archiving", "ta", "ta_aq", "tj"])
devui.responses.unknown = devui.makeAPIResponse([], [], ["self_archiving", "fully_oa", "ta", "tj"], [], [])


devui.api_response = devui.responses.max;
devui.chosen = {
    "journal":{
        "title":"Aging",
        "issn":["1945-4589"],
        "publisher":"\"Impact Journals, LLC \"",
        "id":"1945-4589"
    },
    "funder":{
        "title":"Wellcome",
        "id":"wellcome"
    },
    "institution":{
        "title":"Imperial Oil",
        "country":"Canada",
        "id":"00bve7358"
    }
}

jct.result_equals_chosen = function() {
    return true;
}

devui.setup = function() {
    jct.chosen = devui.chosen;
    jct.latest_full_response = devui.api_response;
    jct.lang = devui.lang;
    jct.success();
    jct.d.toggle_detailed_results();
}