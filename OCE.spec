#
# Conditional build:
%bcond_without	tests		# build with tests
%bcond_with	tbb		# Use tbb for multithreading
%bcond_without	openmp		# Use openmp for multithreading
#
Summary:	OpenCASCADE Community Edition
Name:		OCE
Version:	0.18.3
Release:	3
License:	LGPLv2 with exception
Group:		Applications/Engineering
URL:		https://github.com/tpaviot/oce
Source0:	https://github.com/tpaviot/oce/archive/%{name}-%{version}.tar.gz
# Source0-md5:	1686393c8493bbbb2f3f242330b33cba
Source1:	DRAWEXE.1
Source2:	opencascade-draw.desktop
Source3:	oce-256.png
Source4:	oce-128.png
Source5:	oce-64.png
Source6:	oce-48.png
# Utilities
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
# Libraries
BuildRequires:	FreeImage-devel
BuildRequires:	Mesa-libGL-devel
BuildRequires:	Mesa-libGLU-devel
BuildRequires:	ftgl-devel
BuildRequires:	gl2ps-devel
BuildRequires:	libgomp
%{?with_openmp:BuildRequires:	libopenmpt-devel}
%{?with_tbb:BuildRequires:	tbb-devel}
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXdmcp-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXpm-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXres-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libxkbfile
BuildRequires:	xorg-proto-xproto-devel

%description
OpenCASCADE Community Edition (OCE) is a suite for 3D surface and
solid modeling, visualization, data exchange and rapid application
development. It is an excellent platform for development of numerical
simulation software including CAD/CAM/CAE, AEC and GIS, as well as PDM
applications.

%package foundation
Summary:	OpenCASCADE CAE platform shared libraries
Group:		Libraries

%description foundation
OpenCASCADE CAE platform shared libraries

This package contains foundation classes which provide a variety of
general-purpose services such as automated management of heap memory,
exception handling, classes for manipulating aggregates of data, basic
math tools.

%package modeling
Summary:	OpenCASCADE CAE platform shared libraries
Group:		Libraries

%description modeling
OpenCASCADE CAE platform shared libraries

This package supplies data structures to represent 2D and 3D geometric
models, as well as topological and geometrical algorithms.

%package ocaf
Summary:	OpenCASCADE CAE platform shared libraries
Group:		Libraries

%description ocaf
OpenCASCADE CAE platform shared libraries

This package provides OpenCASCADE Application Framework services and
support for data exchange.

%package visualization
Summary:	OpenCASCADE CAE platform shared libraries
Group:		Libraries

%description visualization
OpenCASCADE CAE platform shared libraries

This package provides services for displaying 2D and 3D graphics.

%package examples
Summary:	OpenCASCADE CAE platform shared libraries
Group:		Libraries

%description examples
OpenCASCADE CAE platform shared libraries

This package contains example input files for OpenCASCADE in various
formats.

%package draw
Summary:	OpenCASCADE CAE platform shared libraries
Group:		Libraries

%description draw
OpenCASCADE CAE DRAW test harness.

%package devel
Summary:	OpenCASCADE CAE platform library development files
Group:		Development/Libraries
Requires:	%{name}-draw = %{version}-%{release}
Requires:	%{name}-foundation = %{version}-%{release}
Requires:	%{name}-modeling = %{version}-%{release}
Requires:	%{name}-ocaf = %{version}-%{release}
Requires:	%{name}-visualization = %{version}-%{release}
Requires:	FreeImage-devel
Requires:	Mesa-libGL-devel
Requires:	Mesa-libGLU-devel
Requires:	freetype-devel
Requires:	gl2ps-devel
Requires:	tbb-devel
Requires:	tcl-devel
Requires:	tk-devel
Requires:	xorg-lib-libICE-devel
Requires:	xorg-lib-libSM-devel
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXScrnSaver-devel
Requires:	xorg-lib-libXcomposite-devel
Requires:	xorg-lib-libXcursor-devel
Requires:	xorg-lib-libXdmcp-devel
Requires:	xorg-lib-libXext-devel
Requires:	xorg-lib-libXi-devel
Requires:	xorg-lib-libXinerama-devel
Requires:	xorg-lib-libXpm-devel
Requires:	xorg-lib-libXrandr-devel
Requires:	xorg-lib-libXres-devel
Requires:	xorg-lib-libXtst-devel
Requires:	xorg-lib-libXv-devel
Requires:	xorg-lib-libxkbfile

