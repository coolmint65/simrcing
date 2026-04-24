"""Tests for .svm setup file reader and writer."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rf2.parameters import get_default_setup
from rf2.svm import read_svm, write_svm


SAMPLE_SVM = """\
// A trimmed sample rF2 setup
[General]
Symmetric=1

[FRONTWING]
FWSetting=10//12 deg

[REARWING]
RWSetting=15//18 deg

[LEFTFRONT]
PressureSetting=5//140 kPa
CamberSetting=30//-3.2 deg

[RIGHTFRONT]
PressureSetting=5//140 kPa
CamberSetting=30//-3.2 deg

[LEFTREAR]
PressureSetting=5//135 kPa

[RIGHTREAR]
PressureSetting=5//135 kPa

[CONTROL]
BrakeBiasSetting=57//57.5 %

[DIFFERENTIAL]
PreloadSetting=30//60 Nm

[UNKNOWN]
MysteryKey=42//42
"""


class SvmTests(unittest.TestCase):

    def test_read_extracts_known_keys(self):
        with tempfile.NamedTemporaryFile("w", suffix=".svm", delete=False, encoding="utf-8") as f:
            f.write(SAMPLE_SVM)
            path = f.name
        try:
            setup, unmapped = read_svm(path)
        finally:
            os.unlink(path)

        self.assertEqual(setup["Aero"]["Front Wing Angle"], 12.0)
        self.assertEqual(setup["Aero"]["Rear Wing Angle"], 18.0)
        self.assertEqual(setup["Tires"]["Front Tire Pressure"], 140.0)
        self.assertEqual(setup["Tires"]["Rear Tire Pressure"], 135.0)
        self.assertEqual(setup["Suspension"]["Front Camber"], -3.2)
        self.assertEqual(setup["Brakes"]["Brake Bias"], 57.5)
        self.assertEqual(setup["Differential"]["Preload"], 60.0)

    def test_read_reports_unmapped_keys(self):
        with tempfile.NamedTemporaryFile("w", suffix=".svm", delete=False, encoding="utf-8") as f:
            f.write(SAMPLE_SVM)
            path = f.name
        try:
            _setup, unmapped = read_svm(path)
        finally:
            os.unlink(path)
        self.assertIn(("UNKNOWN", "MysteryKey"), unmapped)

    def test_write_then_read_roundtrips(self):
        setup = get_default_setup()
        setup["Aero"]["Front Wing Angle"] = 15
        setup["Aero"]["Rear Wing Angle"] = 22
        setup["Tires"]["Front Tire Pressure"] = 150
        setup["Brakes"]["Brake Bias"] = 58.5

        with tempfile.NamedTemporaryFile("w", suffix=".svm", delete=False) as f:
            path = f.name
        try:
            write_svm(path, setup)
            loaded, unmapped = read_svm(path)
        finally:
            os.unlink(path)

        self.assertEqual(loaded["Aero"]["Front Wing Angle"], 15)
        self.assertEqual(loaded["Aero"]["Rear Wing Angle"], 22)
        self.assertEqual(loaded["Tires"]["Front Tire Pressure"], 150)
        self.assertEqual(loaded["Brakes"]["Brake Bias"], 58.5)


if __name__ == "__main__":
    unittest.main()
