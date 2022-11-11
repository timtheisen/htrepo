Name:           htcondor-release
Version:        10.0
Release:        1%{?dist}
Summary:        HTCondor Software for Enterprise Linux repository configuration

License:        ASL 2.0
URL:            https://htcondor.org/

# This is an HTCondor Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.

Source0:        generate-repo-files.sh
Source1:        repo.template
Source2:        HTCondor-10.0-Key
Source3:        HTCondor-10.0-Daily-Key

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

%{SOURCE0} %{version} release 1 %{platform} %{platformname}
%{SOURCE0} %{version} update  0 %{platform} %{platformname}
%{SOURCE0} %{version} rc      0 %{platform} %{platformname}
%{SOURCE0} %{version} daily   0 %{platform} %{platformname}

%install

#GPG Key
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -pm 644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-HTCondor-10.0
install -pm 644 %{SOURCE3} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-HTCondor-10.0-Daily

# yum
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

install -m 644 *.repo $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -f *.repo

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-HTCondor-10.0
/etc/pki/rpm-gpg/RPM-GPG-KEY-HTCondor-10.0-Daily

%changelog
* Thu Nov 10 2022 Tim Theisen <tim@cs.wisc.edu> - 10.0-1
- HTCondor 10.0 repository definition

* Wed Apr 28 2021 Tim Theisen <tim@cs.wisc.edu> - 9.1-1
- HTCondor 9.1 repository definition

* Wed Apr 21 2021 Tim Theisen <tim@cs.wisc.edu> - 9.0-3
- Daily key for 9.0

* Wed Apr 14 2021 Tim Theisen <tim@cs.wisc.edu> - 9.0-1
- New key for 9.0

* Thu Nov 19 2020 Tim Theisen <tim@cs.wisc.edu> - 8.9-3
- merge changes from 8.8

* Thu Nov 19 2020 Tim Theisen <tim@cs.wisc.edu> - 8.8-3
- latest renamed to current

* Sat Sep 19 2020 Tim Theisen <tim@cs.wisc.edu> - 8.9-2
- merge changes from 8.8

* Sat Sep 19 2020 Tim Theisen <tim@cs.wisc.edu> - 8.8-2
- development renamed to daily, testing renamed to rc

* Wed Sep 16 2020 Tim Theisen <tim@cs.wisc.edu> - 8.9-1
- Bump release series number for development release

* Mon Sep 14 2020 Tim Theisen <tim@cs.wisc.edu> - 8.8-1
- Initial package

