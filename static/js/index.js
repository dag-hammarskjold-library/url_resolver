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
    
    // var elements = document.querySelectorAll(
    //     "#doc-title", 
    //     "#agenda",
    //     "#author",
    //     "#authority_authors",
    //     "#document_symbol",
    //     "#notes",
    //     "#publisher",
    //     "#pubyear",
    //     "#related_documents",
    //     "#subjects",
    //     "#summary",
    //     "#title-statement"
    // );
    // for (var i = 0; i < elements.length; i++) {
    //     elements[i].addEventListener("click", function() {
    //         console.log("clicked " + elements[i]);
    //     });
    // };

    $("#title").on("click", function(){
        get_metadata('title');
    });
    $("#title_statement").on("click", function(){
        get_metadata('title_statement');
    });
    $("#document_symbol").on("click", function(){
        get_metadata('document_symbol');
    });
    $("#pubyear").on("click", function(){
        get_metadata('pubyear');
    });
    $("#agenda").on("click", function(){
        get_metadata('agenda');
    });
    $("#author").on("click", function(){
        get_metadata('author');
    });
    $("#imprint").on("click", function(){
        get_metadata('imprint');
    });
    $("#summary").on("click", function(){
        get_metadata('summary');
    });
    $("#agenda").on("click", function(){
        get_metadata('agenda');
    });
    $("#subjects").on("click", function(){
        get_metadata('subjects');
    });
    $("#notes").on("click", function(){
        get_metadata('notes');
    });
    $("#related_documents").on("click", function(){
        get_metadata('related_documents');
    });
    $("#authority_authors").on("click", function(){
        get_metadata('authority_authors');
    });

});


function get_metadata(field){
    var doc_symbol = $('p.document-symbol')[0].id;
    var data_modal = $('#link_modal');
    $.ajax({
        url: '/metadata?tag='+field+'&doc_symbol='+doc_symbol,
        type: 'GET',
        cache: false,
        processData: false,
        contentType: false,
        success: function(data) {
            console.log(data);
            // var obj = jQuery.parseJSON(data);
            // jsonData = JSON.stringify(data, undefined, 2);
            document.getElementById("modal-body-data").innerHTML = data;
            $('#link_modal').modal("show");
        },
        error: function(message) {
            console.log(message);
        }
    });


}


