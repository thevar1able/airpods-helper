## airpods-helper

A simple script to handle Airpods autoconnect on Linux.

tl;dr:
```shell
bluetoothctl power on
bluetoothctl scan on
bluetoothctl pair 14:87:6A:13:20:A2
bluetoothctl trust 14:87:6A:13:20:A2
bluetoothctl connect 14:87:6A:13:20:A2

# Arch Linux
cd pkgbuild
makepkg -si

systemctl enable --user airpods-helper@14:87:6A:13:20:A2.service --now

# Manual
pip install https://github.com/thevar1able/airpods-helper
airpods-helper
```