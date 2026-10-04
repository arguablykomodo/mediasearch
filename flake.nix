{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs =
    inputs:
    inputs.flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import inputs.nixpkgs {
          inherit system;
          config.allowUnfree = true;
          config.cudaSupport = true;
        };
        dependencies = with pkgs.python3Packages; [
          peewee
          tqdm
          easyocr
          openai-whisper
        ];
      in
      {
        formatter = pkgs.nixfmt-tree;
        devShells.default = pkgs.mkShell {
          packages = [ pkgs.pyright ] ++ dependencies;
        };
        packages.default = pkgs.python3Packages.buildPythonApplication {
          pname = "mediasearch";
          version = "0.1.0";
          pyproject = true;
          src = ./.;
          build-system = with pkgs.python3Packages; [ setuptools ];
          dependencies = dependencies;
          meta = {
            description = "CLI program for indexing and searching through media files";
            homepage = "https://github.com/arguablykomodo/mediasearch";
            license = pkgs.lib.licenses.gpl3Plus;
            mainProgram = "mediasearch";
          };
        };
      }
    );
}
