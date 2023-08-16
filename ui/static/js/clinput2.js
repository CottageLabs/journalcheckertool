let clinput = {};

clinput.CLInput = class {
    constructor(params) {
        this.element = params.element;
        this.id = params.id;
        this.label = params.label || false;
        this.selection = params.initialSelection || false;
        this.inputAttrs = params.inputAttrs || {};

        this.optionsMethod = params.options;
        this.optionsTemplate = params.optionsTemplate;
        this.selectedTemplate = params.selectedTemplate;
        this.newValueMethod = params.newValue || false;
        this.selectionToSearchText = params.selectionToSearchText || clinput.selectionToText.guessText;

        this.optionsLimit = params.optionsLimit || 0;

        this.onInit = params.onInit || false;
        this.onChoose = params.onChoose || false;
        this.onClear = params.onClear || false;

        this.logState = params.hasOwnProperty("logState") ? params.logState : true;

        this.options = [];
        this.eventListeners = {};
        this.transitionInfo = {};
        this.search = "";

        this.draw();

        this.input = document.getElementById(this.id);

        if (this.selection) {
            this.transition(false, "Selected");
        } else {
            this.transition(false, "Initial");
        }

        if (this.onInit) {
            this.onInit(this);
        }
    }

    // API through which we interact
    ////////////////////////////////

    currentSelection() {
        // the object that is currently selected, if present
        return this.selection;
    }

    currentSearch() {
        return this.search;
    }

    clear(params) {
        this.search = "";
        this.selection = false;
        this.options = [];
        this.clearInput();
        this.clearOptions();

        this._log("clear");
        if (this.onClear && !params.silent) {
            this.onClear();
        }
    }

    reset(params) {
        this.clear(params);
        this._clearEventListeners();
        this.transition(false, "Initial");
    }

    // Display management
    ////////////////////////////////

    draw() {
        let attrs = []
        let keys = Object.keys(this.inputAttrs)
        for (var i = 0; i < keys.length; i++) {
            var key = keys[i];
            var val = this.inputAttrs[key];
            attrs.push(key + "=\"" + val + "\"");
        }
        let attrsFrag = attrs.join(" ");

        let labelFrag = "";
        if (this.label) {
            labelFrag = '<label for="' + this.id + '">' + this.label + '</label>';
        }
        let initialValue = "";
        if (this.selection) {
            initialValue = this.selectedTemplate(this.selection);
        }
        this.element.innerHTML = labelFrag + ' \
                <input autocomplete="off" type="text" id="' + this.id + '" name="' + this.id + '" ' + attrsFrag + ' value="' + initialValue + '">\
                <div id="' + this.id + '--options" class="clinput__options"></div>';

        this._log("Initial draw");
    }

    clearOptions() {
        document.getElementById(this.id + "--options").innerHTML = "";
    }

    renderOptions() {
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
    }

    clearInput() {
        this.input.value = "";
    }

    setInputToSearch() {
        if (this.search) {
            this.input.value = this.search;
            let end = this.search.length;
            window.setTimeout(() => {
                this.input.setSelectionRange(end, end);
            }, 0);
        }
    }

    setSelectionToSearch() {
        if (this.selection) {
            let text = this.selectionToSearchText(this);
            this.input.value = text;
            let end = text.length;
            window.setTimeout(() => {
                this.input.setSelectionRange(end, end);
            }, 0);
        }
    }

    // Data interactions
    ////////////////////////////////

    lookupOptions(callback) {
        this.search = this.input.value;
        this.optionsMethod(this.search, (data) => {this.optionsReceived(data, callback)});
    }

    optionsReceived(data, callback) {
        if (!this.optionsLimit) {
            this.options = data;
        } else {
            this.options = data.slice(0, this.optionsLimit);
        }

        if (this.newValueMethod && this.options.length === 0) {
            let nv = this.newValueMethod(this.search);
            if (nv) {
                this.options = [nv].concat(this.options);
            }
        }

        callback();
    }

    chooseOption(e, idx) {
        this.selection = this.options[idx];
        this.input.value = this.selectedTemplate(this.options[idx]);

        if (this.onChoose) {
            this.onChoose(e, this.options[idx]);
        }

        let event = new Event("change")
        this.input.dispatchEvent(event);
    }

    // State management
    ////////////////////////////////

    _addEventListener(element, event, listener) {
        if (!(event in this.eventListeners)) {
            this.eventListeners[event] = [];
        }
        let elementRegistered = false;
        for (let elementEvents of this.eventListeners[event]) {
            if (elementEvents.element === element) {
                elementEvents.listeners.push(listener)
                elementRegistered = true;
                break;
            }
        }
        if (!elementRegistered) {
            this.eventListeners[event].push({element: element, listeners: [listener]})
        }

        element.addEventListener(event, listener);
    }

    _removeEventListener(element, event) {
        if (!(event in this.eventListeners)) {
            return;
        }
        let remove = -1;
        for (let j = 0; j < this.eventListeners[event].length; j++) {
            let elementEvents = this.eventListeners[event][j]
            if (elementEvents.element === element) {
                for (let i = 0; i < elementEvents.listeners.length; i++) {
                    element.removeEventListener(event, elementEvents.listeners[i]);
                }
                remove = j;
                break;
            }
        }

        if (remove > -1) {
            this.eventListeners[event].splice(remove, 1);
        }
    }

    _clearEventListeners() {
        for (let event in this.eventListeners) {
            for (let elementEvents of this.eventListeners[event]) {
                for (let i = 0; i < elementEvents.listeners.length; i++) {
                    elementEvents.element.removeEventListener(event, elementEvents.listeners[i])
                }
            }
        }
        this.eventListeners = {};``
    }

    _log(msg) {
        if (!this.logState) { return }
        let datestamp = (new Date()).toISOString()
        console.log(`clinput: ${this.id}: ${datestamp}: ${msg}`);
    }

    transition(source, target, msg) {
        if (!msg) {
            msg = "";
        } else {
            msg = " - " + msg;
        }

        if (source) {
            let sourceFn = "state" + source + "Exit";
            this._log("TState: " + source + " (Exit)" + msg);
            this[sourceFn]();
        }

        let targetFn = "state" + target + "Enter";
        this._log("TState: " + target + " (Enter)" + msg);
        this[targetFn]();
    }

    stateInitialEnter() {
        this.clearOptions();
        this.clearInput();
        this._addEventListener(this.input, "focus", () => {
            this.transition("Initial", "ActiveInput", "input focus");
        });
    }

    stateInitialExit() {
        this._removeEventListener(this.input, "focus");
    }

    stateActiveInputEnter() {
        this.setInputToSearch();
        this._addEventListener(this.input, "blur", () => {
            if (!this.input.value) {
                this.clear();
            }
            if (this.selection) {
                this.transition("ActiveInput", "Selected", "input blur with selection")
            } else {
                this.transition("ActiveInput", "Initial", "input blur no selection")
            }
        })
        this._addEventListener(this.input, "keyup", (e) => {
            this.clearOptions();
            this.lookupOptions(() => {
                if (this.options.length > 0) {
                    this.transition("ActiveInput", "ActiveInputWithOptions", "input keyup");
                }
            });
        })
        if (this.input.value) {
            let event = new Event("keyup");
            this.input.dispatchEvent(event);
        }
    }

    stateActiveInputExit() {
        this._removeEventListener(this.input, "blur");
        this._removeEventListener(this.input, "keyup");
    }

    stateActiveInputWithOptionsEnter() {
        this.setInputToSearch();

        this._addEventListener(this.input, "blur", () => {
            if (!this.input.value) {
                this.clear();
            }
            if (!this.transitionInfo.toSelecting) {
                if (this.selection) {
                    this.transition("ActiveInputWithOptions", "Selected", "input blur selection exists")
                } else {
                    this.transition("ActiveInputWithOptions", "Initial", "input blur selection empty")
                }
            }
            delete this.transitionInfo.toSelecting;
        });

        this.renderOptions();

        let entries = document.getElementsByClassName("clinput__option_"+this.id);
        for (let i = 0; i < entries.length; i++) {
            this._addEventListener(entries[i], "mouseover", (e) => {
                this.transitionInfo.toSelecting = true;
                this.transitionInfo.targetEntry = e.target;
                this.transition("ActiveInputWithOptions", "Selecting", "entry mouseover");
            });
        }

        this._addEventListener(this.input, "keyup", (e) => {
            let code = this._getKeyCode(e);
            if (code === "ArrowDown") {
                this.transitionInfo.toSelecting = true;
                this.transitionInfo.targetEntry = entries[0]
                this.transition("ActiveInputWithOptions", "Selecting", "input arrow down");
            } else if (code === "Enter") {
                if (entries.length === 1) {
                    this.chooseOption(e, 0);
                    this.transition("ActiveInputWithOptions", "Selected", "input enter");
                }
            } else {
                this.lookupOptions(() => {
                    if (this.options.length > 0) {
                        let oldEntries = document.getElementsByClassName("clinput__option_"+this.id);
                        for (let i = 0; i < entries.length; i++) {
                            this._removeEventListener(oldEntries[i], "mouseover");
                        }

                        this.renderOptions();

                        let newEntries = document.getElementsByClassName("clinput__option_"+this.id);
                        for (let i = 0; i < newEntries.length; i++) {
                            this._addEventListener(entries[i], "mouseover", (e) => {
                                this.transitionInfo.toSelecting = true;
                                this.transitionInfo.targetEntry = e.target;
                                this.transition("ActiveInputWithOptions", "Selecting", "entry mouseover");
                            });
                        }
                    } else {
                        this.transition("ActiveInputWithOptions", "ActiveInput", "input keyup no options")
                    }
                });
            }
        })
    }

    stateActiveInputWithOptionsExit() {
        this._removeEventListener(this.input, "blur");
        this._removeEventListener(this.input, "keyup");

        let entries = document.getElementsByClassName("clinput__option_"+this.id);
        for (let i = 0; i < entries.length; i++) {
            this._removeEventListener(entries[i], "mouseover");
        }
    }

    stateSelectingEnter() {
        if (this.transitionInfo.targetEntry) {
            this.transitionInfo.targetEntry.focus();
            delete this.transitionInfo.targetEntry;
        }

        this._addEventListener(window, "click", (e) => {
            if (document.activeElement === this.input) {
                return;
            }

            let stillSelecting = false;
            let entries = document.getElementsByClassName("clinput__option_"+this.id);
            for (let j = 0; j < entries.length; j++) {
                if (document.activeElement === entries[j]) {
                    stillSelecting = true;
                    break;
                }
            }
            if (stillSelecting) {
                return;
            }

            if (!this.input.value) {
                this.clear();
            }

            if (this.selection) {
                this.transition("Selecting", "Selected", "window click existing selection");
            } else {
                this.transition("Selecting", "Initial", "window click no selection");
            }
        });

        this._addEventListener(this.input, "focus", ()=> {
            this.transition("Selecting", "ActiveInputWithOptions", "input focus");
        });

        let entries = document.getElementsByClassName("clinput__option_"+this.id);
        for (let i = 0; i < entries.length; i++) {
            this._addEventListener(entries[i], "mouseover", (e) => {
                e.target.focus();
            });
            this._addEventListener(entries[i], "click", (e) => {
                this.chooseOption(e, i);
                this.transition("Selecting", "Selected", "entry click");
            });
            this._addEventListener(entries[i], "keydown", (e) => {
                let code = this._getKeyCode(e)
                let idx = parseInt(e.target.getAttribute("data-idx"));

                if (entries.length !== 0) {
                    if (code === "ArrowDown") {
                        if (idx < entries.length - 1) {
                            entries[idx + 1].focus();
                            e.preventDefault();
                        }
                    } else if (code === "ArrowUp") {
                        if (idx > 0) {
                            entries[idx - 1].focus();
                        } else {
                            this.input.focus();
                        }
                    } else if (code === "Enter") {
                        this.chooseOption(e, idx);
                        this.transition("Selecting", "Selected", "entry enter");
                    } else if (code === "Tab") {
                        this.chooseOption(e, idx);
                        e.preventDefault();
                        this.transition("Selecting", "Selected", "entry tab");
                    }
                }
            });
        }
    }

    stateSelectingExit() {
        this._removeEventListener(window, "click");
        this._removeEventListener(this.input, "focus");

        let entries = document.getElementsByClassName("clinput__option_"+this.id);
        for (let i = 0; i < entries.length; i++) {
            this._removeEventListener(entries[i], "mouseover");
            this._removeEventListener(entries[i], "click");
            this._removeEventListener(entries[i], "keydown");
        }
    }

    stateSelectedEnter() {
        this.clearOptions();
        this.input.value = this.selectedTemplate(this.selection);
        this._addEventListener(this.input, "focus", () => {
            this.transition("Selected", "ActiveInputWithSelection", "input focus");
        });
    }

    stateSelectedExit() {
        this._removeEventListener(this.input, "focus");
    }

    stateActiveInputWithSelectionEnter() {
        this.setSelectionToSearch();
        this._addEventListener(this.input, "blur", () => {
            this.transition("ActiveInputWithSelection", "Selected", "input blur")
        })
        this._addEventListener(this.input, "keyup", (e) => {
            this.clearOptions();
            this.lookupOptions(() => {
                if (this.options.length > 0) {
                    this.transition("ActiveInputWithSelection", "ActiveInputWithOptions", "input keyup");
                }
            });
        })
        if (this.input.value) {
            let event = new Event("keyup");
            this.input.dispatchEvent(event);
        }
    }

    stateActiveInputWithSelectionExit() {
        this._removeEventListener(this.input, "blur");
        this._removeEventListener(this.input, "keyup");
    }


    // Utilities
    /////////////////////////////////////

    _getKeyCode(event){
        let code;

        if (event.key !== undefined) {
            code = event.key;
        } else if (event.keyIdentifier !== undefined) {
            code = event.keyIdentifier;
        } else if (event.keyCode !== undefined) {
            code = event.keyCode;
        }

        return code;
    }
};

clinput.selectionToText = {};
clinput.selectionToText.guessText = function(clInputInstance) {
    let lsv = clInputInstance.currentSearch().toLowerCase();
    let selection = clInputInstance.currentSelection();

    if (!selection) {
        return clInputInstance.currentSearch();
    }

    if (typeof(selection) === "string") {
        return selection;
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
        } else {
            console.log(v)
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
            return v
        }
    }

    return "";
}

clinput.options = {};
clinput.options.inputLimits = function(params) {
    let min = params.minTextLength || 0;
    let optionsLimit = params.optionsLimit || false;
    let inner = params.inner;

    return function(text, callback) {
        if (text.length < min) {
            callback([]);
            return;
        }

        let myCallback = function(results) {
            if (optionsLimit && results.length > optionsLimit) {
                results = results.slice(0, optionsLimit);
            }
            callback(results);
        }

        inner(text, myCallback);
    }
}

clinput.init = (params) => {
    return new clinput.CLInput(params)
}