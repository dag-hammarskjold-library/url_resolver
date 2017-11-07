/* event listeners for buttons */
$( document ).ready(function(){
    $(".lang").on("click", function() {
        console.log( $(this).val() );
        var link = $(this).val();
        var iframe = $('#document-frame');
        iframe.attr('src', link);
    });
    $(function() {
        $( "#accordion" ).accordion();
    });
});
