/* event listeners for buttons */
$( document ).ready(function(){
    $(".lang").on("click", function() {
        console.log( $(this).val() );
        var link = $(this).val();
        var iframe = $('#frame');
        iframe.attr('src', link);
    });
});
