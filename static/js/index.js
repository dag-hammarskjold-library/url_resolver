// var clipboard = new Clipboard('.btn');

// clipboard.on('success', function(e) {
//     console.info('Action:', e.action);
//     console.info('Text:', e.text);
//     console.info('Trigger:', e.trigger);

//     e.clearSelection();
// });

// clipboard.on('error', function(e) {
//     console.error('Action:', e.action);
//     console.error('Trigger:', e.trigger);
// });



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

    $("#doc-lang-select").on("click", function(){
        console.log("Clicked doc-lang-select button");
        var href = $("iframe").attr('src');
        get_document_url(href);
    });

});


function get_metadata(field){
    var doc_symbol = $('p.document-symbol')[0].id;
    var data_modal = $('#link_modal');
    var metadata_url = '/metadata?tag='+field+'&doc_symbol='+doc_symbol
    document.getElementById("modal-body-data").innerHTML = location.protocol +"//"+location.host+metadata_url;
    $('#link_modal').modal("show");
}

function get_document_url(href){
    document.getElementById("modal-document-data").innerHTML = href;
    $('#document_modal').modal("show");
}
