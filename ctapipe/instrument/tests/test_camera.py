import numpy as np
from astropy import units as u
from ctapipe.instrument import CameraGeometry
from ctapipe.instrument.camera import _find_neighbor_pixels, \
    _get_min_pixel_seperation
from numpy import median


def test_make_rectangular_camera_geometry():
    geom = CameraGeometry.make_rectangular()
    assert(geom.pix_x.shape == geom.pix_y.shape)


def test_load_hess_camera():
    geom = CameraGeometry.from_name("hess", 1)
    assert len(geom.pix_x) == 960


def test_guess_camera():
    px = np.linspace(-10, 10, 11328) * u.m
    py = np.linspace(-10, 10, 11328) * u.m
    geom = CameraGeometry.guess(px, py,0 * u.m)
    assert geom.pix_type.startswith('rect')


def test_get_min_pixel_seperation():
    x, y = np.meshgrid(np.linspace(-5, 5, 5), np.linspace(-5, 5, 5))
    pixsep = _get_min_pixel_seperation(x.ravel(), y.ravel())
    assert(pixsep == 2.5)


def test_find_neighbor_pixels():
    x, y = np.meshgrid(np.linspace(-5, 5, 5), np.linspace(-5, 5, 5))
    neigh = _find_neighbor_pixels(x.ravel(), y.ravel(), rad=3.1)
    assert(set(neigh[11]) == set([16, 6, 10, 12]))

def test_camera_neighbor_pixels():
    hexgeom = CameraGeometry.from_name("HESS", 1)
    recgeom = CameraGeometry.make_rectangular()

    # most pixels should have 4 neighbors for rectangular geometry and 6 for
    # hexagonal
    assert int(median(recgeom.neighbor_matrix.sum(axis=1))) == 4
    assert int(median(hexgeom.neighbor_matrix.sum(axis=1))) == 6

