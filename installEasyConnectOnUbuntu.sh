#!/usr/bin/bash

# To install EasyConnect on Ubuntu18 or later versions, old version of pango and
# other dependent libraries are need. You can use this shell to install them with
# one command `bash install.sh`.

# Learn more on https://zhuanlan.zhihu.com/p/346325399

# Tested on Ubuntu20.04, 2022/1/26

case `sudo uname --m` in
   "x86_64") filename="EasyConnect_x64_7_6_7_3.deb"; libname2="amd64.deb"
   ;;
   "i686") filename="EasyConnect_x86_7_6_7_3.deb"; libname2="i386.deb"
   ;;
   *) echo "Exit because EasyConnect can't be installed on your computer."; exit
esac

thispath=`pwd`

mkdir tmp
cd tmp

wget http://download.sangfor.com.cn/download/product/sslvpn/pkg/linux_767/${filename}
sudo dpkg -i ${filename}

libname1s=("libpango-1.0-0_1.40.14-1_" "libpangocairo-1.0-0_1.40.14-1_" \
           "libpangoft2-1.0-0_1.40.14-1_")

for libname1 in ${libname1s[@]}
do
    wget http://security.ubuntu.com/ubuntu/pool/main/p/pango1.0/${libname1}${libname2}
    dpkg -X ${libname1}${libname2} ./
done

libs=("libpango-1.0.so.0" "libpangocairo-1.0.so.0" "libpangoft2-1.0.so.0")
ecPath="/usr/share/sangfor/EasyConnect"

cd ./usr/lib/x86_64-linux-gnu

for lib in ${libs[@]}
do
    sudo cp ${lib}.4000.14 ${ecPath}
    sudo ln -s ${ecPath}/${lib}.4000.14 ${ecPath}/${lib}
done

cd ${thispath}
rm -fr tmp

sudo apt install libcanberra-gtk-module
