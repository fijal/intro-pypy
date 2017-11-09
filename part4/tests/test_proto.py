
from proto.serializer import serialize, unserialize

class TestProto(object):
    def test_one(self):
        examples = [
            13,
            "foo",
            [1, 2, 3],
            [1, "foo", [1, 2, "bar"]],
            {"foo": [1, 2, 3], "bar": {"A": 13}},
        ]
        for item in examples:
            assert unserialize(serialize(item)) == item
