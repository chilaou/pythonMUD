var STATS = {
    lines_input: 0,
    //lines_output: 0
}


function doConsoleInput() {
    var msg = takeConsoleInput();
    if (STATS.lines_input % 3 == 0) {
        setTimeout(outputToConsole, 3000, "THREEEEEE!");
    }
    outputToConsole(msg);
    return false; // Prevents refresh
}

function takeConsoleInput() {
    var cIn = document.getElementById("console-in");
    var msg = cIn.value;
    STATS.lines_input++;
    cIn.value = "";
    return msg;
}

function outputToConsole(msg) {
    var cOut = document.getElementById("console-out");
    incStat("lines_output");
    cOut.value += "\n(" + STATS.lines_input + ", " + STATS.lines_output + "): " + msg;
}

function incStat(key) {
    if (isNaN(STATS[key])) {
        STATS[key] = 0;
    }
    return STATS[key]++;
}
