document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".remove-btn").forEach(button => {
        button.addEventListener("click", () => {
            let productId = button.getAttribute("data-id");
            removeProduct(productId);
        });
    });
});
