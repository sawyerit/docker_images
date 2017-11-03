/*jshint esversion: 6 */
var lastupdate = 0;

function formatState(state, time) {
    dateStr = dateFormat(new Date(parseInt(time) * 1000), "mmm dS, yyyy, h:MM TT");
    return state.charAt(0).toUpperCase() + state.slice(1) + " as of " + dateStr;
}

garageclick = (name) => {
    $.ajax({
        url: "clk",
        data: { 'id': name }
    });
};

$.ajax({
    url: "cfg",
    success: function (data) {
        $("#doorlist").append(data.map(door => {
            var showhide = door[4] ? '' : 'dontshow';
            var nextState = door[2] == 'open' ? 'close' : 'open';
            var formattedState = formatState(door[2], door[3]);

            return `<div id="${door[0]}" class="card text-center">
            <div class="card-header"><div id="${door[0]}-door" class="garage ${door[2]}-garage"></div></div>
            <div class="card-block">
            <h4 class="card-title text-center">${door[1]}</h4>
            <p class="card-text">${formattedState}</p>
            <button id="${door[0]}-door-button" type="button" class="${showhide} btn " onclick="garageclick('${door[0]}')">Click to ${nextState.toUpperCase()}</a>;
            </div></div>`;
        }));

        // for (var i = 0; i < data.length; i++) {
        //     var id = data[i][0];
        //     var name = data[i][1];
        //     var state = data[i][2];
        //     var time = data[i][3];
        //     var autodoor = data[i][4];
        //     var nextState = state == 'open' ? 'close' : 'open';

        //     var card = '<div id="' + id + '" class="card text-center">';
        //     card = card + '<div class="card-header"><div id="' + id + '-door" class="garage ' + state + '-garage"></div></div>';
        //     card = card + '<div class="card-block">';
        //     card = card + '<h4 class="card-title text-center">' + name + '</h4>';
        //     card = card + '<p class="card-text">' + formatState(state, time) + '</p>';
        //     card = card + '<button id="' + id + '-door-button" type="button" class="'+ ((autodoor) ? '' : 'dontshow') + ' btn " onclick="garageclick(\'' + id + '\')">Click to ' + nextState.toUpperCase() + '</a>';
        //     card = card + '</div></div>';

        //     $("#doorlist").append(card);

        // }
    }
});

function uptime() {
    $.ajax({
        url: "upt",
        success: function (data) {
            $("#uptime").html(data);
            setTimeout(uptime, 60000);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            setTimeout(uptime, 60000);
        },
        dataType: "json",
        timeout: 60000
    });
}

function poll() {
    $.ajax({
        url: "upd",
        data: { 'lastupdate': lastupdate },
        success: function (response, status) {
            lastupdate = response.timestamp;
            console.log("last update: " + lastupdate);
            for (var i = 0; i < response.update.length; i++) {
                let id = response.update[i][0];
                let state = response.update[i][1];
                let time = response.update[i][2];
                let oppositeState = state == 'open' ? 'close' : 'open';

                $("#" + id + " p").html(formatState(state, time));
                $("#" + id + "-door").removeClass().addClass("garage " + state + "-garage");
                let btn = $("#" + id + "-door-button");
                btn.text(oppositeState.toUpperCase());
            }
            setTimeout(poll, 1000);
        },
        // handle error
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            // try again in 10 seconds if there was a request error
            console.log("likely no status change since last poll");
            setTimeout(poll, 10000);
        },
        //complete: poll,
        dataType: "json",
        timeout: 1000
    });
}

setupNav = () => {
    $('.navigate.garage-page').click(function () {
        window.location.href = 'garage.html';
    });
    $('.navigate.cameras-page').click(function () {
        window.location.href = 'cameras.html';
    });
    $('.navigate.lights-page').click(function () {
        window.location.href = 'lights.html';
    });
    $('.navigate.other-page').click(function () {
        window.location.href = 'other.html';
    });
}

$(document).ready(() => {
    uptime();
    poll();
    setupNav();
});
