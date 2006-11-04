# TODO
#	- %%service stuff
#	- add user autopsy with proper homedir rights
%include	/usr/lib/rpm/macros.perl
Summary:	The Autopsy Forensic Browser - a graphical interface to The Sleuth Kit utilities
Summary(pl):	Autopsy Forensic Browser - graficzny interfejs do narzêdzi z The Sleuth Kit
Name:		autopsy
Version:	2.08
Release:	0.3
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/autopsy/%{name}-%{version}.tar.gz
# Source0-md5:	0ac9db9acf66742f8f01f3d8b0cf2f90
URL:		http://www.sleuthkit.org/autopsy
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	coreutils
Requires:	file
# check: openssl contains only shared lib and I don't see any native code here
# shouldn't it be openssl-tools or some openssl-based perl module?
Requires:	openssl
Requires:	perl-Date-Manip
Requires:	sleuthkit
# noarch?
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Autopsy Forensic Browser is a graphical interface to utilities
found in The Sleuth Kit (TSK). TSK is a collection of command line
tools that allow you to investigate a Windows or Unix system by
examining the hard disk contents. TSK and Autopsy will show you the
files, data units, and metadata of NTFS, FAT, EXTxFS, and UFS file
system images in a read-only environment. Autopsy allows you to search
for specific types of evidence based on keywords, MAC times, hash
values, and file types.

%description -l pl
Autopsy Forensic Browser to graficzny interfejs do narzêdzi z pakietu
The Sleuth Kit (TSK). TSK to zbiór programów dzia³aj±cych z linii
poleceñ pozwalaj±cych zbadaæ system Windows lub uniksowy poprzez
sprawdzanie zawarto¶ci twardego dysku. TSK i Autopsy pokazuj± pliki,
jednostki danych i metadane obrazów systemów plików NTFS, FAT, EXTxFS
i UFS w ¶rodowisku tylko do odczytu. Autopsy pozwala wyszukiwaæ
okre¶lone rodzaje dowodów w oparciu o s³owa kluczowe, czasy MAC,
warto¶ci haszy i rodzaje plików.

%prep
%setup -q

echo '#!%{__perl} -wT' > autopsy
echo 'use lib qw(%{perl_vendorlib}/Autopsy);' >> autopsy
echo 'use lib qw(%{perl_vendorlib}/Autopsy/lib);' >> autopsy
cat base/autopsy.base >> autopsy

cat > conf.pl <<-'EOF'
	# Autopsy configuration settings

	# when set to 1, the server will stop after it receives no
	# connections for STIMEOUT seconds.
	$USE_STIMEOUT = 0;
	$STIMEOUT = 3600;

	# number of seconds that child waits for input from client
	$CTIMEOUT = 15;

	# set to 1 to save the cookie value in a file (for scripting)
	$SAVE_COOKIE = 1;

	$INSTALLDIR = '%{perl_vendorlib}/Autopsy/';

	# System Utilities
	$GREP_EXE = '/bin/grep';

	# Directories
	$TSKDIR = '%{_bindir}';
	$FILE_EXE = '%{_bindir}/file';
	$NSRLDB = '';
# FIXME: FHS: /var/{lib,run}/autopsy?
	$LOCKDIR = '/home/services/autopsy';
EOF

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -d $RPM_BUILD_ROOT/home/services/autopsy
install -d $RPM_BUILD_ROOT%{perl_vendorlib}/Autopsy/{lib,pict}

install autopsy $RPM_BUILD_ROOT%{_bindir}
install conf.pl $RPM_BUILD_ROOT%{perl_vendorlib}/Autopsy
install lib/* $RPM_BUILD_ROOT%{perl_vendorlib}/Autopsy/lib
install pict/* $RPM_BUILD_ROOT%{perl_vendorlib}/Autopsy/pict

install man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt docs/sleuthkit-informer-13.txt
%attr(755,root,root) %{_bindir}/*
%dir %{perl_vendorlib}/Autopsy
%{perl_vendorlib}/Autopsy/conf.pl
%{perl_vendorlib}/Autopsy/lib
%{perl_vendorlib}/Autopsy/pict
%{_mandir}/man1/*
/home/services/autopsy
