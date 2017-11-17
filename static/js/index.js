
/* event listeners for buttons */
$( document ).ready(function(){
    $(".lang").on("click", function() {
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
    
    var clipboard = new Clipboard('.clipboard');

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
        var href = $("iframe").attr('src');
        get_document_url(href);
    });

    // $(".copyToClipboard").click( function(){
    //     var clipboardText = "";
    //     clipboardText = $("#modal-body-data").text();

    //     copyTextToClipboard(clipboardText);
    //     alert( "Copied to Clipboard" );
    // });
});


function get_metadata(field){
    var doc_symbol = $('p.document-symbol')[0].id;
    var metadata_url = '/metadata?tag='+field+'&doc_symbol='+doc_symbol
    document.getElementById("modal-body-data").innerHTML = location.protocol+"//"+location.host+metadata_url;
    $('#link_modal').modal("show");
}

function get_document_url(href){
    document.getElementById("modal-document-data").innerHTML = href;
    $('#document_modal').modal("show");
}


// function setDocumentButtonLang(language){
//     var lang = '';
//     if (dictionary.hasOwnProperty(language)) {
//         set_lang(dictionary[language]);
//     }
//     // var buttonLanguage = 
//     $("#doc-lang-select").html()
// }


// function copyTextToClipboard(text) {
//     var textArea = document.createElement("textarea");
//     textArea.value = text;
//     document.body.appendChild(textArea);
//     textArea.select();
//     try {
//         var successful = document.execCommand("copy");
//         var msg = successful ? 'successful' : 'unsuccessful';
//         console.log('Copying text command was ' + msg);
//     } catch (err) {
//         console.log('Oops, unable to copy');
//     }
//     document.body.removeChild( textArea );
// }


