import os
import sys
import re
import shutil
import argparse

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

def strip_code(script):
    return re.sub("\n?\n?////SLACK MODS START////.*////SLACK MODS END////", "", script, flags=re.S)

def uninstall(verbose=False):
    install_path = get_slack_install_path()
    if not verify_install_path(install_path):
        print("Unable to locate valid Slack install path")
        exit(1)
    ssb = install_path + '/ssb-interop.js'
    backup_path = install_path + '/ssb-interop-backup.js'

    if not os.path.exists(backup_path):
        print("Unable to locate backup preload script, attempting to scrub code")
        with open(ssb, 'r') as f:
            clean = strip_code(f.read())
        with open(ssb, 'w') as f:
            f.write(clean)
        shutil.copymode(install_path + "/ssb-interop-lite.js", ssb)
    else:
        if verbose:
            print("Replacing preload script with backup")
        shutil.copyfile(backup_path, ssb)
        shutil.copymode(backup_path, ssb)
    print("Uninstalled slack-mods")

def install(verbose=False):
    install_path = get_slack_install_path()
    if not verify_install_path(install_path):
        print("Unable to locate valid Slack install path")
        exit(1)
    ssb = install_path + '/ssb-interop.js'
    print("Installing to {}".format(ssb))

    # Check if slack-mods is already installed
    with open(ssb) as f:
        content = f.read()
        if "////SLACK MODS START////" in content:
            print("Detected existing install, exiting.")
            exit(1)

    # Make a backup
    backup_path = install_path + '/ssb-interop-backup.js'
    if verbose:
        print("Making backup preload script at {}", backup_path)
    shutil.copyfile(ssb, backup_path)
    shutil.copymode(ssb, backup_path)

    # Do the install
    with open(ssb, 'a') as f:
        f.write(preload_script)

    # Create mod folder if it does not exist
    mods_path = os.path.expanduser("~/.slack_mods")
    if not os.path.exists(mods_path):
        print("`~/.slack_mods` does not exist, creating it now")
        os.makedirs(mods_path)
    elif verbose:
        print("`~/.slack_mods` already exists")

    print("Slack mods has been installed. Please quit and reopen Slack.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action='store_true', help='Uninstall slack-mods')
    parser.add_argument('-v', action='store_true', help='Enable verbose printing')
    args = parser.parse_args()
    if not args.u:
        install(args.v)
    else:
        uninstall(args.v)


preload_script = """

////SLACK MODS START////
// ** slack-plugins ** https://github.com/Noskcaj19/slack-mods
try {
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
} catch (e) {
    console.error(e);
}
////SLACK MODS END////"""


if __name__ == '__main__':
    main()