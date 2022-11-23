{
  inputs = {
    nixpkgs = { url = "github:nixos/nixpkgs/nixos-22.05"; };
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";

      pkgs = import nixpkgs {
        inherit system;
        overlays = [ self.overlays.default ];
      };

    in rec {
      packages."${system}" = {
        impala = pkgs.callPackage ({ buildGoModule }:
          buildGoModule rec {
            pname = "impala";
            version = "2.0.0";

            src = ./.;
            ldflags = [ "-X github.com/wuvt/impala.Version=${version}" ];

            vendorSha256 = "sha256-BS99ODdA54SUqVNdwi/2OIvILIDGm8hk/XBaWl4sHjY=";
          }
        ) {};

        default = packages."${system}".impala;
      };

      overlays.default = final: prev: self.packages."${system}";
    };
}
