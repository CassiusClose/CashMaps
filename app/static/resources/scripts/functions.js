function updateParserProgress() {
    $.ajax({
        url: '/parser/_get_progress',
        type: 'POST',
        success: function(response) {
            setParserProgressMax(response.max);
            setParserProgress(response.progress);
            if(response.progress < response.max) {
                setTimeout(updateParserProgress, 1000);
            }
            else {
                $.ajax({url:'/parser/_parse_done',type:'POST',
                success: function(response1) {
                    window.location.replace(response.redirect_url);
                }});
            }
        }
    });
}

function setParserProgressMax(max) {
    $('#parserprogress').attr('max', max);
}

function setParserProgress(progress) {
    $('#parserprogress').val(progress);
}

function enableParserProgress() {
    updateParserProgress();
}
