import {resetProgress} from './utils.js';

document.addEventListener("DOMContentLoaded", () => {
    initDeleteModal();
    initStars();
    initProgressReset();
});

function initDeleteModal() {
    const modal = document.getElementById("deleteModal");
    if (!modal) return;

    modal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        const id = button.dataset.id;

        document.getElementById("deleteForm").action =
            `/decks/${id}/delete/`;
    });
}

function initStars() {
    document.addEventListener("click", async function(e) {
        const btn = e.target.closest(".star-btn");
        if (!btn) return;

        const deckId = btn.dataset.id;
        const response = await fetch(`/decks/library/${deckId}/star/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "X-Requested-With": "XMLHttpRequest"
            }
        });

        const data = await response.json();

        const empty = btn.querySelector(".empty-star");
        const filled = btn.querySelector(".filled-star");

        empty.style.display = data.starred ? "none" : "inline-block";
        filled.style.display = data.starred ? "inline-block" : "none";

        document.getElementById(`star-count-${deckId}`).textContent = data.count;
    });
}

function initProgressReset(){
    const resetBtn = document.getElementById("progress_reset");
    resetBtn.addEventListener('click', async function (e) {
        const deckId = resetBtn.dataset.deckId;
        await resetProgress(deckId, true);
    })
}