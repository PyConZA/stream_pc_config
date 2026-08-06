# stream-pc-config
Nix and other configuration files for PyConZA Stream PCs

## Setup new mac
1. Install nix with `curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install | sh`
2. Clone this config repo when in the home directory with `git clone https://github.com/PyConZA/stream_pc_config.git`
  1. Allow developer tools to be installed in order to use git.
3. Move pre-existing managed config files that will cause nix-darwin to abort installation:
  1. `sudo mv /etc/bashrc /etc/bashrc.before-nix-darwin && sudo mv /etc/zshenv /etc/zshenv.before-nix-darwin`
4. Install nix-darwin: `sudo nix run nix-darwin --extra-experimental-features "nix-command flakes" -- switch --flake ~/stream_pc_config#stream-pc`