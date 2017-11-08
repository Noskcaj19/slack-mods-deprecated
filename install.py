import os
import sys

COMMON_LINUX_SLACK_LOCATIONS = [
    "/usr/lib/slack/resources/app.asar.unpacked/src/static",
    "/usr/local/lib/slack/resources/app.asar.unpacked/src/static",
    "/opt/slack/resources/app.asar.unpacked/src/static",
]

def get_slack_install_path():
    if sys.platform == 'darwin':
        return '/Applications/Slack.app/Contents/Resources/app.asar.unpacked/src/static'
    else:
        for location in COMMON_LINUX_SLACK_LOCATIONS:
            if os.path.exists(location):
                return location

def verify_install_path(path):
    if not os.path.exists(path):
        return False
    if not os.path.exists(path + '/ssb-interop.js'):
        return False
    return True


def main():
    install_path = get_slack_install_path()
    if not verify_install_path(install_path):
        print("Unable to locate valid Slack install path")
        exit(1)
    ssb = install_path + '/ssb-interop.js'
    with open(ssb) as f:
        content = f.read()
        if "////SLACK MODS START////" in content:
            print("Detected existing install, exiting.")
            exit(1)
    with open(ssb, 'a') as f:
        f.write(launch_script)

    mods_path = os.path.expanduser("~/.slack_mods")
    if not os.path.exists(mods_path):
        os.makedirs(mods_path)
    print("Slack mods has been installed. Please quit and reopen Slack.")

launch_script = """

////SLACK MODS START////
// ** slack-plugins ** https://github.com/Noskcaj19/slack-mods
const fs = require('fs');

const stdPath = 'https://rawgit.com/Noskcaj19/slack-mods/master/mod_lib.js'
const modsPath = path.join(require('os').homedir(), '.slack_mods')
document.addEventListener('DOMContentLoaded', function() {
  $("<script />", {src: stdPath}).appendTo('head');

  fs.readdir(modsPath, (err, files) => {
    files.forEach(file => {
      if (path.extname(file) === ".js") {
        fs.readFile(path.join(modsPath, file), 'utf8', (e, r) => {
          if (e) {
            console.err(e); 
          } else {
            try {
              eval(r)
            } catch(e) {
              console.error(e)
            } 
            console.info(`Loaded mod from: ${path.join(modsPath, file)}`);
          };
        })
      };
    });
  });
});
////SLACK PLUGINS END////"""


if __name__ == '__main__':
    main()