var STATS = {} // An object, but it works kinda like a Python dict


function doConsoleInput() {
    STATS["last_input_time"] = (new Date()).getTime();
    var cmd = takeConsoleInput();
    // Sanitization can happen here, or in takeConsoleInput?

    var parts = cmd.split(" ");
    switch(parts[0].toLowerCase()) {
        case "airplane":
            doAirplane(cmd);
            break;
        case "~stats":
            outputToConsole(JSON.stringify(STATS));
            break;
        default:
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
    setTimeout(function() { cOut.style.backgroundColor="#FFF"; },3000);
    setTimeout(doAirplane2, 5000);
}

function doAirplane2(cmd) { // Notice how this is _after_ a reference to it above. Lazy execution!
    var xh = new XMLHttpRequest(); // Poorly named, this is ANY async request now
    var url = "https://raw.githubusercontent.com/chilaou/pythonMUD/master/stub.txt";
    // We can't access a local file with this, because JS is VERY strict about file access 
    xh.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) { // It needs to be 'finished' + OK
            var response = JSON.parse(this.responseText); // 'this' needs explaining LOL
            incStat("async_msg_recv");
            for (var i = 0; i < response.length; i++) {
                doServerCommand(response[i]);
            }
        }
        // Anything here will run a lot more, because a request changes state a LOT
        incStat("async_state_updates");        
    }
    xh.open("GET", url, true); // I don't know what true means, I think that's the async
    xh.send();
    incStat("async_msg_sent");
    // Notice how we have to give it the instructions first, then send it off. 
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

