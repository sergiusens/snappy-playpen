The snappy playpen is a place to experiment and learn about [creating snaps for Ubuntu 16.04](https://developer.ubuntu.com/desktop). Feel free to:

- Add new snaps to the source tree
- Propose new snaps on the shopping list below
- Examine and learn from the existing apps

If you've got any questions, [let us know](https://developer.ubuntu.com/snappy/support)!

## Snap list

These are the apps that are either already snapped or currently worked on

| App           | Category      | Owner         | Progress      | Issues?       | Notes         |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| [Agar.io Clone](https://github.com/huytd/agar.io-clone) | Games  | Alan Pope  | BLOCKED  | [AppArmor denials](http://paste.ubuntu.com/15833002/)  | Tries to read `/var/snap` (should use `$SNAP` instead) (previous comment: Upstream bug - uses gulp at runtime, fails due to RO fs)  |
| [Atom](https://github.com/atom/atom)  | Development  | David Planella  | INPROGRESS  | - | Need to write a custom Snapcraft plugin that executes Atom's build steps |

## Snap shopping list

These apps are suggestions for the next snaps to work on

| App           | Category      | Owner         | Progress      | Issues?       | Notes         |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| [Dekko](https://code.launchpad.net/dekko) |  Mail  |             |             |             |             | 
