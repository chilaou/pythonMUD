var STATS = {} // An object, but it works kinda like a Python dict


function doConsoleInput() {
    STATS["last_input_time"] = (new Date()).getTime();
    var cmd = takeConsoleInput();
    // Sanitization can happen here, or in takeConsoleInput?
    /*  This looks like the point at which I would look to take the input I've been
        given and do something with it in the Python script. For the special cases
        Jake lined out below, those are commands that won't even make it into the
        Python script, because I'll only pick up things that enter the default case.
        I could also have my game return if something was a bad input, rather than
        assuming that if it makes it to the default case, it's a bad input.
    */

    var parts = cmd.split(" ");
    switch(parts[0].toLowerCase()) {
        case "airplane":
            doAirplane(cmd);
            break;
        case "poll":
            doPoll(cmd);
            break;
        case "~stats":
            outputToConsole(JSON.stringify(STATS));
            break;
        default:
            outputToConsole("Kay you said the first part was: " + parts[0]);
            outputToConsole("WTF is `" + cmd + "` supposed to mean?");
            doBadInput();
            break;
    }

    // This stat is crap if most commands are sub-millisecond.
    incStat("total_processing_time", (new Date()).getTime()-STATS.last_input_time);
    return false; // Prevents page refresh
}

function takeConsoleInput() {
    var cIn = document.getElementById("console-in");
    var msg = cIn.value;
    cIn.value = ""; // Clears out the input so the user can type next command
    incStat("lines_input");
    return msg;
}

function outputToConsole(msg) {
    var cOut = document.getElementById("console-out");
    incStat("lines_output");
    cOut.value += "\n" + msg;
    cOut.scrollTop = cOut.scrollHeight - cOut.clientHeight;
}

function incStat(key, amt = 1) { // Default parameter, syntactic sugar
    if (isNaN(STATS[key])) { // Right now, we assume STATS is strictly str->int
        STATS[key] = 0;      // If used on a non-int stat, this will overwrite it.
    }
    return STATS[key] += amt;
}

function doBadInput() {
    var cIn = document.getElementById("console-in");
    cIn.style.backgroundColor="#FDD"; // Most visual changes should be handled with class changes (classList)
    setTimeout(function() { cIn.style.backgroundColor="#FFF"; },200); // This is an "anonymous function"
    // (But wait, how did I refer to cIn inside that anonymous function? The magic of closures!)
    incStat("bad_inputs");
}


function doAirplane(cmd) {
    outputToConsole("You activated the airplane with: `" + cmd + "`!!!");
    incStat("airplanes_activated");
    var cOut = document.getElementById("console-out");
    cOut.style.backgroundColor="#AEF";
    setTimeout(function() { cOut.style.backgroundColor="#000"; },3000);
    setTimeout(doAirplane2, 5000, cmd);
}

function doAirplane2(cmd) {
    doAsyncRequest(cmd, "http://localhost:7777/airplane");
}

function doPoll(cmd) {
    doAsyncRequest(cmd, "http://localhost:7777/poll");
    incStat("polls_sent");
}

function doAsyncRequest(cmd, url) {
    var xh = new XMLHttpRequest();
    xh.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            incStat("async_msg_recv");
            for (var i = 0; i < response.length; i++) {
                doServerCommand(response[i]);
            }
        }
    }
    xh.open("GET", url, true);
    xh.send();
    incStat("async_msg_sent");
}

function doServerCommand(cmd) {
    switch(cmd.type) {
        case "console-out":
            outputToConsole(cmd.data.msg);
            break;
        case "console-in-flash":
            doConsoleInFlash(Number(cmd.data.speed), cmd.data.seq);
            break;
        default:
            outputToConsole("ERROR: BAD SERVER CMD " + String(cmd));
            incStat("bad_server_commands");
            break;
    }
    incStat("server_commands_processed");
}

function doConsoleInFlash(speed, seq) {
    if (seq.length > 0) {
        var nxt = seq.splice(0, 1); // This pops an array of size 1, starting at index 0.
        var cIn = document.getElementById("console-in");
        cIn.style.backgroundColor = nxt[0]; // Even though it's 1 thing, it's an array
        setTimeout(doConsoleInFlash, speed, speed, seq);
        // This doesn't go forever because we chop something off seq each time.
    }
}

