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