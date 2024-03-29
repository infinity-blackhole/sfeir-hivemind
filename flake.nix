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
                black.enable = true;
                isort.enable = true;
                terraform-format.enable = true;
                hadolint.enable = true;
              };
              env = {
                OPENLLM_LLAMA_MODEL_ID = "NousResearch/Llama-2-7b-chat-hf";
                OPENLLM_LLAMA_FRAMEWORK = "pt";
              };
              packages = [
                pkgs.nixpkgs-fmt
                pkgs.stdenv.cc.cc.lib
                pkgs.python310
                pkgs.nodejs
                pkgs.glab
                pkgs.gh
                pkgs.docker
                pkgs.terraform
                pkgs.skaffold
                pkgs.hatch
                pkgs.cudaPackages.cudatoolkit
                pkgs.cudaPackages.cudnn
                pkgs.cudaPackages.tensorrt
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
