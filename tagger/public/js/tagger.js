/* This file is part of Tagger.
 *
 * Tagger is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Tagger is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Tagger.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Original Copyright (c) 2010, Lorenzo Pierfederici <lpierfederici@gmail.com>
 * Contributor(s): 
 */

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

