%global ns_dir /opt/cpanel

# OBS builds the 32-bit targets as arch 'i586', and more typical
# 32-bit architecture is 'i386', but 32-bit archive is named 'x86'.
# 64-bit archive is 'x86-64', rather than 'x86_64'.
%if "%{_arch}" == "i586" || "%{_arch}" == "i386"
%global archive_arch x86
%else
%if "%{_arch}" == "x86_64"
%global archive_arch x86-64
%else
%global archive_arch %{_arch}
%endif
%endif

%if 0%{?centos} >= 7 || 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

Name:    ea-tomcat101
Vendor:  cPanel, Inc.
Summary: Tomcat
Version: 10.1.34
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: Apache License, 2.0
Group:   System Environment/Daemons
URL: http://tomcat.apache.org/

Source0: https://www-us.apache.org/dist/tomcat/tomcat-8/v%{version}/bin/apache-tomcat-%{version}.tar.gz
Source1: ea-podman-local-dir-setup
Source2: README.md
Source3: test.jsp
Source4: pkg.prerm

# if I do not have autoreq=0, rpm build will recognize that the ea_
# scripts need perl and some Cpanel pm's to be on the disk.
# unfortunately they cannot be satisfied via the requires: tags.
Autoreq: 0

Requires: ea-apache24-mod_proxy_ajp
Requires: ea-podman

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.

Tomcat is developed in an open and participatory environment and
released under the Apache Software License version 2.0. Tomcat is intended
to be a collaboration of the best-of-breed developers from around the world.

%prep
%setup -qn apache-tomcat-%{version}

%build
# empty build section

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat101
cp %{SOURCE1} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat101/ea-podman-local-dir-setup
cp %{SOURCE2} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat101/README.md
cp %{SOURCE3} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat101/test.jsp
echo -n "%{version}-%{release_prefix}" > $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat101/pkg-version

mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat101/user-conf
cp -r ./conf/* $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat101/user-conf

cp %{SOURCE1} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat101/ea-podman-local-dir-setup
cp %{SOURCE2} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat101/README.md
cp %{SOURCE3} $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat101/test.jsp

mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat101/bin

cat << EOF > $RPM_BUILD_ROOT/opt/cpanel/ea-tomcat101/ea-podman.json
{
    "ports" : [8080, 8009],
    "image" : "docker.io/library/tomcat:%{version}",
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

%preun

%include %{SOURCE4}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/cpanel/ea-tomcat101
%attr(0655,root,root) /opt/cpanel/ea-tomcat101
%attr(0755,root,root) /opt/cpanel/ea-tomcat101/ea-podman-local-dir-setup
%attr(0644,root,root) /opt/cpanel/ea-tomcat101/ea-podman.json
%attr(0644,root,root) /opt/cpanel/ea-tomcat101/README.md
%attr(0644,root,root) /opt/cpanel/ea-tomcat101/test.jsp
%attr(0644,root,root) /opt/cpanel/ea-tomcat101/pkg-version

%changelog
* Tue Dec 10 2024 Cory McIntire <cory@cpanel.net> - 10.1.34-1
- EA-12606: Update ea-tomcat101 from v10.1.33 to v10.1.34
- CVE-2024-54677: Apache Tomcat: DoS in examples web application
- CVE-2024-50379: Apache Tomcat: RCE due to TOCTOU issue in JSP compilation

* Mon Nov 18 2024 Cory McIntire <cory@cpanel.net> - 10.1.33-1
- EA-12555: Update ea-tomcat101 from v10.1.30 to v10.1.33
- CVE-2024-52316: Apache Tomcat: Authentication bypass when using Jakarta Authentication API
- CVE-2024-52317: Apache Tomcat: Request/response mix-up with HTTP/2
- CVE-2024-52318: Apache Tomcat: Incorrect JSP tag recycling leads to XSS

* Tue Sep 17 2024 Cory McIntire <cory@cpanel.net> - 10.1.30-1
- EA-12394: Update ea-tomcat101 from v10.1.28 to v10.1.30

* Tue Aug 06 2024 Cory McIntire <cory@cpanel.net> - 10.1.28-1
- EA-12325: Update ea-tomcat101 from v10.1.26 to v10.1.28

* Thu Jul 18 2024 Cory McIntire <cory@cpanel.net> - 10.1.26-1
- EA-12290: Update ea-tomcat101 from v10.1.24 to v10.1.26

* Mon May 13 2024 Cory McIntire <cory@cpanel.net> - 10.1.24-1
- EA-12147: Update ea-tomcat101 from v10.1.20 to v10.1.24

* Wed Apr 10 2024 Cory McIntire <cory@cpanel.net> - 10.1.20-1
- EA-12081: Update ea-tomcat101 from v10.1.10 to v10.1.20

* Thu Mar 28 2024 Dan Muey <dan@cpanel.net> - 10.1.10-2
- ZC-11732: Add SSL and Port information. Clarify role in support and docs

* Mon Jul 31 2023 Julian Brown <julian.brown@cpanel.net> - 10.1.10-1
- ZC-11053: Initial Build

