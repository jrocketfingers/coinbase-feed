from collections import deque
from decimal import ROUND_DOWN, Decimal

from coinbase_feed.vwap import VWAPFrame, Datapoint


def test_empty_vwap():
	vwap = VWAPFrame()
	assert len(vwap.datapoints) == 0
	assert vwap.value_sum == 0
	assert vwap.quantity_sum == 0


def test_single_datapoint():
	vwap = VWAPFrame(deque([Datapoint(price=100, size=1)]))
	assert len(vwap.datapoints) == 1
	assert vwap.value_sum == 100
	assert vwap.quantity_sum == 1


def test_sample_precalculated_data():
	data = deque([
		Datapoint(price='44.26', size='35000'),
		Datapoint(price='43.96', size='32000'),
	])
	vwap = VWAPFrame(deque(data))

	assert len(vwap.datapoints) == 2
	assert vwap().quantize(Decimal('0.01'), ROUND_DOWN) == Decimal('44.11')


def test_adding_a_datapoint():
	vwap = VWAPFrame()
	vwap.add_datapoint(Datapoint(price='2', size='100'))

	assert len(vwap.datapoints) == 1
	assert vwap() == Decimal('2')


def test_adding_when_full():
	# given a full vwap deque
	vwap = VWAPFrame(
		initial_data=deque(
			[
				Datapoint(price='10', size='1'),
				Datapoint(price='10', size='1'),
				Datapoint(price='10', size='1')
			],
			maxlen=3
		),
	)

	# when a new datapoint is added
	vwap.add_datapoint(Datapoint(price='11', size='10'))

	# then the old datapoint should be dropped
	assert len(vwap.datapoints) == 1
	assert vwap().quantize('0.01', ROUND_DOWN) == Decimal('10.33')
