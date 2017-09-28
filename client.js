var STATS = {} // An object, but it works kinda like a Python dict

function doConsoleInput() {
    var msg = takeConsoleInput();
    if (STATS.lines_input % 3 == 0) { // This is just a dumb example of async output
        setTimeout(outputToConsole, 3000, "THREEEEEE!");
    }
    outputToConsole(msg);
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
    cOut.value += "\n(" + STATS.lines_input + ", " + STATS.lines_output + "): " + msg;
    incStat("lines_output");
}

function incStat(key) {
    if (isNaN(STATS[key])) { // Right now, we assume STATS is strictly str->int
        STATS[key] = 0;      // If used on a non-int stat, this will overwrite it.
    }
    return STATS[key]++;
}

