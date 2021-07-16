%bcond_without    check
%bcond_without    use_system_libuv

%global forgeurl  https://github.com/Shadowsocks-NET/Qv2ray
%global branch    main
Version:          3.0.0

%forgemeta

Name:             qv2ray
Release:          0.2.pre2%{?dist}
Summary:          A cross-platform V2Ray graphical front-end
License:          GPLv3
URL:              https://qv2ray.net/

# Source is created by:
# cd $(outdir)
# git clone https://github.com/Shadowsocks-NET/Qv2ray $(name-version)
# cd $(name-version)
# git checkout $(committish)
# git submodule update --init --recursive
# cd ..
# tar czf $(source0) --exclude .git $(name-version)
# rm -rf $(name-version)
Source0:          %{archivename}.tar.gz

Patch0:           0001-update-include-path.patch
Patch1:           https://github.com/Qv2ray/Qv2ray/commit/12e508cc5d9a3e9e3eacd91ddd85f5eabb150849.patch

%if %{with check}
BuildRequires:    desktop-file-utils
BuildRequires:    libappstream-glib
%endif

%if %{with use_system_libuv}
BuildRequires:    libuv-devel >= 1.38.1
%endif

BuildRequires:    cmake >= 3.10.1
BuildRequires:    gcc
BuildRequires:    gcc-c++
BuildRequires:    openssl-devel
BuildRequires:    libcurl-devel
BuildRequires:    protobuf-devel
BuildRequires:    grpc-devel
BuildRequires:    grpc-plugins
BuildRequires:    cmake(Qt6)
BuildRequires:    cmake(Qt6Gui)
BuildRequires:    cmake(Qt6Svg)
Requires:         hicolor-icon-theme

Recommends:       %{name}-plugin-builtin-protocol-support%{?_isa} = %{version}-%{release}
Recommends:       %{name}-plugin-builtin-subscription-support%{?_isa} = %{version}-%{release}

%package plugin-builtin-protocol-support
Summary:          Qv2ray Builtin Protocol Support
Requires:         %{name}%{?_isa} = %{version}-%{release}

%package plugin-builtin-subscription-support
Summary:          Qv2ray Builtin Subscription Support
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description
Qv2ray is a cross-platform v2ray graphical front-end written in Qt.
Features:
    * Cross-platform, multi-distribution support
    * Versatile Host Importing
    * Subscriptions
    * Built-in Host Editors
    * (Almost) Full Functionality Support
    * Real-time Speed & Data Usage Monitoring
    * Latency Testing (TCP)
For more details please see %{url}

%description plugin-builtin-protocol-support
VMess, VLESS, SOCKS, HTTP, Shadowsocks, DNS, Dokodemo-door editor support.

%description plugin-builtin-subscription-support
Basic subscription support for Qv2ray.


%prep
%forgeautosetup -p 1


%build
%cmake                    -DQV2RAY_DISABLE_AUTO_UPDATE=ON \
%{?with_check:            -DBUILD_TESTING=ON} \
%{?with_use_system_libuv: -DUSE_SYSTEM_LIBUV=ON} \
                          -DQV2RAY_BUILD_INFO="Qv2ray built from rpmbuild" \
                          -DQV2RAY_BUILD_EXTRA_INFO="$(rpmbuild --version), kernel-$(uname -r), qt-$(pkg-config --modversion Qt6)" \
                          -DQV2RAY_DEFAULT_VCORE_PATH="%{_bindir}/v2ray" \
                          -DQV2RAY_DEFAULT_VASSETS_PATH="%{_datadir}/v2ray" \
                          -DCMAKE_BUILD_TYPE="Release"
%cmake_build


%install
%cmake_install


%if %{with check}
%check
desktop-file-validate                 %{buildroot}%{_datadir}/applications/qv2ray.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/qv2ray.metainfo.xml
%ctest
%endif


%files
%license LICENSE
%doc README.md
%{_bindir}/qv2ray
%{_metainfodir}/qv2ray.metainfo.xml
%{_datadir}/applications/qv2ray.desktop
%{_datadir}/icons/hicolor/*
%dir %{_exec_prefix}/lib/qv2ray/
%dir %{_exec_prefix}/lib/qv2ray/plugins/

%files plugin-builtin-protocol-support
%{_exec_prefix}/lib/qv2ray/plugins/libQvPlugin-BuiltinProtocolSupport.so

%files plugin-builtin-subscription-support
%{_exec_prefix}/lib/qv2ray/plugins/libQvPlugin-BuiltinSubscriptionSupport.so


%changelog
* Thu Apr 22 2021 sixg0000d <sixg0000d@gmail.com> - 2.7.0-0.2.pre2.20210422gitdev
- Initial qv2ray
