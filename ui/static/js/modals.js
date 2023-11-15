if (!window.hasOwnProperty("jct")) { jct = {}; }

// some convenience shortcuts
jct.d = document;
jct.d.gebi = document.getElementById;
jct.d.gebc = document.getElementsByClassName;

////////////////////////////////////////////////
// Modal handling

jct.bindModalTriggers = function() {
    let triggers = document.getElementsByClassName("modal-trigger");
    for (let i = 0; i < triggers.length; i++) {
        let trigger = triggers[i];
        trigger.removeEventListener("click", jct.modalTrigger);
        trigger.addEventListener("click", jct.modalTrigger)
    }
};

jct.modalTrigger = function(event) {
    event.preventDefault();
    let element = event.currentTarget;
    let modalId = element.getAttribute("data-modal");
    let modal = jct.build_modal(modalId);
    jct.modalShow(modal);
    if (jct.modal_setup.hasOwnProperty(modalId)) {
        jct.modal_setup[modalId]();
    }
};

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
};

jct.closeModal = function() {
    let modal_div = jct.d.gebi("jct_modal_container");
    modal_div.innerText = "";
    window.removeEventListener("click", jct._windowCloseModal)
};

jct._windowCloseModal = function(e) {
    let modals = [].slice.call(jct.d.gebc("modal"));
    if (modals.includes(e.target)){
        jct.closeModal();
    }
};

jct.build_modal = (modal_id) => {
    let modalText = jct.lang ? jct.lang.modals[modal_id] : "";
    if (!modalText) {
        modalText = jct.site_modals[modal_id];
        if (!modalText) {
            console.log("No modal text found for " + modal_id);
            return "";
        }
        if (modalText.en) {
            if (modalText[jct.languageCode]) {
                modalText = modalText[jct.languageCode];
            } else {
                modalText = modalText.en;
            }
        }
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
    </div>`;
    return modal_html;
};
