/**
* Add a new command `reload` which reloads the page for easy debugging
*/
addCommand("/reload", {
    desc: "Reload the Slack window",
    func: function reload() {
        window.location = '';
    }
});

/**
* Modify the global slack object to expose the devtools command
*/
TS.cmd_handlers['/slackdevtools'].autocomplete = true;
TS.cmd_handlers['/slackdevtools'].desc = "Open Chromium DevTools";