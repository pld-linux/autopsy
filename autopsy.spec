#
# TODO	- %service stuff
#	- add user autopsy with proper homedir rights
#	- pl desc
#
Summary:	The Autopsy Forensic Browser is a graphical interface to The Sleuth Kit utilities
Summary(pl):	Autopsy Forensic Browser jest graficznym interfejsem do narzêdzi z The Sleuth Kit
Name:		autopsy
Version:	2.08
Release:	0.1
#Epoch:		-
License:	GPL
Group:		Applications
Source0:	http://mesh.dl.sourceforge.net/sourceforge/autopsy/%{name}-%{version}.tar.gz
# Source0-md5:	0ac9db9acf66742f8f01f3d8b0cf2f90
URL:		http://www.sleuthkit.org/autopsy
BuildRequires:	openssl-devel
BuildRequires:	perl-base
BuildRequires:	sleuthkit
Requires:	coreutils
Requires:	perl-Date-Manip
Requires:	openssl
Requires:	libmagic
Requires:	sleuthkit
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Autopsy Forensic Browser is a graphical interface to utilities
found in The Sleuth Kit (TSK).  TSK is a collection of command line
tools that allow you to investigate a Windows or Unix system by
examining the hard disk contents.  TSK and Autopsy will show you
the files, data units, and metadata of NTFS, FAT, EXTxFS, and UFS
file system images in a read-only environment.  Autopsy allows you
to search for specific types of evidence based on keywords, MAC
times, hash values, and file types.

%prep
%setup -q

%build

echo "#!/usr/bin/perl -wT" > autopsy
echo "use lib qw(/usr/share/perl5/vendor_perl/Autopsy);" >> autopsy
echo "use lib qw(/usr/share/perl5/vendor_perl/Autopsy/lib);" >> autopsy
cat base/autopsy.base >> autopsy

cat > conf.pl <<-EOF
	# Autopsy configuration settings
	
	# when set to 1, the server will stop after it receives no
	# connections for STIMEOUT seconds. 
	\$USE_STIMEOUT = 0;
	\$STIMEOUT = 3600;
	
	# number of seconds that child waits for input from client
	\$CTIMEOUT = 15;
	
	# set to 1 to save the cookie value in a file (for scripting)
	\$SAVE_COOKIE = 1;
	
	\$INSTALLDIR = '/usr/share/perl5/vendor_perl/Autopsy/';
	
	# System Utilities
	\$GREP_EXE = '/bin/grep';
	
	# Directories
	\$TSKDIR = '/usr/bin';
	\$FILE_EXE = '/usr/bin/file';
	\$NSRLDB = '';
	\$LOCKDIR = '/home/services/autopsy';
EOF

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -d $RPM_BUILD_ROOT/home/services/autopsy
install -d $RPM_BUILD_ROOT/usr/share/perl5/vendor_perl/Autopsy/{lib,pict}

install autopsy $RPM_BUILD_ROOT%{_bindir}
install conf.pl $RPM_BUILD_ROOT/usr/share/perl5/vendor_perl/Autopsy/
install lib/* $RPM_BUILD_ROOT/usr/share/perl5/vendor_perl/Autopsy/lib
install pict/* $RPM_BUILD_ROOT/usr/share/perl5/vendor_perl/Autopsy/pict

install man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%postun

%files
%defattr(644,root,root,755)
%doc README.txt docs/sleuthkit-informer-13.txt
%attr(755,root,root) %{_bindir}/*
/usr/share/perl5/vendor_perl/Autopsy/conf.pl
/usr/share/perl5/vendor_perl/Autopsy/lib/*
/usr/share/perl5/vendor_perl/Autopsy/pict/*
%{_mandir}/man1/*
/home/services/autopsy
