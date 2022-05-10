
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
