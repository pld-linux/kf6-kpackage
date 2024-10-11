#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.7
%define		qtver		5.15.2
%define		kfname		kpackage

Summary:	Library to load and install packages as plugins
Name:		kf6-%{kfname}
Version:	6.7.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	b1beccbf7acc2c91c3952e0f818e69a0
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-karchive-devel >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	kf6-kdoctools-devel >= %{version}
BuildRequires:	kf6-ki18n-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Core >= %{qtver}
Requires:	Qt6DBus >= %{qtver}
Requires:	kf6-dirs
Requires:	kf6-karchive >= %{version}
Requires:	kf6-kcoreaddons >= %{version}
Requires:	kf6-ki18n >= %{version}
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Library to load and install packages as plugins.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	kf6-kcoreaddons-devel >= %{version}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/qt6/plugins/kpackage/packagestructure
%ninja_install -C build

%find_lang lib%{kfname}6

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f lib%{kfname}6.lang
%defattr(644,root,root,755)
%doc README.md
%{_datadir}/qlogging-categories6/kpackage.categories
%attr(755,root,root) %{_bindir}/kpackagetool6
%ghost %{_libdir}/libKF6Package.so.6
%attr(755,root,root) %{_libdir}/libKF6Package.so.*.*
%dir %{_libdir}/qt6/plugins/kpackage
%dir %{_libdir}/qt6/plugins/kpackage/packagestructure
%{_mandir}/man1/kpackagetool6.1*
%lang(ca) %{_mandir}/ca/man1/kpackagetool6.1*
%lang(es) %{_mandir}/es/man1/kpackagetool6.1*
%lang(it) %{_mandir}/it/man1/kpackagetool6.1*
%lang(nl) %{_mandir}/nl/man1/kpackagetool6.1*
%lang(pt_BR) %{_mandir}/pt_BR/man1/kpackagetool6.1*
%lang(sl) %{_mandir}/sl/man1/kpackagetool6.1*
%lang(uk) %{_mandir}/uk/man1/kpackagetool6.1*
%lang(fr) %{_mandir}/fr/man1/kpackagetool6.1*
%{_datadir}/qlogging-categories6/kpackage.renamecategories
%lang(tr) %{_mandir}/tr/man1/kpackagetool6.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KPackage
%{_libdir}/cmake/KF6Package
%{_libdir}/libKF6Package.so
