from hhr import strategy
import cv2
import numpy as np

WIDTH = 320
HEIGHT = 240
PUCK_RADIUS = 10

def test_pymunk_strategy_intercept_calc():
    pred = strategy.PyMunkPredictor(WIDTH, HEIGHT)
    strategy_intercept_calc(pred)

def test_box2d_strategy_intercept_calc():
    pred = strategy.Box2dPredictor(WIDTH, HEIGHT)
    strategy_intercept_calc(pred)

def strategy_intercept_calc(pred):
    time_step = cv2.getTickFrequency() * 0.1
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
        if i_point is None or expected is None:
            assert i_point == expected
        else:
            np.allclose(i_point, expected)



