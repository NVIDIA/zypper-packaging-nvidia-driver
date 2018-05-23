#!/bin/sh

driver_version=$(grep -i ^version: nvidia-gfxG0?.spec |awk '{print $2}')

for arch in x86 x86_64; do
  file=NVIDIA-Linux-${arch}-${driver_version}.run
  if [ ! -s ${file} ]; then
    echo -n "Dowloading ${file} ... "
    curl -s -o $file https://download.nvidia.com/XFree86/Linux-${arch}/${driver_version}/$file
    echo "done"
  fi
done

for arch in x86 x86_64; do
  file=NVIDIA-Linux-${arch}-${driver_version}.run
  test -f ${file}
  if [ $? -ne 0 ]; then
    echo "${file} not available. Download failed? Exiting."
    exit 1
  else
    echo -n "Checking ${file}: "
    sh ./${file} --check
    if [ $? -ne 0 ]; then
      rm ${file} 
      echo "Check failed. Corrupt {file} removed. Download failed? Exiting."
      exit 1
    fi
  fi
done

which sha256sum &> /dev/null
if [ $? -ne 0 ]; then
  echo "sha256sum not available! Exiting."
  exit 1
fi

sha256sum_x86=$(sha256sum NVIDIA-Linux-x86-${driver_version}.run | awk '{print $1}')
sha256sum_x86_64=$(sha256sum NVIDIA-Linux-x86_64-${driver_version}.run | awk '{print $1}')

echo -n "Creating _service file ..."
cat << EOF > _service
<services>
  <service name="download_files" mode="disabled"/>
  <service name="verify_file" mode="disabled">
    <param name="file">NVIDIA-Linux-x86-${driver_version}.run</param>
    <param name="verifier">sha256</param>
    <param name="checksum">${sha256sum_x86}</param>
  </service>
  <service name="verify_file" mode="disabled">
    <param name="file">NVIDIA-Linux-x86_64-${driver_version}.run</param>
    <param name="verifier">sha256</param>
    <param name="checksum">${sha256sum_x86_64}</param>
  </service>
</services>
EOF
echo done
