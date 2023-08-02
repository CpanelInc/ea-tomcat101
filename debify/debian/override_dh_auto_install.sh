#!/bin/bash

source debian/vars.sh

mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat101
cp $SOURCE1 $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat101/ea-podman-local-dir-setup
cp $SOURCE2 $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat101/README.md
cp $SOURCE3 $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat101/test.jsp
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat101/user-conf
cp -r ./conf/* $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat101/user-conf
cp $SOURCE1 $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat101/ea-podman-local-dir-setup
cp $SOURCE2 $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat101/README.md
cp $SOURCE3 $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat101/test.jsp
echo -n "$version-$release_prefix" > $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat101/pkg-version
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat101/bin
cat << EOF > ea-podman.json
{
    "ports" : [8080, 8009],
    "image" : "docker.io/library/tomcat:$version",
    "startup" : {
        "-e" : ["CATALINA_OPTS=-Xmx100m", "CATALINA_BASE=/usr/local/tomcat"],
        "-v" : [
            "conf:/usr/local/tomcat/conf",
            "logs:/usr/local/tomcat/logs",
            "webapps:/usr/local/tomcat/webapps"
        ]
    }
}
EOF
cp ea-podman.json $DEB_INSTALL_ROOT/opt/cpanel/ea-tomcat101/ea-podman.json
