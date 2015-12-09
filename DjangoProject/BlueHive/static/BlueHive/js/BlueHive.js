
function onClickRadioUserEventApplication(userEventApplication) {
    userEventApplication.submit();
}


/*TODO make it work*/
$('.panel-body').on('click', function () {
    var details = $(this).next('.element-block-details');
    console.log(details);
    console.log('tamere')
});

$('document.body').on('click', '.row.element-block.event', function() {
    // do something

    console.log('tamere')
});