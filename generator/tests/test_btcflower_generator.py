import generator.weights as weights


def test_background():
    assert(calculate_sum(weights.background) == 100)


def test_background_accessory():
    assert(calculate_sum(weights.background_accessory) == 100)


def test_body_head():
    assert(calculate_sum(weights.body_head) == 100)


def test_top_head_leaf():
    assert(calculate_sum(weights.top_head_leaf) == 100)


def test_top_head_crown():
    assert(calculate_sum(weights.top_head_crown) == 100)


def test_top_head_chain():
    assert(calculate_sum(weights.top_head_chain) == 100)


def test_mask():
    assert(calculate_sum(weights.mask) == 100)


def test_eye():
    assert(calculate_sum(weights.eye) == 100)


def test_accessory():
    assert(calculate_sum(weights.accessory) == 100)


def test_bottom_head_accessory():
    assert(calculate_sum(weights.bottom_head_accessory) == 100)


def test_body_accessory():
    assert(calculate_sum(weights.body_accessory) == 100)


def test_neck():
    assert(calculate_sum(weights.neck) == 100)


def test_frame():
    assert(calculate_sum(weights.frame) == 100)


def test_laser():
    assert(calculate_sum(weights.laser) == 100)


def calculate_sum(weights):
    sum = 0
    for weight in weights:
        sum += weight
    return round(sum)
