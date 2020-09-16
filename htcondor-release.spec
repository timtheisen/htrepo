Name:           htcondor-release
Version:        8.9
Release:        1%{?dist}
Summary:        HTCondor Software for Enterprise Linux repository configuration

License:        ASL 2.0
URL:            https://htcondor.org/

# This is an HTCondor Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.

Source0:        generate-repo-files.sh
Source1:        repo.template
Source2:        RPM-GPG-KEY-HTCondor

BuildArch:      noarch

%if 0%{?rhel}
Requires:       epel-release >= %{rhel}
%endif

%description
This package contains the HTCondor Software for Enterprise Linux repository
configuration for yum.

%prep
exit 0

%build
# generate .repo files for current rhel version
%if 0%{?rhel}
%define platformname "Enterprise Linux %{rhel}"
%define platform "el%{rhel}"
%endif

%if 0%{?fedora}
%define platformname "Fedora %{fedora}"
%define platform "fc%{fedora}"
%endif

# Amazon Linux needs to go after rhel (both are defined)
%if 0%{?amzn}
%define platformname "Amazon Linux %{amzn}"
%define platform "amzn%{amzn}"
%endif

%{SOURCE0} %{version} release     1 %{platform} %{platformname}
%{SOURCE0} %{version} testing     0 %{platform} %{platformname}
%{SOURCE0} %{version} development 0 %{platform} %{platformname}

%install

#GPG Key
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -pm 644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-HTCondor

# yum
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

install -m 644 *.repo $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -f *.repo

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-HTCondor

%changelog
* Wed Sep 14 2020 Tim Theisen <tim@cs.wisc.edu> - 8.9-1
- Bump release series number for development release

* Mon Sep 14 2020 Tim Theisen <tim@cs.wisc.edu> - 8.8-1
- Initial package

