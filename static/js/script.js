document.addEventListener("click", function(e) {

    if (e.target.closest(".delete-btn")) {

        const btn = e.target.closest(".delete-btn");
        const card = btn.closest(".word-card");
        const checkbox = card.querySelector('input[type="checkbox"]');

        checkbox.checked = !checkbox.checked;

        card.classList.toggle("opacity-50");
    }

});

const button = document.getElementById("add-card");
if (button) {
    button.addEventListener("click", function() {

        const totalForms = document.getElementById("id_form-TOTAL_FORMS");
        const currentIndex = totalForms.value;

        const template = document.getElementById("empty-form-template").innerHTML;

        const newFormHTML = template.replace(/__prefix__/g, currentIndex);

        const temp = document.createElement("div");
        temp.innerHTML = newFormHTML;

        const newForm = temp.firstElementChild;

        document.getElementById("formset-container")
            .insertBefore(newForm, button.parentNode);

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
