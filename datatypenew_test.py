# coding=utf-8
from __future__ import division

import unittest
import pytest
import math
PI = math.pi

from ladybug.datatypenew import DataTypes
from ladybug.datatypenew import DataTypeBase


class DataTypesTestCase(unittest.TestCase):
    """Test for (ladybug/datatype.py)"""

    # preparing to test.
    def setUp(self):
        """set up."""

    def tearDown(self):
        """Nothing to tear down as nothing gets written to file."""
        pass

    def test_all_possible_units(self):
        """Check to be sure that we can get all currently supported units."""
        all_types = DataTypes.all_possible_units()
        assert len(all_types.split('\n')) == len(DataTypes().BASETYPES)

    def test_type_by_name(self):
        """Check the type_by_name methods."""
        all_types = DataTypes().TYPES
        for typ in all_types.keys():
            assert hasattr(DataTypes.type_by_name(typ), 'isDataType')

    def test_type_by_unit(self):
        """Check the type_by_unit method."""
        all_types = DataTypes().BASETYPES
        for typ in range(len(all_types)):
            typ_units = all_types[typ].units
            for u in typ_units:
                assert hasattr(DataTypes.type_by_unit(u), 'isDataType')

    def test_type_by_name_and_unit(self):
        """Check the type_by_unit method."""
        all_types = DataTypes().BASETYPES
        for typ in range(len(all_types)):
            typ_name = all_types[typ].name
            typ_units = all_types[typ].units
            for u in typ_units:
                assert hasattr(DataTypes.type_by_name_and_unit(
                    typ_name, u), 'isDataType')

    def test_unitless_type(self):
        """Test the creation of generic types."""
        test_type = DataTypes.type_by_name_and_unit('Test Type', None)
        assert hasattr(test_type, 'isDataType')

    def test_generic_type(self):
        """Test the creation of generic types."""
        test_type = DataTypes.type_by_name_and_unit('Test Type', 'widgets')
        assert hasattr(test_type, 'isDataType')
        assert test_type.is_unit_acceptable('widgets')

    def test_json_methods(self):
        """Test to_json and from_json methods."""
        test_type = DataTypes.type_by_name_and_unit('Test Type', 'widgets')
        test_json = test_type.to_json()
        assert test_json == DataTypeBase.from_json(test_json).to_json()

        temp_type = DataTypes.type_by_name('Temperature')
        temp_json = temp_type.to_json()
        assert temp_json == DataTypeBase.from_json(temp_json).to_json()

    def test_temperature(self):
        """Test Temperature type."""
        temp_type = DataTypes.type_by_name('Temperature')
        for unit in temp_type.units:
            assert temp_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = temp_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = temp_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in temp_type.units:
                assert len(temp_type.to_unit([1], other_unit, unit)) == 1
        assert temp_type.to_unit([1], 'F', 'C')[0] == pytest.approx(33.8, rel=1e-1)
        assert temp_type.to_unit([1], 'K', 'C')[0] == pytest.approx(274.15, rel=1e-1)
        assert temp_type.to_unit([1], 'C', 'F')[0] == pytest.approx(-17.2222, rel=1e-1)
        assert temp_type.to_unit([1], 'C', 'K')[0] == pytest.approx(-272.15, rel=1e-1)

    def test_percentage(self):
        """Test Percentage type."""
        pct_type = DataTypes.type_by_name('Percentage')
        for unit in pct_type.units:
            assert pct_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = pct_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = pct_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in pct_type.units:
                assert len(pct_type.to_unit([1], other_unit, unit)) == 1
        assert pct_type.to_unit([1], 'fraction', '%')[0] == 0.01
        assert pct_type.to_unit([1], 'tenths', '%')[0] == 0.1
        assert pct_type.to_unit([1], 'thousandths', '%')[0] == 10
        assert pct_type.to_unit([1], '%', 'fraction')[0] == 100
        assert pct_type.to_unit([1], '%', 'tenths')[0] == 10
        assert pct_type.to_unit([1], '%', 'thousandths')[0] == 0.1

    def test_distance(self):
        """Test Distance type."""
        dist_type = DataTypes.type_by_name('Distance')
        for unit in dist_type.units:
            assert dist_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = dist_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = dist_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in dist_type.units:
                assert len(dist_type.to_unit([1], other_unit, unit)) == 1
        assert dist_type.to_unit([1], 'ft', 'm')[0] == pytest.approx(3.28084, rel=1e-2)
        assert dist_type.to_unit([1], 'mm', 'm')[0] == 1000
        assert dist_type.to_unit([1], 'in', 'm')[0] == pytest.approx(39.3701, rel=1e-1)
        assert dist_type.to_unit([1], 'km', 'm')[0] == 0.001
        assert dist_type.to_unit([1], 'mi', 'm')[0] == pytest.approx(1 / 1609.344, rel=1e-1)
        assert dist_type.to_unit([1], 'cm', 'm')[0] == 100
        assert dist_type.to_unit([1], 'm', 'ft')[0] == pytest.approx(1 / 3.28084, rel=1e-2)
        assert dist_type.to_unit([1], 'm', 'mm')[0] == 0.001
        assert dist_type.to_unit([1], 'm', 'in')[0] == pytest.approx(1 / 39.3701, rel=1e-1)
        assert dist_type.to_unit([1], 'm', 'km')[0] == 1000
        assert dist_type.to_unit([1], 'm', 'mi')[0] == pytest.approx(1609.344, rel=1e-1)
        assert dist_type.to_unit([1], 'm', 'cm')[0] == 0.01

    def test_area(self):
        """Test Area type."""
        area_type = DataTypes.type_by_name('Area')
        for unit in area_type.units:
            assert area_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = area_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = area_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in area_type.units:
                assert len(area_type.to_unit([1], other_unit, unit)) == 1
        assert area_type.to_unit([1], 'ft2', 'm2')[0] == pytest.approx(10.7639, rel=1e-2)
        assert area_type.to_unit([1], 'mm2', 'm2')[0] == 1000000
        assert area_type.to_unit([1], 'in2', 'm2')[0] == pytest.approx(1550, rel=1e-1)
        assert area_type.to_unit([1], 'km2', 'm2')[0] == 0.000001
        assert area_type.to_unit([1], 'mi2', 'm2')[0] == pytest.approx(1 / 2590000, rel=1e-8)
        assert area_type.to_unit([1], 'cm2', 'm2')[0] == 10000
        assert area_type.to_unit([1], 'ha', 'm2')[0] == 0.0001
        assert area_type.to_unit([1], 'acre', 'm2')[0] == pytest.approx(1 / 4046.86, rel=1e-8)
        assert area_type.to_unit([1], 'm2', 'ft2')[0] == pytest.approx(1 / 10.7639, rel=1e-3)
        assert area_type.to_unit([1], 'm2', 'mm2')[0] == 0.000001
        assert area_type.to_unit([1], 'm2', 'in2')[0] == pytest.approx(1 / 1550, rel=1e-4)
        assert area_type.to_unit([1], 'm2', 'km2')[0] == 1000000
        assert area_type.to_unit([1], 'm2', 'mi2')[0] == pytest.approx(2590000, rel=1e-1)
        assert area_type.to_unit([1], 'm2', 'cm2')[0] == 0.0001
        assert area_type.to_unit([1], 'm2', 'ha')[0] == 10000
        assert area_type.to_unit([1], 'm2', 'acre')[0] == pytest.approx(4046.86, rel=1e-1)

    def test_volume(self):
        """Test Volume type."""
        vol_type = DataTypes.type_by_name('Volume')
        for unit in vol_type.units:
            assert vol_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = vol_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = vol_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in vol_type.units:
                assert len(vol_type.to_unit([1], other_unit, unit)) == 1
        assert vol_type.to_unit([1], 'ft3', 'm3')[0] == pytest.approx(35.3147, rel=1e-2)
        assert vol_type.to_unit([1], 'mm3', 'm3')[0] == 1e+9
        assert vol_type.to_unit([1], 'in3', 'm3')[0] == pytest.approx(61023.7, rel=1e-1)
        assert vol_type.to_unit([1], 'km3', 'm3')[0] == 0.000000001
        assert vol_type.to_unit([1], 'mi3', 'm3')[0] == pytest.approx(1 / 4.168e+9, rel=1e-8)
        assert vol_type.to_unit([1], 'L', 'm3')[0] == 1000
        assert vol_type.to_unit([1], 'mL', 'm3')[0] == 1000000
        assert vol_type.to_unit([1], 'gal', 'm3')[0] == pytest.approx(264.172, rel=1e-1)
        assert vol_type.to_unit([1], 'fl oz', 'm3')[0] == pytest.approx(33814, rel=1e-1)
        assert vol_type.to_unit([1], 'm3', 'ft3')[0] == pytest.approx(1 / 35.3147, rel=1e-3)
        assert vol_type.to_unit([1], 'm3', 'mm3')[0] == 0.000000001
        assert vol_type.to_unit([1], 'm3', 'in3')[0] == pytest.approx(1 / 61023.7, rel=1e-5)
        assert vol_type.to_unit([1], 'm3', 'km3')[0] == 1e+9
        assert vol_type.to_unit([1], 'm3', 'mi3')[0] == pytest.approx(4.168e+9, rel=1e-1)
        assert vol_type.to_unit([1], 'm3', 'L')[0] == 0.001
        assert vol_type.to_unit([1], 'm3', 'mL')[0] == 0.000001
        assert vol_type.to_unit([1], 'm3', 'gal')[0] == pytest.approx(1 / 264.172, rel=1e-4)
        assert vol_type.to_unit([1], 'm3', 'fl oz')[0] == pytest.approx(1 / 33814, rel=1e-5)

    def test_pressure(self):
        """Test Pressure type."""
        press_type = DataTypes.type_by_name('Pressure')
        for unit in press_type.units:
            assert press_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = press_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = press_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in press_type.units:
                assert len(press_type.to_unit([1], other_unit, unit)) == 1
        assert press_type.to_unit([1], 'inHg', 'Pa')[0] == pytest.approx(0.0002953, rel=1e-5)
        assert press_type.to_unit([1], 'atm', 'Pa')[0] == pytest.approx(1 / 101325, rel=1e-7)
        assert press_type.to_unit([1], 'bar', 'Pa')[0] == 0.00001
        assert press_type.to_unit([1], 'Torr', 'Pa')[0] == pytest.approx(0.00750062, rel=1e-5)
        assert press_type.to_unit([1], 'psi', 'Pa')[0] == pytest.approx(0.000145038, rel=1e-5)
        assert press_type.to_unit([1], 'inH2O', 'Pa')[0] == pytest.approx(0.00401865, rel=1e-5)
        assert press_type.to_unit([1], 'Pa', 'inHg')[0] == pytest.approx(1 / 0.0002953, rel=1e-1)
        assert press_type.to_unit([1], 'Pa', 'atm')[0] == pytest.approx(101325, rel=1e-1)
        assert press_type.to_unit([1], 'Pa', 'bar')[0] == 100000
        assert press_type.to_unit([1], 'Pa', 'Torr')[0] == pytest.approx(1 / 0.00750062, rel=1e-1)
        assert press_type.to_unit([1], 'Pa', 'psi')[0] == pytest.approx(1 / 0.000145038, rel=1e-1)
        assert press_type.to_unit([1], 'Pa', 'inH2O')[0] == pytest.approx(1 / 0.00401865, rel=1e-1)

    def test_energy(self):
        """Test Energy type."""
        energy_type = DataTypes.type_by_name('Energy')
        for unit in energy_type.units:
            assert energy_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = energy_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = energy_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in energy_type.units:
                assert len(energy_type.to_unit([1], other_unit, unit)) == 1
        assert energy_type.to_unit([1], 'kBtu', 'kWh')[0] == pytest.approx(3.41214, rel=1e-2)
        assert energy_type.to_unit([1], 'Wh', 'kWh')[0] == 1000
        assert energy_type.to_unit([1], 'Btu', 'kWh')[0] == pytest.approx(3412.14, rel=1e-1)
        assert energy_type.to_unit([1], 'MMBtu', 'kWh')[0] == pytest.approx(0.00341214, rel=1e-5)
        assert energy_type.to_unit([1], 'J', 'kWh')[0] == 3600000
        assert energy_type.to_unit([1], 'kJ', 'kWh')[0] == 3600
        assert energy_type.to_unit([1], 'MJ', 'kWh')[0] == 3.6
        assert energy_type.to_unit([1], 'GJ', 'kWh')[0] == 0.0036
        assert energy_type.to_unit([1], 'therm', 'kWh')[0] == pytest.approx(0.0341214, rel=1e-5)
        assert energy_type.to_unit([1], 'cal', 'kWh')[0] == pytest.approx(860421, rel=1e-1)
        assert energy_type.to_unit([1], 'kcal', 'kWh')[0] == pytest.approx(860.421, rel=1e-2)
        assert energy_type.to_unit([1], 'kWh', 'kBtu')[0] == pytest.approx(1 / 3.41214, rel=1e-2)
        assert energy_type.to_unit([1], 'kWh', 'Wh')[0] == 0.001
        assert energy_type.to_unit([1], 'kWh', 'Btu')[0] == pytest.approx(1 / 3412.14, rel=1e-5)
        assert energy_type.to_unit([1], 'kWh', 'MMBtu')[0] == pytest.approx(1 / 0.00341214, rel=1e-1)
        assert energy_type.to_unit([1], 'kWh', 'J')[0] == 1 / 3600000
        assert energy_type.to_unit([1], 'kWh', 'kJ')[0] == 1 / 3600
        assert energy_type.to_unit([1], 'kWh', 'MJ')[0] == 1 / 3.6
        assert energy_type.to_unit([1], 'kWh', 'GJ')[0] == 1 / 0.0036
        assert energy_type.to_unit([1], 'kWh', 'therm')[0] == pytest.approx(1 / 0.0341214, rel=1e-1)
        assert energy_type.to_unit([1], 'kWh', 'cal')[0] == pytest.approx(1 / 860421, rel=1e-7)
        assert energy_type.to_unit([1], 'kWh', 'kcal')[0] == pytest.approx(1 / 860.421, rel=1e-4)

    def test_energy_intensity(self):
        """Test Energy type."""
        energyi_type = DataTypes.type_by_name('EnergyIntensity')
        for unit in energyi_type.units:
            assert energyi_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = energyi_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = energyi_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in energyi_type.units:
                assert len(energyi_type.to_unit([1], other_unit, unit)) == 1
        assert energyi_type.to_unit([1], 'kBtu/ft2', 'kWh/m2')[0] == pytest.approx(0.316998, rel=1e-3)
        assert energyi_type.to_unit([1], 'Wh/m2', 'kWh/m2')[0] == 1000
        assert energyi_type.to_unit([1], 'Btu/ft2', 'kWh/m2')[0] == pytest.approx(316.998, rel=1e-1)
        assert energyi_type.to_unit([1], 'kWh/m2', 'kBtu/ft2')[0] == pytest.approx(1 / 0.316998, rel=1e-2)
        assert energyi_type.to_unit([1], 'kWh/m2', 'Wh/m2')[0] == 0.001
        assert energyi_type.to_unit([1], 'kWh/m2', 'Btu/ft2')[0] == pytest.approx(1 / 316.998, rel=1e-5)

    def test_power(self):
        """Test Power type."""
        power_type = DataTypes.type_by_name('Power')
        for unit in power_type.units:
            assert power_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = power_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = power_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in power_type.units:
                assert len(power_type.to_unit([1], other_unit, unit)) == 1
        assert power_type.to_unit([1], 'Btu/h', 'W')[0] == pytest.approx(3.41214, rel=1e-3)
        assert power_type.to_unit([1], 'kW', 'W')[0] == 0.001
        assert power_type.to_unit([1], 'kBtu/h', 'W')[0] == pytest.approx(0.00341214, rel=1e-5)
        assert power_type.to_unit([1], 'TR', 'W')[0] == pytest.approx(1 / 3516.85, rel=1e-5)
        assert power_type.to_unit([1], 'hp', 'W')[0] == pytest.approx(1 / 745.7, rel=1e-5)
        assert power_type.to_unit([1], 'W', 'Btu/h')[0] == pytest.approx(1 / 3.41214, rel=1e-2)
        assert power_type.to_unit([1], 'W', 'kW')[0] == 1000
        assert power_type.to_unit([1], 'W', 'kBtu/h')[0] == pytest.approx(1 / 0.00341214, rel=1e-1)
        assert power_type.to_unit([1], 'W', 'TR')[0] == pytest.approx(3516.85, rel=1e-1)
        assert power_type.to_unit([1], 'W', 'hp')[0] == pytest.approx(745.7, rel=1e-1)

    def test_energy_flux(self):
        """Test Energy Flux type."""
        energyf_type = DataTypes.type_by_name('EnergyFlux')
        for unit in energyf_type.units:
            assert energyf_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = energyf_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = energyf_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in energyf_type.units:
                assert len(energyf_type.to_unit([1], other_unit, unit)) == 1
        assert energyf_type.to_unit([1], 'Btu/h-ft2', 'W/m2')[0] == pytest.approx(1 / 3.15459075, rel=1e-2)
        assert energyf_type.to_unit([1], 'kW/m2', 'W/m2')[0] == 0.001
        assert energyf_type.to_unit([1], 'kBtu/h-ft2', 'W/m2')[0] == pytest.approx(1 / 3154.59075, rel=1e-5)
        assert energyf_type.to_unit([1], 'W/ft2', 'W/m2')[0] == pytest.approx(1 / 10.7639, rel=1e-4)
        assert energyf_type.to_unit([1], 'met', 'W/m2')[0] == pytest.approx(1 / 58.2, rel=1e-4)
        assert energyf_type.to_unit([1], 'W/m2', 'Btu/h-ft2')[0] == pytest.approx(3.15459075, rel=1e-2)
        assert energyf_type.to_unit([1], 'W/m2', 'kW/m2')[0] == 1000
        assert energyf_type.to_unit([1], 'W/m2', 'kBtu/h-ft2')[0] == pytest.approx(3154.59075, rel=1e-1)
        assert energyf_type.to_unit([1], 'W/m2', 'W/ft2')[0] == pytest.approx(10.7639, rel=1e-1)
        assert energyf_type.to_unit([1], 'W/m2', 'met')[0] == pytest.approx(58.2, rel=1e-1)

    def test_illuminance(self):
        """Test Illuminance type."""
        ill_type = DataTypes.type_by_name('Illuminance')
        for unit in ill_type.units:
            assert ill_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = ill_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = ill_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in ill_type.units:
                assert len(ill_type.to_unit([1], other_unit, unit)) == 1
        assert ill_type.to_unit([1], 'fc', 'lux')[0] == pytest.approx(1 / 10.7639, rel=1e-3)
        assert ill_type.to_unit([1], 'lux', 'fc')[0] == pytest.approx(10.7639, rel=1e-1)

    def test_luminance(self):
        """Test luminance type."""
        lum_type = DataTypes.type_by_name('Luminance')
        for unit in lum_type.units:
            assert lum_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = lum_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = lum_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in lum_type.units:
                assert len(lum_type.to_unit([1], other_unit, unit)) == 1
        assert lum_type.to_unit([1], 'cd/ft2', 'cd/m2')[0] == pytest.approx(1 / 10.7639, rel=1e-3)
        assert lum_type.to_unit([1], 'cd/m2', 'cd/ft2')[0] == pytest.approx(10.7639, rel=1e-1)

    def test_angle(self):
        """Test angle type."""
        lum_type = DataTypes.type_by_name('Angle')
        for unit in lum_type.units:
            assert lum_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = lum_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = lum_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in lum_type.units:
                assert len(lum_type.to_unit([1], other_unit, unit)) == 1
        assert lum_type.to_unit([1], 'radians', 'degrees')[0] == pytest.approx(PI / 180, rel=1e-3)
        assert lum_type.to_unit([1], 'degrees', 'radians')[0] == pytest.approx((1 / PI) * 180, rel=1e-1)

    def test_mass(self):
        """Test Mass type."""
        mass_type = DataTypes.type_by_name('Mass')
        for unit in mass_type.units:
            assert mass_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = mass_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = mass_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in mass_type.units:
                assert len(mass_type.to_unit([1], other_unit, unit)) == 1
        assert mass_type.to_unit([1], 'lb', 'kg')[0] == pytest.approx(2.20462, rel=1e-3)
        assert mass_type.to_unit([1], 'g', 'kg')[0] == 1000
        assert mass_type.to_unit([1], 'tonne', 'kg')[0] == 0.001
        assert mass_type.to_unit([1], 'ton', 'kg')[0] == pytest.approx(1 / 907.185, rel=1e-5)
        assert mass_type.to_unit([1], 'oz', 'kg')[0] == pytest.approx(35.274, rel=1e-1)
        assert mass_type.to_unit([1], 'kg', 'lb')[0] == pytest.approx(1 / 2.20462, rel=1e-3)
        assert mass_type.to_unit([1], 'kg', 'g')[0] == 0.001
        assert mass_type.to_unit([1], 'kg', 'tonne')[0] == 1000
        assert mass_type.to_unit([1], 'kg', 'ton')[0] == pytest.approx(907.185, rel=1e-1)
        assert mass_type.to_unit([1], 'kg', 'oz')[0] == pytest.approx(1 / 35.274, rel=1e-3)

    def test_speed(self):
        """Test Speed type."""
        speed_type = DataTypes.type_by_name('Speed')
        for unit in speed_type.units:
            assert speed_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = speed_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = speed_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in speed_type.units:
                assert len(speed_type.to_unit([1], other_unit, unit)) == 1
        assert speed_type.to_unit([1], 'mph', 'm/s')[0] == pytest.approx(2.23694, rel=1e-3)
        assert speed_type.to_unit([1], 'km/h', 'm/s')[0] == 3.6
        assert speed_type.to_unit([1], 'knot', 'm/s')[0] == pytest.approx(1.94384, rel=1e-3)
        assert speed_type.to_unit([1], 'ft/s', 'm/s')[0] == pytest.approx(3.28084, rel=1e-3)
        assert speed_type.to_unit([1], 'm/s', 'mph')[0] == pytest.approx(1 / 2.23694, rel=1e-3)
        assert speed_type.to_unit([1], 'm/s', 'km/h')[0] == 1 / 3.6
        assert speed_type.to_unit([1], 'm/s', 'knot')[0] == pytest.approx(1 / 1.94384, rel=1e-3)
        assert speed_type.to_unit([1], 'm/s', 'ft/s')[0] == pytest.approx(1 / 3.28084, rel=1e-3)

    def test_volume_flow_rate(self):
        """Test VolumeFlowRate type."""
        vfr_type = DataTypes.type_by_name('VolumeFlowRate')
        for unit in vfr_type.units:
            assert vfr_type.to_unit([1], unit, unit)[0] == pytest.approx(1, rel=1e-5)
            ip_vals, ip_u = vfr_type.to_ip([1], unit)
            assert len(ip_vals) == 1
            si_vals, si_u = vfr_type.to_si([1], unit)
            assert len(si_vals) == 1
            for other_unit in vfr_type.units:
                assert len(vfr_type.to_unit([1], other_unit, unit)) == 1
        assert vfr_type.to_unit([1], 'ft3/s', 'm3/s')[0] == pytest.approx(35.3147, rel=1e-3)
        assert vfr_type.to_unit([1], 'L/s', 'm3/s')[0] == 1000
        assert vfr_type.to_unit([1], 'cfm', 'm3/s')[0] == pytest.approx(2118.88, rel=1e-1)
        assert vfr_type.to_unit([1], 'gpm', 'm3/s')[0] == pytest.approx(15850.3231, rel=1e-3)
        assert vfr_type.to_unit([1], 'mL/s', 'm3/s')[0] == 1000000
        assert vfr_type.to_unit([1], 'fl oz/s', 'm3/s')[0] == pytest.approx(33814, rel=1e-3)
        assert vfr_type.to_unit([1], 'm3/s', 'ft3/s')[0] == pytest.approx(1 / 35.3147, rel=1e-4)
        assert vfr_type.to_unit([1], 'm3/s', 'L/s')[0] == 0.001
        assert vfr_type.to_unit([1], 'm3/s', 'cfm')[0] == pytest.approx(1 / 2118.88, rel=1e-7)
        assert vfr_type.to_unit([1], 'm3/s', 'gpm')[0] == pytest.approx(1 / 15850.3231, rel=1e-8)
        assert vfr_type.to_unit([1], 'm3/s', 'mL/s')[0] == 0.000001
        assert vfr_type.to_unit([1], 'm3/s', 'fl oz/s')[0] == pytest.approx(1 / 33814, rel=1e-7)


if __name__ == "__main__":
    unittest.main()