%description devel
OpenCASCADE CAE platform library development files

%prep
%setup -q -n oce-%{name}-%{version}

%build
install -d build
cd build
%{cmake} \
		-DOCE_INSTALL_PREFIX=%{_prefix} \
		-DOCE_INSTALL_LIB_DIR=%{_lib} \
		-DOCE_WITH_FREEIMAGE=ON \
		-DOCE_WITH_GL2PS=ON \
		-DOCE_MULTITHREAD_LIBRARY:STRING=%{?with_tbb:TBB}%{!?with_tbb:%{?with_openmp:OPENMP}%{!?with_openmp:NONE}} \
		-DOCE_DRAW=ON \
		-DOCE_TESTING=ON \
		../

%{__make}

%if %{with tests}
export CTEST_OUTPUT_ON_FAILURE=1
%{__make} -C test test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# Install manpage for DRAWEXE
install -Dm 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1/DRAWEXE.1

# Install and validate desktop file
desktop-file-install \
    --dir=$RPM_BUILD_ROOT%{_desktopdir} \
    %{SOURCE2}

# Install icons
for size in 256 128 64 48; do
    icon=%{_sourcedir}/oce-${size}.png
    install -Dm 0644 $icon \
        $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}x${size}/apps/oce.png
done

%post foundation -p /sbin/ldconfig
%postun foundation -p /sbin/ldconfig

%post modeling -p /sbin/ldconfig
%postun modeling -p /sbin/ldconfig

%post ocaf -p /sbin/ldconfig
%postun ocaf -p /sbin/ldconfig

%post visualization -p /sbin/ldconfig
%postun visualization -p /sbin/ldconfig

%post draw
%update_icon_cache hicolor

%postun draw
if [ $1 -eq 0 ] ; then
    %update_icon_cache hicolor
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files foundation
%defattr(644,root,root,755)
%doc AUTHORS.md LICENSE_LGPL_21.txt NEWS.md OCCT_LGPL_EXCEPTION.txt
# Foundation
%attr(755,root,root) %{_libdir}/libTKernel.so.*
%attr(755,root,root) %{_libdir}/libTKMath.so.*
%{_datadir}/oce-*.*/

%files modeling
%defattr(644,root,root,755)
# Modeling Data
%attr(755,root,root) %{_libdir}/libTKG2d.so.*
%attr(755,root,root) %{_libdir}/libTKG3d.so.*
%attr(755,root,root) %{_libdir}/libTKGeomBase.so.*
%attr(755,root,root) %{_libdir}/libTKBRep.so.*
# Modeling Algorithm s
%attr(755,root,root) %{_libdir}/libTKGeomAlgo.so.*
%attr(755,root,root) %{_libdir}/libTKTopAlgo.so.*
%attr(755,root,root) %{_libdir}/libTKPrim.so.*
%attr(755,root,root) %{_libdir}/libTKBO.so.*
%attr(755,root,root) %{_libdir}/libTKHLR.so.*
%attr(755,root,root) %{_libdir}/libTKMesh.so.*
%attr(755,root,root) %{_libdir}/libTKShHealing.so.*
%attr(755,root,root) %{_libdir}/libTKXMesh.so.*
%attr(755,root,root) %{_libdir}/libTKBool.so.*
%attr(755,root,root) %{_libdir}/libTKFillet.so.*
%attr(755,root,root) %{_libdir}/libTKFeat.so.*
%attr(755,root,root) %{_libdir}/libTKOffset.so.*
# Data exchange
%attr(755,root,root) %{_libdir}/libTKSTL.so.*
%attr(755,root,root) %{_libdir}/libTKXSBase.so.*
%attr(755,root,root) %{_libdir}/libTKSTEPBase.so.*
%attr(755,root,root) %{_libdir}/libTKIGES.so.*
%attr(755,root,root) %{_libdir}/libTKSTEPAttr.so.*
%attr(755,root,root) %{_libdir}/libTKSTEP209.so.*
%attr(755,root,root) %{_libdir}/libTKSTEP.so.*
%attr(755,root,root) %{_libdir}/libTKVRML.so.*
%attr(755,root,root) %{_libdir}/libTKXCAF.so.*
%attr(755,root,root) %{_libdir}/libTKXCAFSchema.so.*
%attr(755,root,root) %{_libdir}/libTKXmlXCAF.so.*
%attr(755,root,root) %{_libdir}/libTKBinXCAF.so.*
%attr(755,root,root) %{_libdir}/libTKXDEIGES.so.*
%attr(755,root,root) %{_libdir}/libTKXDESTEP.so.*

