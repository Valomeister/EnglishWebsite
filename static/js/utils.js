export async function resetProgress(deckId, reloadOnSuccess) {

    const response = await fetch(`/decks/${deckId}/study/progress/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            reset: true,
        })
    });

    const data = await response.json();

    if (reloadOnSuccess) {
        if (data.success && data.reset) {
            location.reload();
        }
    }

}