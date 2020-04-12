# Maintainer: thevar1able <var1able@var1able.ru>

_pkgbase=airpods-helper
pkgname="${_pkgbase}-git"
pkgver=r3.4b3acde  # FIXME
pkgrel=1
pkgdesc="Small utility to automate Apple Airpods connection process"
arch=(any)
url="https://github.com/thevar1able/airpods-helper"
license=('MIT')
depends=('python' 'python-pydbus' 'python-gobject')
makedepends=('git')
optdepends=()
provides=("${_pkgbase}")
conflicts=("${_pkgbase}")
source=("git+https://github.com/thevar1able/airpods-helper.git")
sha256sums=('SKIP')

pkgver() {
    cd "${srcdir}/${_pkgbase}"
    (
        set -o pipefail
        git describe --long --tags 2>/dev/null | sed 's/^v//;s/\([^-]*-g\)/r\1/;s/-/./g' ||
        printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
    )
}

package() {
    cd "${srcdir}/${_pkgbase}"
    python setup.py install --root="$pkgdir/" --optimize=1

    install -D -m644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
    install -D -m644 systemd/airpods-companion.service "${pkgdir}/usr/lib/systemd/user/discordrp-mpris.service"
}