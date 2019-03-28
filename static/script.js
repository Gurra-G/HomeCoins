$(document).ready(function() {
    // Kod inne i denna funktionen körs när sidan har laddats klart

    /*
        Döljer alla element (utom "<header>") i alla element av typen
        "<article>" med klassen "foldable"
    */
    $("article.foldable > *:not(header)").hide();

    /*
        När man klickar på ett "<header>"-element i ett "<article>"-
        element med klassen "foldable" så döljs/visas alla element
        som ligger efter "<header>"-elementet som användaren klickade på
    */
    $("article.foldable header").on("click", function() {
        $(this).nextAll("*").slideToggle();
    });
});