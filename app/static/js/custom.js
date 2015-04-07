
(function($){

    $('#submit-xml').click(function() {

        xml = $('#textarea-xml').val();
        console.log(xml);

        $.ajax({
            url: '/input-xml',
            type: 'POST',
            data: {"xml" : xml},
            dataType:"json",
            success: function (result) {
                console.log(result.data);
            }
        });
    });

})(window.jQuery);
