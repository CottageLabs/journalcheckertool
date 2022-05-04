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

