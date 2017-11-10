# Slack Mods

[Slack](https://slack.com) is great, but I wanted to be able to inject some Javascript to change a few things.

Any Javascript files in `~/.slack_mods/` will be injected into the main view at startup

Also, any CSS files `~/.slack_mods/` will be loaded at startup

Some example mods are included in the examples folder, such as LaTeX rendering

# Install

Just run `python install.py`

Unfortunately, it will be uninstalled on every Slack update

# Uninstall

To uninstall, just run `python install.py -u`