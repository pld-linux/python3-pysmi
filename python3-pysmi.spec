#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	pysmi
Summary:	SNMP SMI/MIB parser
Summary(pl.UTF-8):	Analizator składniowy SNMP SMI/MIB
Name:		python3-%{module}
Version:	2.0.0
Release:	1
License:	BSD
Group:		Libraries/Python
# PyPI sdist lacks tests and examples
Source0:	https://github.com/lextudio/pysmi/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	a6ef4681cc4861307129a3b4bd74c3f7
URL:		https://www.pysnmp.com/pysmi/
BuildRequires:	python3 >= 1:3.10
BuildRequires:	python3-build
BuildRequires:	python3-flit_core >= 3.9.0
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.10
%if %{with tests}
BuildRequires:	python3-jinja2 >= 3.1.3
BuildRequires:	python3-lark >= 1.1.9
BuildRequires:	python3-pysnmp >= 7.1.16
BuildRequires:	python3-pytest >= 6.2.5
BuildRequires:	python3-requests >= 2.26.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A pure-Python implementation of SNMP/SMI MIB parsing and conversion
library. It can turn ASN.1 MIBs into pysnmp Python modules or JSON
documents.

%description -l pl.UTF-8
Napisana w czystym Pythonie biblioteka do analizy składniowej i
konwersji MIB-ów SNMP/SMI. Potrafi przekształcić MIB-y ASN.1 w moduły
Pythona dla pysnmp lub dokumenty JSON.

%package examples
Summary:	Example programs for Python pysmi module
Summary(pl.UTF-8):	Programy przykładowe do modułu Pythona pysmi
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description examples
This package contains example programs for Python pysmi module.

%description examples -l pl.UTF-8
Ten pakiet zawiera przykładowe programy do modułu Pythona pysmi.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}

%py3_install_pyproject

cp -a examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.rst README.md THANKS.txt TODO.txt
%attr(755,root,root) %{_bindir}/mibcopy
%attr(755,root,root) %{_bindir}/mibdump
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
