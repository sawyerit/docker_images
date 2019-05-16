/*jshint esversion: 6 */
var lastupdate = 0;

function formatState(state, time) {
    dateStr = dateFormat(new Date(parseInt(time) * 1000), "mmm dS, yyyy, h:MM TT");
    return state.charAt(0).toUpperCase() + state.slice(1) + " as of " + dateStr;
}

garageclick = (name) => {
    $.ajax({
        url: "clk",
        data: { 'id': name, 'type': 'door' }
    });
};

zoneclick = (name) => {
    $.ajax({
        url: "clk",
        data: { 'id': name, 'type': 'zone' }
    });
};

$.ajax({
    url: "cfg-door",
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
            <button id="${door[0]}-door-button" type="button" class="${showhide} btn " onclick="garageclick('${door[0]}')">Click to ${nextState.toUpperCase()}</a>
            </div></div>`;
        }));
    },
    error: function (XMLHttpRequest, textStatus, errorThrown) {
        Console.log(errorThrown);
    }
});

$.ajax({
    url: "cfg-zone",
    success: function (data) {
        $("#zonelist").append(data.map(zone => {
            var nextState = zone[3] == 'on' ? 'off' : 'on';
            var formattedState = formatState(zone[1], zone[2]);

            return `<div id="${zone[0]}" class="card text-center">
            <div class="card-header"><div id="${zone[0]}-zone" class="sprinkler ${zone[3]}-sprinkler"></div></div>
            <div class="card-block">
            <h4 class="card-title text-center">${zone[1]}</h4>
            <p class="card-text">${formattedState}</p>
            <button id="${zone[0]}-zone-button" type="button" btn " onclick="zoneclick('${zone[0]}')">${nextState.toUpperCase()}</a>
            </div></div>`;
        }));
    },
    error: function (XMLHttpRequest, textStatus, errorThrown) {
        Console.log(errorThrown);
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

function info() {
    $.ajax({
        url: "inf",
        success: function (data) {
            $("#version").html(data);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            $("#version").html(errorThrown);
        },
        dataType: "html"
    });
}

function poll() {
    if ($("h1").text() == "Garages") {
        $.ajax({
            url: "upd-door",
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
                    btn.text("Click to " + oppositeState.toUpperCase());
                }
                setTimeout(poll, 2000);
            },
            // handle error
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                // try again in 10 seconds if there was a request error
                console.log("likely no status change in the door since last poll " + errorThrown);
                setTimeout(poll, 10000);
            },
            //complete: poll,
            dataType: "json",
            timeout: 1000
        });
    }
    if ($("h1").text() == "Zones") {
        $.ajax({
            url: "upd-zone",
            data: { 'lastupdate': lastupdate },
            success: function (response, status) {
                lastupdate = response.timestamp;
                console.log("last update: " + lastupdate);
                for (var i = 0; i < response.update.length; i++) {
                    let id = response.update[i][0];
                    let state = response.update[i][1];
                    let time = response.update[i][2];
                    let oppositeState = state == 'on' ? 'off' : 'on';

                    $("#" + id + " p").html(formatState(state, time));
                    $("#" + id + "-zone").removeClass().addClass("sprinkler " + state + "-sprinkler");
                    let btn = $("#" + id + "-zone-button");
                    btn.text(oppositeState.toUpperCase());
                }
                setTimeout(poll, 2000);
            },
            // handle error
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                // try again in 10 seconds if there was a request error
                console.log("err " + errorThrown);
                setTimeout(poll, 10000);
            },
            //complete: poll,
            dataType: "json",
            timeout: 1000
        });
    }
}

setupNav = () => {
    $('.navigate.garage-page').click(function () {
        window.location.href = 'garage.html';
    });
    $('.navigate.irrigation-page').click(function () {
        window.location.href = 'irrigation.html';
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
};

$(document).ready(() => {
    uptime();   
    poll();
    setupNav();
    info();
});
