from colormath.color_objects import AdobeRGBColor, LCHabColor, LabColor
from colormath.color_conversions import convert_color
import numpy as np
from cycler import cycler
import matplotlib.pyplot as plt
import os


def get_color_cycler(
        n=5,
        l_min=70,
        c_min=30,
        h_min=0,
        a_min=0,
        b_min=0,
        l_max=None,
        c_max=None,
        h_max=None,
        a_max=None,
        b_max=None,
        type="Lch"):

    if type == "Lch":
        if not c_max:
            c_max = c_min
        if not h_max:
            h_max = h_min + 360 - (360 / n)
        if not l_max:
            l_max = l_min

    if type == "Lab":
        if not l_max:
            l_max = l_min
        if not a_max:
            a_max = - a_min
        if not b_max:
            b_max = - b_min

    if type == "Lch":
        rgb = get_lch_rgb(
            n=n,
            l_min=l_min,
            l_max=l_max,
            c_min=c_min,
            c_max=c_max,
            h_min=h_min,
            h_max=h_max,
            clamped_tuples=True)

    if type == "Lab":
        rgb = get_lch_rgb(
            n=n,
            l_min=l_min,
            l_max=l_max,
            a_min=a_min,
            a_max=a_max,
            b_min=b_min,
            b_max=b_max,
            clamped_tuples=True)

    cyc = cycler("color", rgb)
    return cyc


def get_lch_rgb(
        n=5,
        l_min=70,
        c_min=30,
        h_min=0,
        l_max=None,
        c_max=None,
        h_max=None,
        clamped_tuples=False):

    if not c_max:
            c_max = c_min
    if not h_max:
        h_max = h_min + 360 - (360 / n)
    if not l_max:
        l_max = l_min

    L = np.linspace(l_min, l_max, n)
    c = np.linspace(c_min, c_max, n)
    h = np.linspace(h_min, h_max, n)
    Lch = np.vstack((L, c, h)).T

    Lch_colors = [
        LCHabColor(Lch[i, 0], Lch[i, 1], Lch[i, 2])
        for i in range(Lch.shape[0])]
    rgb_colors = [
        convert_color(Lch_color, AdobeRGBColor, target_illuminant="D50")
        for Lch_color in Lch_colors]

    if clamped_tuples:

        clamped_rgb_tuples = [
            (color.clamped_rgb_r, color.clamped_rgb_g, color.clamped_rgb_b)
            for color in rgb_colors]

        return clamped_rgb_tuples

    return rgb_colors


def get_lab_rgb(
        n=5,
        l_min=80,
        a_min=30,
        b_min=30,
        l_max=None,
        a_max=None,
        b_max=None,
        clamped_tuples=False):

    if not l_max:
        l_max = l_min
    if not a_max:
        a_max = - a_min
    if not b_max:
        b_max = - b_min

    L = np.linspace(l_min, l_max, n)
    a = np.linspace(a_min, a_max, n)
    b = np.linspace(b_min, b_max, n)
    Lab = np.vstack((L, a, b)).T

    Lab_colors = [
        LabColor(Lab[i, 0], Lab[i, 1], Lab[i, 2])
        for i in range(Lab.shape[0])]
    rgb_colors = [
        convert_color(Lab_color, AdobeRGBColor, target_illuminant="D50")
        for Lab_color in Lab_colors]

    if clamped_tuples:

        clamped_rgb_tuples = [
            (color.clamped_rgb_r, color.clamped_rgb_g, color.clamped_rgb_b)
            for color in rgb_colors]

        return clamped_rgb_tuples

    return rgb_colors


def set_custom_style(style):
    package_directory = os.path.dirname(os.path.abspath(__file__))
    style_folder = "\\styles\\"
    file_extension = ".mplstyle"
    plt.style.use(
        "".join([package_directory, style_folder, style, file_extension]))
