import pytestfrom src.masks import get_mask_account, get_mask_card_number@pytest.mark.parametrize("number_card, expected_card", [    (1596837868705199, '1596 83** **** 5199'),    (7158300734726758, '7158 30** **** 6758'),    (6831982476737658, '6831 98** **** 7658'),    (8990922113665229, '8990 92** **** 5229'),    (5999414228426353, '5999 41** **** 6353')])def test_get_mask_card_number(number_card, expected_card):    assert get_mask_card_number(number_card) == expected_carddef test_get_mask_account():    pass