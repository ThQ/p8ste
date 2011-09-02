pkg_url=$1
pkg_full_name=`echo "$1" | grep -o -P "([^/]+)$"`
pkg_base_name=`echo "$pkg_full_name" | grep -o -P "^[^0-9]+(?=-\d)"`
pkg_version=`echo "$pkg_full_name" | grep -o -P "\d+\.\d+(\.\d+)?"`
pkg_name=${pkg_base_name}-${pkg_version}
module=$2
dest=$3
dest_archive=$3/${pkg_full_name}

if [ ! -d "${dest}/${module}" ] ; then
	echo "PACKAGE_NAME: ${pkg_base_name}"
	echo "PACKAGE_VERSION: ${pkg_version}"

	wget -N -P $dest $pkg_url

	if [ ! -f "$dest_archive" ] ; then
		echo "Failed to download archive from ${pkg_url}."
		echo "Should be at ${dest_archive}."
		exit 1
	fi

	tar --directory $dest --exclude "$pkg_name/$module/tests" -zxf ${dest}/${pkg_full_name} ${pkg_name}/${module}
	rm ${dest}/${pkg_full_name}
	if [ "$4" != "" ] ; then
		echo "POUUUUET"
		mv ${dest}/${pkg_name}/${module}/${4} ${dest}
	else
		mv ${dest}/${pkg_name}/* ${dest}
	fi
	rm -r ${dest}/${pkg_name}
else
	echo "${pkg_base_name} seems to be already installed."
fi
