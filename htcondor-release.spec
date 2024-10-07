%if 0%{?suse_version}
%if %{suse_version} == 1500
%define dist .leap15
%endif
%endif

Name:           htcondor-release
Version:        24.x
Release:        1%{?dist}
Summary:        HTCondor Software for Enterprise Linux repository configuration

License:        ASL 2.0
URL:            https://htcondor.org/

# This is an HTCondor Software maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.

Source0:        generate-repo-files.sh
Source1:        repo.template
Source2:        RPM-GPG-KEY-OSG-24-dev
Source3:        RPM-GPG-KEY-OSG-24-auto
Source4:        RPM-GPG-KEY-OSG-23-developer
Source5:        RPM-GPG-KEY-OSG-23-auto

BuildArch:      noarch

%if 0%{?rhel} && ! 0%{?amzn}
Requires:       epel-release = %{rhel}
%endif

%description
Repository definitions for the HTCondor Software Suite

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

%define packager yum.
%if 0%{?suse_version}
%define packager zypp/
%if %{suse_version} == 1500
%define platformname "openSUSE Leap 15"
%define platform "leap15"
%define dist .leap15
%endif
%endif

# Amazon Linux needs to go after rhel (both are defined)
%if 0%{?amzn}
%define platformname "Amazon Linux %{amzn}"
%define platform "amzn%{amzn}"
%endif

%{SOURCE0} %{version} snapshot 0 %{platform} %{platformname}
%{SOURCE0} %{version} alpha    0 %{platform} %{platformname}
%{SOURCE0} %{version} beta     0 %{platform} %{platformname}
%{SOURCE0} %{version} release  1 %{platform} %{platformname}

%install

#GPG Keys
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -pm 644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-HTCondor-%{version}
install -pm 644 %{SOURCE3} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-HTCondor-%{version}-Snapshot
install -pm 644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-HTCondor-23
install -pm 644 %{SOURCE5} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-HTCondor-23-Daily

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{packager}repos.d
install -m 644 *.repo $RPM_BUILD_ROOT%{_sysconfdir}/%{packager}repos.d

%clean
rm -f *.repo

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/%{packager}repos.d/*
/etc/pki/rpm-gpg/*

%changelog
* Mon Oct 07 2024 Tim Theisen <tim@cs.wisc.edu> - 24.x-1
- HTCondor 24.x repository definition

* Fri Aug 30 2024 Tim Theisen <tim@cs.wisc.edu> - 24.0-1
- HTCondor 24.0 repository definition

* Wed Dec 13 2023 Tim Theisen <tim@cs.wisc.edu> - 23.x-2
- Add openSUSE LEAP 15

* Tue Nov 28 2023 Tim Theisen <tim@cs.wisc.edu> - 23.0-2
- Add openSUSE LEAP 15

* Thu Aug 24 2023 Tim Theisen <tim@cs.wisc.edu> - 23.x-1
- HTCondor 23.x repository definition

* Thu Aug 24 2023 Tim Theisen <tim@cs.wisc.edu> - 23.0-1
- HTCondor 23.0 repository definition

* Fri Nov 11 2022 Tim Theisen <tim@cs.wisc.edu> - 10.1-1
- HTCondor 10.1 repository definition

* Fri Nov 11 2022 Tim Theisen <tim@cs.wisc.edu> - 10.0-1
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

