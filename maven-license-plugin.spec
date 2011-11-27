Name:           maven-license-plugin
Version:        1.8.0
Release:        5
Summary:        Maven plugin to update header licenses of source files

Group:          Development/Java
License:        ASL 2.0
URL:            http://code.google.com/p/maven-license-plugin
### upstream only provides binaries or source without build scripts
# tar creation instructions
# svn export http://maven-license-plugin.googlecode.com/svn/tags/maven-license-plugin-1.8.0 maven-license-plugin
# tar cfJ maven-license-plugin-1.8.0.tar.xz maven-license-plugin 
Source0:        %{name}-%{version}.tar.xz
# custom depmap needed to workaround missing xml-commons-apis poms
Source1:        maven-license-plugin-jpp-depmap.xml
# remove testng dep (tests are skipped) and maven-license-plugin call
Patch0:         001-mavenlicenseplugin-fixbuild.patch
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  maven2
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
BuildRequires:  maven-eclipse-plugin
BuildRequires:  maven-help-plugin
BuildRequires:  maven-idea-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-pmd-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-repository-plugin
BuildRequires:  maven-remote-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-shared
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  maven-release-plugin
BuildRequires:  plexus-utils
BuildRequires:  plexus-classworlds
BuildRequires:  xml-commons-apis
BuildRequires:  xmltool

Requires:       java 
Requires:       jpackage-utils
Requires:       maven2
Requires:       xmltool

Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

%description
maven-license-plugin is a Maven 2 plugin that help you managing license 
headers in source files. Basically, when you are developing a project 
either in open source or in a company, you often need to add at the top 
of your source files a license to protect your work. 
This plugin lets you maintain the headers, including checking if the 
header is present, generating a report and of course having the 
possibility to update / reformat missing license headers. 


%package javadoc
Summary:        Javadocs for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
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


%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
  -e \
  -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
  -Dmaven2.jpp.depmap.file=%{SOURCE1} \
  -Dmaven.test.skip=true \
  install javadoc:aggregate


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_javadir}
install -Dp -m 644 target/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && ln -sf %{name}-%{version}.jar %{name}.jar)

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -rp target/site/apidocs/  \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -sf %{name}-%{version} %{name})

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_to_maven_depmap com.mycila.maven-license-plugin %{name} %{version} JPP %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc NOTICE.txt LICENSE.txt
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*


%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}
%{_javadocdir}/%{name}-%{version}


%post
%update_maven_depmap

%postun
%update_maven_depmap

