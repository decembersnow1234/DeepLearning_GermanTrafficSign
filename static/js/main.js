document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript chargé avec succès");

    // Sélectionner toutes les miniatures
    const miniatures = document.querySelectorAll(".miniature");
    console.log("Miniatures sélectionnées :", miniatures);

    // Pour chaque miniature, ajouter un événement "click"
    miniatures.forEach(function(miniature) {
        miniature.addEventListener("click", function() {
            // Récupérer l'URL de la nouvelle image
            const newImageUrl = this.getAttribute("data-image-url");
            console.log("Nouvelle URL de l'image :", newImageUrl);

            // Mettre à jour l'image principale avec la nouvelle URL
            const imagePrincipale = document.getElementById('image-principale');
            imagePrincipale.src = newImageUrl;
        });
    });
});
