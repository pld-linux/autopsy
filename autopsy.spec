# TODO
#	- change use/require Appsort to Autopsy::lib::Appsort or Autopsy::Appsort and more
#
%include	/usr/lib/rpm/macros.perl
Summary:	The Autopsy Forensic Browser - a graphical interface to The Sleuth Kit utilities
Summary(pl.UTF-8):	Autopsy Forensic Browser - graficzny interfejs do narzędzi z The Sleuth Kit
Name:		autopsy
Version:	2.21
Release:	1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/autopsy/%{name}-%{version}.tar.gz
# Source0-md5:	48d970749861cde7b850283636c6c4dd
Source1:	%{name}.init
URL:		http://www.sleuthkit.org/autopsy
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	coreutils
Requires:	file
# check: openssl contains only shared lib and I don't see any native code here
# shouldn't it be openssl-tools or some openssl-based perl module?
Requires:	openssl
Requires:	perl-Date-Manip
Requires:	sleuthkit
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
# some script/macro finds that autopsy requires the following perl modules
# which are provided in the package - as a workaround we provide them:
# (but this pollutes a perl module namespace)
Provides:	perl(Appsort)
Provides:	perl(Appview)
Provides:	perl(Args)
Provides:	perl(Caseman)
Provides:	perl(Data)
Provides:	perl(Exec)
Provides:	perl(File)
Provides:	perl(Filesystem)
Provides:	perl(Frame)
Provides:	perl(Fs)
Provides:	perl(Hash)
Provides:	perl(Kwsrch)
Provides:	perl(Main)
Provides:	perl(Meta)
Provides:	perl(Notes)
Provides:	perl(Print)
Provides:	perl(Timeline)
Provides:	perl(Vs)
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

%description -l pl.UTF-8
Autopsy Forensic Browser to graficzny interfejs do narzędzi z pakietu
The Sleuth Kit (TSK). TSK to zbiór programów działających z linii
poleceń pozwalających zbadać system Windows lub uniksowy poprzez
sprawdzanie zawartości twardego dysku. TSK i Autopsy pokazują pliki,
jednostki danych i metadane obrazów systemów plików NTFS, FAT, EXTxFS
i UFS w środowisku tylko do odczytu. Autopsy pozwala wyszukiwać
określone rodzaje dowodów w oparciu o słowa kluczowe, czasy MAC,
wartości haszy i rodzaje plików.

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
	$MD5_EXE = '%{_bindir}/md5sum';
	$SHA1_EXE = '%{_bindir}/sha1sum';
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

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/autopsy

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 178 autopsy
%useradd -u 178 -r -d /home/services/autopsy -s /bin/false -c "Autopsy user" -g autopsy autopsy

%post
/sbin/chkconfig --add autopsy

%preun
%service autopsy stop
/sbin/chkconfig --del autopsy

%postun
%userremove autopsy
%groupremove autopsy


%files
%defattr(644,root,root,755)
%doc README.txt docs/sleuthkit-informer-13.txt
%attr(755,root,root) %{_bindir}/*
%dir %{perl_vendorlib}/Autopsy
%{perl_vendorlib}/Autopsy/conf.pl
%{perl_vendorlib}/Autopsy/lib
%{perl_vendorlib}/Autopsy/pict
%{_mandir}/man1/*
%attr(750,autopsy,autopsy) /home/services/autopsy
%attr(754,root,root) /etc/rc.d/init.d/autopsy
