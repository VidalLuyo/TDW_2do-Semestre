// Interacciones pequeñas de la demo: cierre de notificaciones flash.
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-alert-close]").forEach((boton) => {
        boton.addEventListener("click", () => {
            const alerta = boton.closest("[data-alert]");
            if (!alerta) return;

            // Se anima con clases de Tailwind y luego se retira del DOM.
            alerta.classList.add("opacity-0", "translate-y-1");
            window.setTimeout(() => alerta.remove(), 200);
        });
    });
});
