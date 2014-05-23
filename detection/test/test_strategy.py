from hhr import strategy
import cv2
import numpy as np

WIDTH = 320
HEIGHT = 240
PUCK_RADIUS = 10

def test_strategy_intercept_calc():
    pred = strategy.TableSimPredictor(WIDTH, HEIGHT)

    time_step = 0.1
    # [ puck-position, expected_intercept_point ]
    COORDS = [
        ((160,120), None),
        ((180,120), (280.0, 120.0)),
        ((200,120), (280.0, 120.0)),
        ((210,120), (280.0, 120.0)),
        ((220,120), (280.0, 120.0)),
        ((240,120), (280.0, 120.0)),
        ((260,120), (280.1, 120.0)),
        ((280,120), None),
        ((300,120), None),
        ((320,120), None)
        ]

    for (step, (pos, expected)) in zip(range(10), COORDS):
        print step, pos
        sim_time = time_step * step
        pred.add_puck_event(sim_time, pos, PUCK_RADIUS)
        i_point = pred.intercept_point()
        assert (i_point is None and expected is None) or np.allclose(i_point, expected)

