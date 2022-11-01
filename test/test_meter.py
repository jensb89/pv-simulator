from meter import Meter

def test_meter_output_range():
    """Test that the output from the meter is between 0 and 9000W"""
    m = Meter()
    for i in range(500):
        datapoint = m.generateNewSample()
        assert(datapoint > 0 and datapoint < 9000)
            
    assert(True)
