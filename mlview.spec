%define	version	0.9.0
%define release %mkrel 4

%define major	10
%define libname %mklibname %{name} %{major}

Summary:	Tree oriented XML editor for GNOME
Name:		mlview
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Editors
URL:		http://mlview.org/
Buildroot:	%{_tmppath}/%{name}-%{version}-root

Source:		ftp://ftp.gnome.org/pub/gnome/sources/%{name}/%{version}/%{name}-%{version}.tar.bz2
Patch0:		mlview-0.9.0-gcc411.patch.bz2

BuildRequires:	libgnomeui2-devel >= 2.2.0
BuildRequires:	eel-devel >= 2.2.0
BuildRequires:	gtk+2-devel >= 2.2.0
BuildRequires:	libxml2-devel >= 2.4.30
BuildRequires:	libxslt-devel >= 1.0.33
BuildRequires:	libglade2.0-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	gtkmm2.4-devel
BuildRequires:	gtksourceview-devel >= 1.0
BuildRequires:	libglademm-devel >= 2.4.0
BuildRequires:	libvte-devel >= 0.11.12
BuildRequires:	libexpat-devel
BuildRequires:  desktop-file-utils
Requires:	%{libname} = %{version}
Requires(post):		GConf2 >= 2.3.3
Requires(preun):	GConf2 >= 2.3.3

%description
MlView is a generic XML editor for the GNOME environment.

%package	-n %{libname}
Summary:	Essential library for MLView
Group:		System/Libraries

%description	-n %{libname}
libmlview is the essential library needed by the mlview application.

%prep
%setup -q
%patch0 -p1

%build
%configure2_5x 

%make

%install
rm -rf %{buildroot}
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

mkdir -p %{buildroot}%{_menudir}
cat << _EOF_ > %{buildroot}%{_menudir}/%{name}
?package(%{name}): \
 command="%{_bindir}/mlview" \
 icon="editors_section.png" \
 longtitle="Tree oriented XML editor" \
 needs="x11" \
 section="Applications/Editors" \
 title="MlView XML editor" \
 xdg="true"
_EOF_

sed -i s/mlview-app-icon.xpm/mlview-app-icon/ $RPM_BUILD_ROOT%{_datadir}/applications/*

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="TextEditor" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%find_lang %{name}

# remove files not bundled
# "devel" files not useful yet
rm -f %{buildroot}%{_libdir}/lib*.a \
      %{buildroot}%{_libdir}/lib*.la \
      %{buildroot}%{_libdir}/lib*.so \
      %{buildroot}%{_libdir}/mlview/plugins/lib*.a \
      %{buildroot}%{_libdir}/mlview/plugins/lib*.la \
      %{buildroot}%{_libdir}/mlview/plugins/lib*.so

%post
%post_install_gconf_schemas mlview.schemas
%update_menus

%preun
%preun_uninstall_gconf_schemas mlview.schemas

%postun
%clean_menus

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS BRANCHES COPYING ChangeLog NEWS README
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/*.schemas
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_datadir}/%{name}
%{_datadir}/mime-info/*
%{_datadir}/application-registry/*
%{_menudir}/%{name}
%{_libdir}/mlview/plugins/*
%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/lib*.so*

