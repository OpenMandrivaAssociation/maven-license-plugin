%{?_javapackages_macros:%_javapackages_macros}
Name:           maven-license-plugin
Version:        1.8.0
Release:        17.1
Summary:        Maven plugin to update header licenses of source files
Group:		Development/Java

License:        ASL 2.0
URL:            http://code.google.com/p/maven-license-plugin
### upstream only provides binaries or source without build scripts
# tar creation instructions
# svn export http://maven-license-plugin.googlecode.com/svn/tags/maven-license-plugin-1.8.0 maven-license-plugin
# tar cfJ maven-license-plugin-1.8.0.tar.xz maven-license-plugin
Source0:        %{name}-%{version}.tar.xz
# remove testng dep (tests are skipped) and maven-license-plugin call
Patch0:         001-mavenlicenseplugin-fixbuild.patch
BuildArch:      noarch

BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  apache-resource-bundles
BuildRequires:  maven-local
BuildRequires:  maven-assembly-plugin
BuildRequires:  maven-deploy-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-source-plugin
BuildRequires:  maven-changelog-plugin
BuildRequires:  maven-changes-plugin
BuildRequires:  maven-clean-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-dependency-plugin
BuildRequires:  maven-help-plugin
BuildRequires:  maven-idea-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-pmd-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-repository-plugin
BuildRequires:  maven-remote-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-shared
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  maven-release-plugin
BuildRequires:  plexus-utils
BuildRequires:  plexus-classworlds
BuildRequires:  xml-commons-apis
BuildRequires:  xmltool

Requires:       java
Requires:       jpackage-utils
Requires:       maven
Requires:       maven-shared
Requires:       xmltool

%description
maven-license-plugin is a Maven plugin that help you managing license
headers in source files. Basically, when you are developing a project
either in open source or in a company, you often need to add at the top
of your source files a license to protect your work.
This plugin lets you maintain the headers, including checking if the
header is present, generating a report and of course having the
possibility to update / reformat missing license headers.


%package javadoc
Summary:        Javadocs for %{name}

Requires:       jpackage-utils
BuildArch:      noarch

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{name}
%patch0 -p1
# fix EOL
sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' NOTICE.txt

# Remove wagon-webdav extension which is not available
%pom_xpath_remove pom:build/pom:extensions

%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc NOTICE.txt LICENSE.txt

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 03 2013 Guido Grazioli <guido.grazioli@gmail.com> - 1.8.0-14
- Fix FTBFS

* Tue Feb 26 2013 Tomas Radej <tradej@redhat.com> - 1.8.0-13
- Reintroduced B/R on maven-shared

* Mon Feb 18 2013 Tomas Radej <tradej@redhat.com> - 1.8.0-12
- Removed BR on maven-shared (unnecessary + blocking maven-shared retirement)
- Remove wagon-webdav extension which is not available

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.8.0-10
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.8.0-8
- Remove maven-eclipse-plugin requirement to simplify build

* Tue Apr 17 2012 Tomas Radej <tradej@redhat.com> - 1.8.0-7
- Apache-resource-bundles BR
- Guidelines fixes

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 5 2011 Alexander Kurtakov <akurtako@redhat.com> 1.8.0-5
- Adapt to current guidelines.

* Fri Jun 24 2011 Guido Grazioli <guido.grazioli@gmail.com> - 1.8.0-4
- Fix FTBFS
- Update to maven 3
- Adapt to current guidelines

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 17 2010 Guido Grazioli <guido.grazioli@gmail.com> - 1.8.0-2
- Add missing Requires and update BuildRequires
- Fix macro usage

* Sat Oct 02 2010 Guido Grazioli <guido.grazioli@gmail.com> - 1.8.0-1
- Upstream version 1.8.0

* Sat May 08 2010 Guido Grazioli <guido.grazioli@gmail.com> - 1.6.1-1
- Initial packaging
