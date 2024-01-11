Name:           autotrace
Version:        0.31.1
Release:        55%{?dist}
Summary:        Utility for converting bitmaps to vector graphics
License:        GPLv2+ and LGPLv2+
URL:            http://autotrace.sourceforge.net/
Source0:        http://download.sf.net/autotrace/%{name}-%{version}.tar.gz
Patch1:         autotrace-0001-Modify-GetOnePixel-usage-to-build-against-current-Im.patch
Patch2:         autotrace-0002-Fixed-underquoted-AM_PATH_AUTOTRACE-definition.patch
Patch3:         autotrace-0003-libpng-fix.patch
# Sent upstream
Patch4:         autotrace-0.31.1-CVE-2013-1953.patch
Patch5:         autotrace-0.31.1-multilib-fix.patch
Patch6:         autotrace-0.31.1-pstoedit-detection-fix.patch
Patch7:         autotrace-0.31.1-CVE-2016-7392.patch
Patch8:         autotrace-0.31.1-CVE-2019-19004.patch
Patch9:         autotrace-0.31.1-CVE-2019-19005.patch
# Upstream patch
Patch10:        autotrace-0.31.1-CVE-2022-32323.patch

BuildRequires:  libpng-devel > 2:1.2
BuildRequires:  libexif-devel
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libxml2-devel
BuildRequires:  bzip2-devel
BuildRequires:  freetype-devel
BuildRequires:  pstoedit-devel
BuildRequires:  gcc-c++

# For autoreconf
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pstoedit-devel


%description
AutoTrace is a program for converting bitmaps to vector graphics.

Supported input formats include BMP, TGA, PNM, PPM, PNG, whereas output
can be produced in Postscript, SVG, xfig, SWF, and others.

%package devel
Summary:        Header files for autotrace
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       pstoedit-devel


%description devel
This package contains header files and development libraries for autotrace.


%prep
%setup -q
%patch1 -p1 -b .GetOnePixel
%patch2 -p1 -b .aclocal18
%patch3 -p1 -b .libpng15
%patch4 -p1 -b .CVE-2013-1953
%patch5 -p1 -b .multilib-fix
%patch6 -p1 -b .pstoedit-detection-fix
%patch7 -p1 -b .CVE-2016-7392
%patch8 -p1 -b .CVE-2019-19004
%patch9 -p1 -b .CVE-2019-19005
%patch10 -p1 -b .CVE-2022-32323
autoreconf -ivf

%build
%configure --without-magick

# remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog FAQ NEWS README THANKS TODO
%license COPYING COPYING.LIB
%{_bindir}/autotrace
%{_libdir}/*.so.*
%{_mandir}/man[^3]/*

%files devel
%doc HACKING
%{_bindir}/autotrace-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/autotrace.pc
%{_includedir}/autotrace/
%{_datadir}/aclocal/autotrace.m4


%changelog
* Tue Sep 13 2022 Parag Nemade <pnemade AT redhat DOT com> - 0.31.1-55
- Resolves: rhbz#2121827 Fix the gating tests by using only local test
  Upstream testsuite will not work as this package code is very old

* Mon Sep 12 2022 Parag Nemade <pnemade AT redhat DOT com> - 0.31.1-54
- Resolves: rhbz#2121827
  CVE-2022-32323 - heap-buffer overflow via the ReadImage() at input-bmp.c

* Fri Apr 30 2021 Parag Nemade <pnemade AT redhat DOT com> - 0.31.1-53
- Resolves: CVE-2019-19004 : integer overflow in input-bmp.c
- Resolves: CVE-2019-19005 : fix bitmap double free in main.c

* Tue Aug 21 2018 Parag Nemade <pnemade AT redhat DOT com> - 0.31.1-52
- Resolves:rh#1564990: Removed BR: ImageMagick-devel

* Thu May  3 2018 Jan Horak <jhorak@redhat.com> - 0.31.1-51
- Resolves:rh#1564990: Removed ImageMagick support

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.1-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 24 2017 Michael Cronenworth <mike@cchtml.com> - 0.31.1-49
- Bump release for upgrade path

* Wed Aug 23 2017 Michael Cronenworth <mike@cchtml.com> - 0.31.1-48
- Rebuilt for new ImageMagick

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.1-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Kevin Fenzi <kevin@scrye.com> - 0.31.1-46
- Rebuild for new ImageMagick

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.1-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.1-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 0.31.1-43
- Enabled pstoedit backend
- Fixed out of bounds write when using pstoedit backend
  Resolves: CVE-2016-7392
- Fixed hardcoded version on source URL
- Fixed bogus date in changelog (best effort)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.1-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Jon Ciesla <limburgher@gmail.com> - 0.31.1-38
- ImageMagick rebuild.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.31.1-36
- Fix building on AArch64
- Enable pstoedit back

* Fri Jul 19 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.31.1-35
- Fixed multilib conflict in devel package (by multilib-fix patch)
- Removed rpaths

* Fri Jun 28 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.31.1-34
- Fixed buffer overflow when parsing BMP files
  Resolves: CVE-2013-1953

* Mon Mar 18 2013 Jon Ciesla <limburgher@gmail.com> - 0.31.1-33
- ImageMagick rebuild.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.31.1-31
- Cosmetic changes in the spec-file (closes rhbz #803928 and #817950)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-30.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 02 2012 Jon Ciesla <limburgher@gmail.com> - 0.31.1-29.1
- Libpng 1.5 fix.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-28.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.31.1-27.1
- Rebuild for new libpng

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-26.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.31.1-25.1
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.31.1-24.1
- rebuild (ImageMagick)

* Mon May 17 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.31.1-24
- Changed description (closes rhbz #591659).

* Mon Jul 27 2009 Peter Lemenkov <lemenkov@gmail.com> - 0.31.1-23
- Removed static libraries from -devel
- Changed %%makeinstall to "make install DESTDIR=blablabla"
- Fixed rhbz# 477980

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Hans de Goede <hdegoede@redhat.com> - 0.31.1-21
- Rebuild for new ImageMagick

* Mon Mar 02 2009 Caolán McNamara <caolanm@redhat.com> - 0.31.1-20
- Modify GetOnePixel usage to build against current ImageMagick api

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.31.1-18
- fix license tag

* Mon May 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.31.1-17
- Rebuild for new ImageMagick.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.31.1-16
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Quentin Spencer <qspencer@users.sourceforge.net> - 0.31.1-15
- Rebuild for F8.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.31.1-14
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Quentin Spencer <qspencer@users.sourceforge.net> - 0.31.1-13
- Rebuild for FC6.

* Mon Feb 13 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-12
- Rebuild for Fedora Extras 5

* Sat Jan 28 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-11
- rebuild

* Tue Jan 17 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-10
- add BuildRequires on freetype-devel

* Tue Jan 17 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-9
- remove BuildRequires on XFree86-devel

* Mon Jan 16 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 0.31.1-8
- add %%{?dist} tag
- add a BuildRequires on bzip2-devel
- add ldconfig to %%post and %%postun

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 0.31.1-7
- and more buildrequires

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 0.31.1-6
- BR libtiff-devel

* Wed May 25 2005 Jeremy Katz <katzj@redhat.com> - 0.31.1-5
- rebuild

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Aug 21 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.31.1-3
- Temporarily changed buildreq pstoedit-devel to buildconflicts.

* Thu Apr 22 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.31.1-0.fdr.2
- Added new BuildReq pstoedit-devel.
- Added missing BuildReq libexif-devel.
- Added missing -devel requires pkgconfig, ImageMagick-devel.
- Converted spec file to UTF-8.

* Mon Sep 29 2003 Marius L. Johndal <mariuslj at ifi.uio.no> 0:0.31.1-0.fdr.1
- Initial RPM release.

