
/* event listeners for buttons */
$( document ).ready(function(){
    var lang = $("div#document_lang").text().trim();
    
    switch (lang.toLowerCase()){
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


    $(".lang").on("click", function() {
        var link = $(this).val();
        var iframe = $('#document-frame');
        iframe.attr('src', link);
        var lang = $(this).attr("id");

        var loc = window.location.href;
        var locLang = loc.split('?');
        console.log(locLang);
        if (locLang.length == 2){
            history.pushState( {'page': locLang[0]}, lang,  '?lang=' + lang);
        }

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
    $("#all-metadata").on("click", function(){
        get_metadata('');
    });

    $("#doc-lang-select").on("click", function(){
        var href = $("iframe").attr('src');
        get_document_url(href);
    });

    $("#document_modal").on("show.bs.modal", function(event){
        $(this).find('h4.modal-title').text("");
    });

    $("#metadata-xml").on("click", function(){
        var url = window.location.href;
        window.location = url + "&format=xml";
        $("#metadata-xml").prop('disabled', true);
        $("#metadata-json").prop('disabled', false)
    });

});


function get_metadata(field){
    var doc_symbol = encodeURIComponent($('p.document-symbol')[0].id);
    var metadata_url = '/metadata?tag='+field+'&doc_symbol='+doc_symbol
    document.getElementById("modal-document-data").innerHTML = location.protocol+"//"+location.host+'/dev'+metadata_url;
    $('#document_modal').modal("show");
}

function get_document_url(href){
    document.getElementById("modal-document-data").innerHTML = href;
    $('#document_modal').modal("show");
}

var dictionary = {
    "english": {
        "_documentlink": "Document Link",
        "_undl_link": "UNDL Page"
    },
    "spanish": {
        "_documentlink" : "Enlace del documento",
        "_undl_link": "UNDL Página"
    },
    "french": {
        "_documentlink" : "Lien du document",
        "_undl_link": "UNDL Page"
    },
    "german": {
        "_documentlink" : "Dokumentlink",
        "_undl_link": "UNDL Seite"
    },
    "russian": {
        "_documentlink": "ссылка документа",
        "_undl_link": "UNDL страница"
    },
    "arabic": {
        "_documentlink" : "رابط المستند",
        "_undl_link": "صفحة UNDL"
    },
    "chinese": {
        "_documentlink" : "文件链接",
        "_undl_link": "UNDL 页"
    }
};


function setDocumentButtonLang(language){
    if (dictionary.hasOwnProperty(language)) {
        $("#doc-lang-select").html(dictionary[language]["_documentlink"]);
        $("#link-lang-select").html(dictionary[language]["_undl_link"]);
    }
};

// function setModalLang(language, prop){
//     if(dictionary.hasOwnProperty(language)) {
//         if(prop == "metadata"){
//             $("#modal-lable").text(dictionary[language]["_metadatalink"]);
//         } else {
//             $("#modal-lable").text(dictionary[language]["_documentlink"]);
//         }
//     }
// };
