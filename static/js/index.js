/* event listeners for buttons */
$( document ).ready(function(){
    $(".lang").on("click", function() {
        console.log( $(this).val() );
        var link = $(this).val();
        var iframe = $('#document-frame');
        iframe.attr('src', link);
    });
    
    $(function() {
        $( "#accordion" ).accordion({
            heightStyle: "content",
            "collapsible": true
        });
    });
    
    var elements = document.querySelectorAll(
        "#doc-title", 
        "#agenda",
        "#author",
        "#authority_authors",
        "#document_symbol",
        "#notes",
        "#publisher",
        "#pubyear",
        "#related_documents",
        "#subjects"
    );
    for (var i = 0; i < elements.length; i++) {
        elements[i].addEventListener("click", function() {
            console.log("clicked " + elements[i]);
        });
    };

});


