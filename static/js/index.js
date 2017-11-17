
/* event listeners for buttons */
$( document ).ready(function(){
    $(".lang").on("click", function() {
        var link = $(this).val();
        var iframe = $('#document-frame');
        iframe.attr('src', link);

        var lang = $(this).attr("id");
        console.log(lang);

        switch (lang){
            case "en":
                setDocumentButtonLang("english");
                break;
            case "fr":
                setDocumentButtonLang('french');
                break;
            case "es":
                setDocumentButtonLang('spanish');
                break;
            case 'de':
                setDocumentButtonLang('german');
                break;
            case "ru":
                setDocumentButtonLang("russian");
                break;
            case "ar":
                setDocumentButtonLang("arabic");
                break;
            case "zh":
                setDocumentButtonLang("chinese");
                break;
        }
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

var dictionary = {
    "english": {
        "_documentlink": "Document Link"
    },
    "spanish": {
        "_documentlink" : "Enlace de documento"
    },
    "french": {
        "_documentlink" : "Lien de document"
    },
    "german": {
        "_documentlink" : "Dokumentlink"
    },
    "russian": {
        "_documentlink": "ссылка документа",
    },
    "arabic": {
        "_documentlink" : "رابط المستند"
    },
    "chinese": {
        "_documentlink" : "文件链接"
    }
};


function setDocumentButtonLang(language){
    if (dictionary.hasOwnProperty(language)) {
        $("#doc-lang-select").html(dictionary[language]["_documentlink"]);
    }
};
