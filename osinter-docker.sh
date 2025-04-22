# OUTPUTS SCAN DATA TO ~/.osinter/scans

docker run --rm -it -v "$HOME/.osinter/scans:/root/.osinter/scans" -v "$HOME/.config/osinter:/root/.config/osinter" blacklanternsecurity/osinter:stable "$@"