%files visualization
%defattr(644,root,root,755)
# Visualization Dependents
%attr(755,root,root) %{_libdir}/libTKService.so.*
%attr(755,root,root) %{_libdir}/libTKV3d.so.*
# Visualization
%attr(755,root,root) %{_libdir}/libTKOpenGl.so.*
%attr(755,root,root) %{_libdir}/libTKMeshVS.so.*
%attr(755,root,root) %{_libdir}/libTKNIS.so.*
%attr(755,root,root) %{_libdir}/libTKVoxel.so.*

%files ocaf
%defattr(644,root,root,755)
# Application framework
%attr(755,root,root) %{_libdir}/libTKCDF.so.*
%attr(755,root,root) %{_libdir}/libPTKernel.so.*
%attr(755,root,root) %{_libdir}/libTKLCAF.so.*
%attr(755,root,root) %{_libdir}/libFWOSPlugin.so.*
%attr(755,root,root) %{_libdir}/libTKPShape.so.*
%attr(755,root,root) %{_libdir}/libTKBinL.so.*
%attr(755,root,root) %{_libdir}/libTKXmlL.so.*
%attr(755,root,root) %{_libdir}/libTKPLCAF.so.*
%attr(755,root,root) %{_libdir}/libTKTObj.so.*
%attr(755,root,root) %{_libdir}/libTKShapeSchema.so.*
%attr(755,root,root) %{_libdir}/libTKStdLSchema.so.*
%attr(755,root,root) %{_libdir}/libTKCAF.so.*
%attr(755,root,root) %{_libdir}/libTKBin.so.*
%attr(755,root,root) %{_libdir}/libTKXml.so.*
%attr(755,root,root) %{_libdir}/libTKPCAF.so.*
%attr(755,root,root) %{_libdir}/libTKBinTObj.so.*
%attr(755,root,root) %{_libdir}/libTKXmlTObj.so.*
%attr(755,root,root) %{_libdir}/libTKStdSchema.so.*

%files draw
%defattr(644,root,root,755)
# Draw Libraries
%dir %{_libdir}/oce-*.*
%attr(755,root,root) %{_libdir}/oce-*.*/libTKDraw.so.*
%attr(755,root,root) %{_libdir}/oce-*.*/libTKTopTest.so.*
%attr(755,root,root) %{_libdir}/oce-*.*/libTKViewerTest.so.*
%attr(755,root,root) %{_libdir}/oce-*.*/libTKXSDRAW.so.*
%attr(755,root,root) %{_libdir}/oce-*.*/libTKDCAF.so.*
%attr(755,root,root) %{_libdir}/oce-*.*/libTKXDEDRAW.so.*
%attr(755,root,root) %{_libdir}/oce-*.*/libTKTObjDRAW.so.*
# DRAWEXE application
%attr(755,root,root) %{_bindir}/DRAWEXE
%{_mandir}/man1/DRAWEXE.1*
%{_desktopdir}/opencascade-draw.desktop
%{_iconsdir}/hicolor/*/apps/*

%files devel
%defattr(644,root,root,755)
%doc examples
%{_includedir}/*
%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_libdir}/oce-*.*/*.so
%{_libdir}/oce-*.*/*.cmake
