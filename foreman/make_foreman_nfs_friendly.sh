## Success!
##  * Foreman is running at https://rhos6pi.narkissos.net
##      Initial credentials are admin / Gr5JXcMdJYg5co3j
##  * Foreman Proxy is running at https://rhos6pi.narkissos.net:8443
##  * Puppetmaster is running at port 8140
##  The full log is at /var/log/rhel-osp-installer/rhel-osp-installer.log

mkdir -p /media/cdrom
mkdir -p /kram/bin/redhat/7_1
mkdir -p /kram/bin/redhat/7_0


mount /dev/cdrom /media/cdrom

yum install nfs-utils nfs-utils-lib -y

rsync -avz --progress /media/cdrom/* /kram/bin/redhat/7_1

rsync -avz --progress /media/cdrom/images/pxeboot/vmlinuz /var/lib/tftpboot/boot/RedHat-7.1-x86_64-vmlinuz

rsync -avz --progress /media/cdrom/images/pxeboot/initrd.img /var/lib/tftpboot/boot/RedHat-7.1-x86_64-initrd.img

chown foreman-proxy:root /var/lib/tftpboot/boot/*

chmod 755 /var/lib/tftpboot/boot/*

echo 'ALL:127.0.0.1' >> /etc/hosts.allow

service iptables stop
service firewalld stop
chkconfig iptables off
chkconfig firewalld off

service rpcbind start
service nfs start
chkconfig rpcbind on
chkconfig nfs on

echo '/kram/bin		*(insecure,rw,sync,no_root_squash)' >> /etc/exports

service nfs restart



