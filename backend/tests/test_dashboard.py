from app.services.dashboard.engine import layout_engine

def test_grid_layout_boundary_validation() -> None:
    # 12-column bounds check
    assert layout_engine.validate_layout_grid({"x": 0, "w": 4}) is True
    assert layout_engine.validate_layout_grid({"x": 10, "w": 3}) is False  # x + w = 13
    assert layout_engine.validate_layout_grid({"x": -1, "w": 2}) is False
