import {resetProgress} from './utils.js';

document.addEventListener("DOMContentLoaded", () => {
    initCardForm();
    initCardDeleteButtons();
    initJSONEditing();
});

function initCardForm() {
    const buttonAddNewCard = document.getElementById("add-card");

    if (buttonAddNewCard) {
        buttonAddNewCard.addEventListener("click", function () {

            const cards = document.querySelectorAll("#formset-container .word-card");

            if (cards.length > 1) {
                const lastCard = cards[cards.length - 2];

                if (isCardEmpty(lastCard)) {
                    buttonAddNewCard.classList.add("shake");

                    setTimeout(() => {
                        buttonAddNewCard.classList.remove("shake");
                    }, 300);

                    return;
                }
            }

            addWordCard();
        });
    }
}

function initCardDeleteButtons() {
    document.addEventListener("click", function (e) {
        const btn = e.target.closest(".delete-btn");
        if (!btn) return;

        const card = btn.closest(".word-card");
        if (!card) return;

        // new card
        if (card.parentNode.classList.contains("extra-card")) {
            if (isCardEmpty(card)) {
                card.closest(".col").remove();
                return;
            }
        }

        // existing card from db
        const checkbox = card.querySelector('input[type="checkbox"]');

        if (checkbox) {
            checkbox.checked = !checkbox.checked;
            card.classList.toggle("opacity-50");
        }
    });
}

function isCardEmpty(card) {
    const fields = card.querySelectorAll("input[type='text'], textarea");

    return [...fields].every(field => field.value.trim() === "");
}

function addWordCard() {
    const buttonAddNewCard = document.getElementById("add-card");

    const totalForms = document.getElementById("id_form-TOTAL_FORMS");
    const currentIndex = totalForms.value;

    const template = document.getElementById("empty-form-template").innerHTML;
    const newFormHTML = template.replace(/__prefix__/g, currentIndex);

    const temp = document.createElement("div");
    temp.innerHTML = newFormHTML;

    const newForm = temp.firstElementChild;
    newForm.classList.add("extra-card");

    document.getElementById("formset-container")
        .insertBefore(newForm, buttonAddNewCard.parentNode);

    totalForms.value = parseInt(currentIndex) + 1;

    return newForm;
}

// function deleteLast

function initJSONEditing() {
    const jsonTextarea = document.getElementById('json_edit');
    const deckTitle = document.getElementById('id_title');
    const deckDescription = document.getElementById('id_description');
    const deckCefr = document.getElementById('id_cefr_level');
    const formsetsContainer = document.getElementById('formset-container');
    const formsets = formsetsContainer.querySelectorAll('.word-card:not(.add-card-button-bg)');

    const applyBtn = document.getElementById('apply_json');

    // forms -> textarea json
    let formsContent = {
        deck_title: deckTitle.value,
        deck_description: deckDescription.value,
        deck_level: deckCefr.value,
        words: [],
    };

    formsets.forEach((el, i) => {
        const wordTitle = el.querySelector(`#id_form-${i}-word`);
        const wordTranslation = el.querySelector(`#id_form-${i}-translation`);
        const wordDescription = el.querySelector(`#id_form-${i}-description`);
        formsContent.words.push({
            word: wordTitle.value,
            translation: wordTranslation.value,
            description: wordDescription.value,
        })
    })

    jsonTextarea.value = jsonToHuman(formsContent);

    // textarea json -> forms
    applyBtn.addEventListener('click', async function (e) {
        console.log('click');
        const updatedJSON = humanToJson(jsonTextarea.value);

        // main form
        deckTitle.value = updatedJSON.deck_title;
        deckDescription.value = updatedJSON.deck_description;
        deckCefr.value = updatedJSON.deck_level;

        // subforms
        for (const formset of formsets) {
            const formsetInputs = formset.querySelectorAll('input[type="text"], textarea')
            const wordTitle = formsetInputs[0];
            const wordTranslation = formsetInputs[1];
            const wordDescription = formsetInputs[2];
            wordTitle.value = '';
            wordTranslation.value = '';
            wordDescription.value = '';
        }

        const totalForms = document.getElementById("id_form-TOTAL_FORMS");
        const formsCount = parseInt(totalForms.value);

        updatedJSON.words.forEach((el, i) => {
            const form = (i < formsCount) ? formsets[i] : addWordCard();
            const wordTitle = form.querySelector(`#id_form-${i}-word`);
            const wordTranslation = form.querySelector(`#id_form-${i}-translation`);
            const wordDescription = form.querySelector(`#id_form-${i}-description`);

            wordTitle.value = updatedJSON.words[i].word;
            wordTranslation.value = updatedJSON.words[i].translation;
            wordDescription.value = updatedJSON.words[i].description;
        });

        for (const formset of formsets) {
            const formsetInputs = formset.querySelectorAll('input[type="text"], textarea')
            const wordTitle = formsetInputs[0];
            const wordTranslation = formsetInputs[1];
            if (wordTitle.value === '' || wordTranslation.value === '') {
                const checkbox = formset.querySelector('input[type="checkbox"]');
                checkbox.checked = true;
                formset.classList.add("opacity-50");
            }
        }

        const deckId = applyBtn.dataset.deckId;
        console.log(deckId);
        await resetProgress(deckId, false);
    })

}


function jsonToHuman(data) {
    let result = '';

    result += `Title: ${data.deck_title}\n`;
    result += `Description: ${data.deck_description}\n`;
    result += `Level: ${data.deck_level}\n`;
    result += `Words:\n`;

    data.words.forEach(item => {
        result += `${item.word} : ${item.translation} : ${item.description}\n`;
    });

    return result;
}

function humanToJson(text) {
    const lines = text.split('\n').map(line => line.trim()).filter(Boolean);

    const result = {
        deck_title: '',
        deck_description: '',
        deck_level: '',
        words: []
    };

    let wordsMode = false;

    for (const line of lines) {
        if (line.startsWith('Title:')) {
            result.deck_title = line.replace('Title:', '').trim();
        }
        else if (line.startsWith('Description:')) {
            result.deck_description = line.replace('Description:', '').trim();
        }
        else if (line.startsWith('Level:')) {
            result.deck_level = line.replace('Level:', '').trim();
        }
        else if (line.startsWith('Words:')) {
            wordsMode = true;
        }
        else if (wordsMode) {
            const parts = line.split(':');

            result.words.push({
                word: parts[0].trim() || '',
                translation: parts[1].trim() || '',
                description: parts.slice(2).join(' : ') || ''
            });
        }
    }

    return result;
}