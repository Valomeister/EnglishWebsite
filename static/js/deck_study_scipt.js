document.addEventListener("DOMContentLoaded", () => {
    initDeckSlider();
});

function initDeckSlider() {
    const cards = document.querySelectorAll(".flashcard-wrapper");
    const wordOptionBtn1 = document.getElementById("wordOptionBtn1");
    const wordOptionBtn2 = document.getElementById("wordOptionBtn2");
    const wordOptionBtn3 = document.getElementById("wordOptionBtn3");
    const showBtn = document.getElementById("showBtn");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const currentIndexEl = document.getElementById("currentCardIndex");
    const totalCardsEl = document.getElementById("totalCards");
    const cardsContainer = document.getElementById("flashcards-container");
    const opt1Percentage = document.getElementById("option1Percentage");
    const opt2Percentage = document.getElementById("option2Percentage");
    const opt3Percentage = document.getElementById("option3Percentage");
    const completionBanner = document.getElementById("completionBanner");
    const deckStudyControls = document.getElementById("deckStudyControls");
    const deckStudyControlsHint = document.getElementById("deckStudyControlsHint");
    const pageTitle = document.getElementById("pageTitle");
    const cardIndexWrapper = document.getElementById("cardIndexWrapper");
    const mode = cardsContainer.dataset.mode;

    let index = 0;
    let revealed = false;

    function updateTotalCards() {
        let count = 0;
        cards.forEach((el, i) => {
            if (el.dataset.mastery !== undefined &&(el.dataset.mastery) <= 99) {
                count++;
            }
        });

        totalCardsEl.textContent = count.toString();
    }

    function updateOptionsPercentages() {
        if (mode !== "study") return;
        const curCard = getCurrentCard();
        opt1Percentage.textContent = curCard.dataset.option1;
        opt2Percentage.textContent = curCard.dataset.option2;
        opt3Percentage.textContent = curCard.dataset.option3;
    }

    function getCurrentCard() {
        return cards[index];
    }

    function render() {
        cards.forEach((card, i) => {
            card.classList.toggle("d-none", i !== index);
        });

        revealed = false;
        hideContent();
        currentIndexEl.textContent = index + 1;
    }

    function showContent() {
        const body = getCurrentCard()
            .querySelector(".flashcard-content");

        body.classList.remove("d-none");
        revealed = true;
    }

    function hideContent() {
        const body = getCurrentCard()
            .querySelector(".flashcard-content");

        body.classList.add("d-none");
        revealed = false;
    }

    function toggleContent() {
        if (revealed) hideContent();
        else showContent();
    }

    function nextCard(hideMasteredCards=false, hideAssessedCards=false) {
        const total = cards.length;

        if (total === 0) return;

        let startIndex = index;

        do {
            index = (index + 1) % total;

            if (index === startIndex) {
                pageTitle.classList.add('d-none');
                cardIndexWrapper.classList.add('d-none');
                cardsContainer.classList.add('d-none');
                deckStudyControls.classList.add('d-none');
                deckStudyControlsHint.classList.add('d-none');
                completionBanner.classList.remove('d-none')
                return;
            }
        } while (
            hideMasteredCards && Number(getCurrentCard().dataset.mastery) >= 90 ||
            hideAssessedCards && getCurrentCard().dataset.mastery !== '');

        render();
        updateOptionsPercentages();
    }

    function prevCard() {
        const total = cards.length;

        if (total === 0) return;

        index = (total + (index - 1)) % total;

        render();
        updateOptionsPercentages();
    }

    async function answer(option) {
        const card = getCurrentCard();

        const deckId = cardsContainer.dataset.deckId;
        const cardId = card.dataset.cardId;

        const response = await fetch(`/decks/${deckId}/study/progress/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                card_id: cardId,
                option: option,
                mode: mode,
            })
        });

        const data = await response.json();

        if (data.success) {
            const resultingMastery = data.mastery;

            card.dataset.mastery = resultingMastery;

            const currentCardMastery = card.querySelector(".current_card_mastery");
            setTimeout(() => {
                currentCardMastery.textContent = resultingMastery.toString();
                currentCardMastery.parentElement.classList.remove('invisible');
            }, 200)

            if (resultingMastery === 100) {
                setTimeout(() => {
                    card.children[0].classList.remove('deck_card_bad_mastery');
                    card.children[0].classList.remove('deck_card_medium_mastery');
                    card.children[0].classList.add('deck_card_good_mastery');
                }, 200);
            } else if (resultingMastery === 50) {
                setTimeout(() => {
                    card.children[0].classList.remove('deck_card_bad_mastery');
                    card.children[0].classList.remove('deck_card_good_mastery');
                    card.children[0].classList.add('deck_card_medium_mastery');
                }, 200);

            } else if (resultingMastery === 0) {
                setTimeout(() => {
                    card.children[0].classList.remove('deck_card_good_mastery');
                    card.children[0].classList.remove('deck_card_medium_mastery');
                    card.children[0].classList.add('deck_card_bad_mastery');
                }, 200);
            }

            if (mode === "study") {
                card.dataset.option1 = data.masteryOptions[0];
                card.dataset.option2 = data.masteryOptions[1];
                card.dataset.option3 = data.masteryOptions[2];
                updateOptionsPercentages();
            }

            nextCard(true, (mode === "assess"));
        }
    }

    // click on card
   document.addEventListener("click", (e) => {
        const cardBody = e.target.closest(".card-header");
        if (cardBody) return;
        const card = e.target.closest(".flashcard");
        if (!card) return;

        toggleContent();
    });


    // buttons
    wordOptionBtn1.addEventListener("click", () => answer(1));
    wordOptionBtn2.addEventListener("click", () => answer(2));
    wordOptionBtn3.addEventListener("click", () => answer(3));
    showBtn.addEventListener('click', (e) => toggleContent());
    prevBtn.addEventListener('click', (e) => prevCard());
    nextBtn.addEventListener('click', (e) => nextCard());

    // keyboard
    document.addEventListener("keydown", (e) => {
        if (e.code === "Space") {
            e.preventDefault();
            toggleContent();
            flashClass(showBtn, 'show_btn_fake_hover', 140);
        }

        if (e.key === "3") {
            answer(3);
            flashClass(wordOptionBtn3, 'know_btn_fake_hover', 140);
        }

        if (e.key === "2") {
            answer(2);
            flashClass(wordOptionBtn2, 'not_sure_btn_fake_hover', 140);
        }

        if (e.key === "1") {
            answer(1);
            flashClass(wordOptionBtn1, 'dont_know_btn_fake_hover', 140);
        }

        if (e.key === "ArrowLeft") {
            prevCard();
            flashClass(prevBtn, 'secondary_btn_fake_hover', 140);
        }

        if (e.key === "ArrowRight") {
            nextCard();
            flashClass(nextBtn, 'secondary_btn_fake_hover', 140);
        }
    });
    prevCard(); nextCard(true, (mode === "assess")); // update
    updateTotalCards();
    render();
    updateOptionsPercentages();
}

function flashClass(el, cl, time) {
    el.classList.add(cl);
    setTimeout(() => {
        el.classList.remove(cl);
    }, time);
}