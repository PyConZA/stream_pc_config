# stream-pc-config
Nix and other configuration files for PyConZA Stream PCs

## Setup new mac
1. Install nix with `curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install | sh`
2. Clone this config repo when in the home directory with `git clone https://github.com/PyConZA/stream_pc_config.git`
  1. Allow developer tools to be installed in order to use git.
3. Install nix-darwin: `nix run nix-darwin --extra-experimental-features "nix-command flakes" -- switch -- flake ~/nix#stream-pc`