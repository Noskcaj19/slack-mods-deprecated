// A collection of utilities to make modifing Slack more easy

/**
 * Registers a client side Slack command
 *
 * @param {String} cmd - Name of the command to register
 * @param {Object} opts - Object with various options for the function
 */
function addCommand(cmd, opts) {
  opts.type = opts.type || "client"
  TS.cmd_handlers[cmd] = opts;
}

/**
 * Displays a message to the user from Slackbot
 *
 * @param {String} msg - Message to display, markdown is supported
 */
function ephemeralMessage(msg) {
    TS.cmd_handlers.addEphemeralFeedback(msg);
}

/**
 * Adds an external js file
 *
 * @param {String} url - Url of the resource to add
 */
function addDependency(url) {
    $("<script />", {src: url}).appendTo('head');
}