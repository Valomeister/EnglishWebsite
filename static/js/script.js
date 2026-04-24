function isCardEmpty(card) {
    const fields = card.querySelectorAll("input[type='text'], textarea");

    return [...fields].every(field => field.value.trim() === "");
}

document.addEventListener("click", function (e) {

    if (!e.target.closest(".delete-btn")) return;

    const btn = e.target.closest(".delete-btn");
    const card = btn.closest(".word-card");

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

const buttonAddNewCard = document.getElementById("add-card");

if (buttonAddNewCard) {
    buttonAddNewCard.addEventListener("click", function () {

        const cards = document.querySelectorAll("#formset-container .word-card");

        if (cards.length > 1) {
            const lastCard = cards[cards.length - 2];

            const inputs = lastCard.querySelectorAll("input, textarea");

            let isEmpty = true;

            inputs.forEach(input => {
                if (input.value.trim() !== "") {
                    if (input.type === "checkbox") return;
                    isEmpty = false;
                }
            });

            if (isEmpty) {
                buttonAddNewCard.classList.add("shake");

                setTimeout(() => {
                    buttonAddNewCard.classList.remove("shake");
                }, 300);

                return;
            }
        }

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
    });
}

const modal = document.getElementById("deleteModal");

if (modal) {
    modal.addEventListener("show.bs.modal", function (event) {
        console.log(1);
        const button = event.relatedTarget;
        const id = button.getAttribute("data-id");

        const form = document.getElementById("deleteForm");
        form.action = `/decks/${id}/delete/`;
    });
}
