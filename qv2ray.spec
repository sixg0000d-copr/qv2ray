%bcond_without    check
%bcond_without    use_system_libuv
%bcond_with       qt6

%global forgeurl  https://github.com/Qv2ray/Qv2ray
%global tag       v2.7.0
Version:          2.7.0

%forgemeta

Name:             qv2ray
Release:          %{autorelease}
Summary:          A cross-platform V2Ray graphical front-end
License:          GPLv3
URL:              https://qv2ray.net/

# Source is created by:
# cd $(outdir)
# git clone https://github.com/Qv2ray/Qv2ray $(archivename)
# cd $(archivename)
# git checkout $(committish)
# git submodule update --init --recursive
# cd ..
# tar czf $(source0) --exclude .git $(archivename)
# rm -rf $(archivename)
Source0:          %{archivename}.tar.gz

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
BuildRequires:    libcurl-devel
BuildRequires:    protobuf-devel
BuildRequires:    grpc-devel
BuildRequires:    grpc-plugins
%if %{with qt6}
BuildRequires:    cmake(Qt6)
BuildRequires:    cmake(Qt6Gui)
BuildRequires:    cmake(Qt6Svg)
BuildRequires:    cmake(Qt6LinguistTools)
%else
BuildRequires:    cmake(Qt5)
BuildRequires:    cmake(Qt5Gui)
BuildRequires:    cmake(Qt5Svg)
BuildRequires:    cmake(Qt5LinguistTools)
%endif
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
%forgeautosetup


%build
%if %{with qt6}
export QT_MODVERSION="$(pkg-config --modversion Qt6)"
%else
export QT_MODVERSION="$(pkg-config --modversion Qt5)"
%endif

%cmake                    -DQV2RAY_DISABLE_AUTO_UPDATE=ON \
%{?with_check:            -DBUILD_TESTING=ON} \
%{?with_use_system_libuv: -DUSE_SYSTEM_LIBUV=ON} \
                          -DQV2RAY_BUILD_INFO="Qv2ray built by rpm-build" \
                          -DQV2RAY_BUILD_EXTRA_INFO="$(rpmbuild --version), kernel-$(uname -r), qt-${QT_MODVERSION:-unknown}" \
%{?with_qt6:              -DQV2RAY_QT6=ON} \
                          -DQV2RAY_DEFAULT_VCORE_PATH="%{_bindir}/v2ray" \
                          -DQV2RAY_DEFAULT_VASSETS_PATH="%{_datadir}/v2ray" \
                          -DCMAKE_BUILD_TYPE="Release"
%cmake_build


%install
%cmake_install
%find_lang %{name} --with-qt --all-name


%if %{with check}
%check
desktop-file-validate                 %{buildroot}%{_datadir}/applications/qv2ray.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/qv2ray.metainfo.xml
%ctest
%endif


%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/qv2ray
%{_metainfodir}/qv2ray.metainfo.xml
%{_datadir}/applications/qv2ray.desktop
%{_datadir}/icons/hicolor/*
%dir %{_datadir}/qv2ray/
%dir %{_datadir}/qv2ray/lang/
%dir %{_datadir}/qv2ray/plugins/

# https://github.com/rpm-software-management/rpm/issues/1642
%if 0%{?fedora} <= 35
%lang(yue_HK) %{_datadir}/qv2ray/lang/yue.qm
%endif

%files plugin-builtin-protocol-support
%{_datadir}/qv2ray/plugins/libQvPlugin-BuiltinProtocolSupport.so

%files plugin-builtin-subscription-support
%{_datadir}/qv2ray/plugins/libQvPlugin-BuiltinSubscriptionSupport.so


%changelog
%{autochangelog}
