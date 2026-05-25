#!/bin/bash
set -e

DIR="/tmp/sqleasy-deb"
rm -rf "$DIR"
mkdir -p "$DIR/DEBIAN"
mkdir -p "$DIR/usr/bin"
mkdir -p "$DIR/usr/share/sqleasy/core"

cat << 'EOF' > "$DIR/DEBIAN/control"
Package: sqleasy
Version: 1.1.0
Section: utils
Priority: optional
Architecture: all
Depends: python3, sqlmap, unzip, wget, git
Maintainer: syed-sameer-ul-hassan <syed-sameer-ul-hassan@github>
Description: SQL Easy Automated Penetration Testing Framework
 High-performance automated reconnaissance and SQL injection exploitation orchestration pipeline.
EOF

cp -r core/* "$DIR/usr/share/sqleasy/core/"
cp main.py "$DIR/usr/share/sqleasy/"
cp start.py "$DIR/usr/share/sqleasy/"
cp uninstall.py "$DIR/usr/share/sqleasy/"
cp requirements.txt "$DIR/usr/share/sqleasy/"

cp sqleasy "$DIR/usr/bin/sqleasy"
chmod +x "$DIR/usr/bin/sqleasy"

dpkg-deb --root-owner-group --build "$DIR" sqleasy.deb
echo "[+] Debian package 'sqleasy.deb' built successfully!"
