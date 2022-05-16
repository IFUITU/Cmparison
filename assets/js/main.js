
$(function(){
    $('form').on('submit', function(e){
        $('body').append('<div class="position-fixed text-center" id="loading-container"><div id="loading"><div><div class="spinner-border text-danger" role="status"><span class="sr-only">Loading...</span></div><h4>Wait! Loading...</h4></div></div>')
        
    });
})

