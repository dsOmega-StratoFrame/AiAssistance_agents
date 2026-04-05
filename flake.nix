{
  description = "Flake with aider-chat installed as Python dependency";

  inputs = {
    systems.url = "github:nix-systems/x86_64-linux";
    flake-utils.url = "github:numtide/flake-utils";
    flake-utils.inputs.systems.follows = "systems";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
        };
        aider-chat-no-tests = pkgs.aider-chat.overridePythonAttrs (old: {
          # Some tests related to `max_input_tokens` are impure and require network connection.
          # We could use `--impure --sandbox false` but I decided to ditch it.
          doCheck = false;
        });
      in rec {
        # enables use of `nix shell`
        devShell = pkgs.mkShell {
          # add things you want in your shell here
          buildInputs = [
            aider-chat-no-tests
          ];
        };
      }
    );
}
