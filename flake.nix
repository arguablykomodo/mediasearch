{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };
  outputs =
    {
      nixpkgs,
      ...
    }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
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
      formatter.${system} = pkgs.nixfmt-tree;
      devShells.${system}.default = pkgs.mkShell {
        packages = [ pkgs.pyright ] ++ dependencies;
      };
      packages.${system}.default = pkgs.python3Packages.buildPythonApplication {
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
    };
}
