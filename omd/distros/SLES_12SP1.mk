DISTRO_CODE     = sles12sp1
BUILD_PACKAGES  =
BUILD_PACKAGES += tar # needed for "make rpm"
BUILD_PACKAGES += rpm-devel # needed for "make rpm"
BUILD_PACKAGES += unzip # unpack src files of packages
BUILD_PACKAGES += groff # needed for building rrdtool
BUILD_PACKAGES += libltdl7 # needed for gearman
BUILD_PACKAGES += libtool # needed for gearman
BUILD_PACKAGES += boost-devel
BUILD_PACKAGES += samba-client # otherwise path to smblient missing in util.pm
BUILD_PACKAGES += rpcbind # otherwise missing path in util.pm
BUILD_PACKAGES += bind-utils # check_dns
BUILD_PACKAGES += freetype2-devel
BUILD_PACKAGES += gcc
BUILD_PACKAGES += gcc-c++
BUILD_PACKAGES += gd-devel
BUILD_PACKAGES += git
BUILD_PACKAGES += glib2-devel
BUILD_PACKAGES += libcurl-devel   # needed by perl modules / thruk
BUILD_PACKAGES += libexpat-devel
BUILD_PACKAGES += libevent-devel
BUILD_PACKAGES += libgnutls-devel
BUILD_PACKAGES += libjpeg62-devel
BUILD_PACKAGES += libmysqlclient-devel
BUILD_PACKAGES += libopenssl-devel
BUILD_PACKAGES += libpng16-devel # Perl::GD
BUILD_PACKAGES += libXpm-devel # Perl::GD
BUILD_PACKAGES += libvpx-devel # Perl::GD
BUILD_PACKAGES += libtiff-devel # Perl::GD
BUILD_PACKAGES += libuuid-devel
BUILD_PACKAGES += libxml2-devel
BUILD_PACKAGES += sqlite3-devel # needed by Python (for sqlite3 module)
BUILD_PACKAGES   += tk-devel # needed by Python (for Tkinter module)
BUILD_PACKAGES += make
BUILD_PACKAGES += mysql
BUILD_PACKAGES += openldap2-devel
BUILD_PACKAGES += pango-devel
BUILD_PACKAGES += patch
BUILD_PACKAGES += postgresql-devel
BUILD_PACKAGES += readline-devel
BUILD_PACKAGES += apache2-devel
BUILD_PACKAGES += freeradius-client-devel
BUILD_PACKAGES += libbz2-devel # needed for msitools
BUILD_PACKAGES += libgsf-devel # needed for msitools
BUILD_PACKAGES += libpcap-devel # needed buy CMC
BUILD_PACKAGES += rrdtool-devel # needed for CMC
BUILD_PACKAGES += libffi-devel # needed for pyOpenSSL (and dependant) compilations
BUILD_PACKAGES += krb5-devel # needed for pykerberos / requests-kerberos python modules
BUILD_PACKAGES += flex # needed for heirloom-pkgtools
BUILD_PACKAGES   += openssh # needed for check_by_ssh
OS_PACKAGES     =
OS_PACKAGES    += cronie # needed for sites cron jobs
OS_PACKAGES      += net-tools # traceroute is needed for Check_MK parent scan
OS_PACKAGES    += apache2
OS_PACKAGES    += bind-utils # check_dns
OS_PACKAGES    += curl
OS_PACKAGES    += dialog
OS_PACKAGES    += gd
OS_PACKAGES    += graphviz
OS_PACKAGES    += libpng12-0
OS_PACKAGES    += libevent-2_0-5
OS_PACKAGES    += libltdl7
OS_PACKAGES    += libreadline6
OS_PACKAGES    += libuuid1
OS_PACKAGES    += pango
OS_PACKAGES    += php-fastcgi
OS_PACKAGES    += php-gd
OS_PACKAGES    += php-iconv
OS_PACKAGES    += php-mbstring
OS_PACKAGES    += php-pear
OS_PACKAGES    += php-sockets
OS_PACKAGES    += php-sqlite
OS_PACKAGES    += php-openssl
OS_PACKAGES    += rsync
OS_PACKAGES    += samba-client
OS_PACKAGES    += rpcbind
OS_PACKAGES    += unzip
OS_PACKAGES    += xinetd
OS_PACKAGES    += xorg-x11-fonts
OS_PACKAGES    += freeradius-client-libs
OS_PACKAGES    += binutils # Needed by Check_MK Agent Bakery
OS_PACKAGES    += rpm-build # Needed by Check_MK Agent Bakery
OS_PACKAGES    += libgio-2_0-0 # needed by msitools/Agent Bakery
OS_PACKAGES    += libgsf-1-114 # needed by msitools/Agent Bakery
OS_PACKAGES    += cpio # needed for Agent bakery (solaris pkgs)
OS_PACKAGES    += poppler-tools # needed for preview of PDF in reporting
OS_PACKAGES    += libpcap1 # needed for ICMP of CMC
OS_PACKAGES     += libffi4 # needed for pyOpenSSL and dependant
OS_PACKAGES    += libjpeg62 # needed by PIL
USERADD_OPTIONS   = -M
ADD_USER_TO_GROUP = gpasswd -a %(user)s %(group)s
PACKAGE_INSTALL   = zypper -n refresh ; zypper -n install
ACTIVATE_INITSCRIPT = chkconfig --add %s
APACHE_CONF_DIR   = /etc/apache2/conf.d
APACHE_INIT_NAME  = apache2
APACHE_USER       = wwwrun
APACHE_GROUP      = www
APACHE_BIN        = /usr/sbin/httpd2-prefork
APACHE_CTL        = /usr/sbin/apache2ctl
APACHE_MODULE_DIR = /usr/lib/apache2-prefork
APACHE_MODULE_DIR_64 = /usr/lib64/apache2-prefork
HTPASSWD_BIN      = /usr/bin/htpasswd2
PHP_FCGI_BIN	  = /usr/bin/php-cgi
APACHE_ENMOD      = a2enmod %s
BECOME_ROOT       = su -c
MOUNT_OPTIONS     =
INIT_CMD          = /usr/bin/systemctl %(action)s %(name)s.service
