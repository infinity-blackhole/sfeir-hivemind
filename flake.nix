{
  description = "Sfeir Hivemind";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/release-23.05";
    devenv = {
      url = "github:cachix/devenv";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  nixConfig = {
    extra-public-keys = [
      "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw="
    ];
    extra-substituters = [
      "https://devenv.cachix.org"
    ];
  };

  outputs = { nixpkgs, devenv, ... }@inputs: {
    devShells = nixpkgs.lib.genAttrs nixpkgs.lib.platforms.unix (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
      in
      {
        default = devenv.lib.mkShell {
          inherit inputs pkgs;
          modules = [
            {
              pre-commit.hooks = {
                actionlint.enable = true;
                markdownlint.enable = true;
                shellcheck.enable = true;
                shfmt.enable = true;
                nixpkgs-fmt.enable = true;
                statix.enable = true;
                deadnix.enable = true;
                hadolint.enable = true;
              };
              packages = [
                pkgs.nixpkgs-fmt
                pkgs.docker
                pkgs.nodejs
                pkgs.glab
                pkgs.gh
                pkgs.skaffold
                pkgs.openjdk
              ];
            }
            {
              pre-commit.hooks = {
                black.enable = true;
                isort.enable = true;
                terraform-fmt.enable = true;
              };
              packages = [
                pkgs.terraform
                pkgs.hatch
                pkgs.cudaPackages.cudatoolkit
                pkgs.cudaPackages.cudnn
                (pkgs.google-cloud-sdk.withExtraComponents [
                  pkgs.google-cloud-sdk.components.alpha
                  pkgs.google-cloud-sdk.components.beta
                  pkgs.google-cloud-sdk.components.log-streaming
                  pkgs.google-cloud-sdk.components.cloud-run-proxy
                  pkgs.google-cloud-sdk.components.gsutil
                ])
              ];
            }
          ];
        };
      }
    );
  };
}
