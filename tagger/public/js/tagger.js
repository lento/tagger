/* we put all our functions and objects inside "tagger" so we don't clutter
 * the namespace */
tagger = new(Object);

/* if firebug is not active we create a fake "console" */
if (typeof(console)=="undefined") {
    console = new(Object);
    console.log = function() {};
}

/**********************************************************************
 * Overlays
 **********************************************************************/
tagger.overlays_activate = function(select) {
    if (typeof(select)=="undefined" || select==null) {
        select = "";
    }

    $(select + " .overlay").overlay({
        onBeforeLoad: function(event) {
            // grab wrapper element inside content
            var iframe = $("#overlay iframe")[0];
            //console.log('tagger.overlays_activate', wrap);

            // load the page specified in the trigger
            iframe.src = this.getTrigger().attr("href");
        },
        expose: {
            color: '#333'
        }
    });
}

/****************************************
 * Startup function
 ****************************************/
$(function() {
    tagger.overlays_activate();

    /* make #flash slide in and out */
    $("#flash div").hide().slideDown(function() {
        setTimeout(function() {
            $("#flash div").slideUp();
        }, 2500);
    });

    /* zebra stripes tables */
    $("tr:odd").addClass("odd").removeClass("even");
    $("tr:even").addClass("even").removeClass("odd");
});

