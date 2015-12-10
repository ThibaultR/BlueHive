
function onClickRadioUserEventApplication(userEventApplication) {
    userEventApplication.submit();
}

$(document).ready(function() {
    $('.row.element-block.event').click(function () {
        console.log("event triggered")
        var detailsBlock = $(this).next('.element-block-details');

        if(detailsBlock.hasClass('element-blocks-details-opened')){
            detailsBlock.removeClass('element-blocks-details-opened');
            detailsBlock.addClass('element-blocks-details-closed');
            setTimeout(function() {
                detailsBlock.css('display', 'none');
            }, 1000);
        } else {
            detailsBlock.css('display', 'block');
            detailsBlock.removeClass('element-blocks-details-closed');
            detailsBlock.addClass('element-blocks-details-opened');

        }
    });
});

