from flask import Flask


def test_get_blueprint(app: Flask):
    """
    This test ensures that the expected alerts API endpoints are
    configured in the app
    """
    expected_rules = (
        {
            'rule': '/api/vessels/',
            'methods': {'POST'}
        },
        {
            'rule': '/api/vessels/<code>',
            'methods': {'GET'}
        },
        {
            'rule': '/api/vessels/<vessel_code>/equipments/',
            'methods': {'GET'}
        },
        {
            'rule': '/api/vessels/<vessel_code>/equipments/',
            'methods': {'POST'}
        },
        {
            'rule': '/api/vessels/<vessel_code>/equipments/inactivate',
            'methods': {'PATCH'}
        }
    )

    for expected_rule in expected_rules:
        assert any(
            expected_rule['rule'] == rule.rule
            and expected_rule['methods'].issubset(rule.methods)
            for rule in list(app.url_map.iter_rules()))

