from pv_generator import PVGenerator
import datetime


def test_power_curve_output():
    """Test the power curve output at three signficant time points"""
    pv = PVGenerator()
    data10am = pv.get_data_point(
        datetime.datetime.now().replace(hour=10, minute=0, second=0)
    )
    data2pm = pv.get_data_point(
        datetime.datetime.now().replace(hour=14, minute=0, second=0)
    )
    data4pm = pv.get_data_point(
        datetime.datetime.now().replace(hour=16, minute=0, second=0)
    )
    assert data10am < data2pm
    assert data2pm > data4pm
    assert data2pm > 3.1
